"""
patch_sushi.py
Run: python3 patch_sushi.py
Input:  index.html  (your sushi page, same folder)
Output: index_updated.html
Changes:
  1. addItem() gains taxType param ('food'|'drink')
  2. All Getränke addItem calls use 'drink'
  3. calcTax() helper added
  4. submitOrder() — WhatsApp removed, tax sent to printer & receipt
  5. Checkout modal shows MwSt breakdown
  6. Receipt includes tax lines
"""

import re

SRC  = 'index.html'
DEST = 'index_updated.html'

with open(SRC, encoding='utf-8') as f:
    html = f.read()

# ── 1. Mark drink items (Getränke section only) ───────────────────────────────
# All drink addItem calls are in cat-drinks section. Replace their taxType.
DRINK_NAMES = [
    "Coca-Cola 0.5l", "Coca-Cola ZERO 0.5l", "Fanta Orange 0.5l",
    "Sprite 0.5l", "Apfelschorle 0.5l", "Arizona Green Tea 0.5l",
    "Arizona Mucho Mango 0.5l", "Mineralwasser 0.5l",
    "Stilles Wasser 0.5l", "RedBull 0.25l"
]
for name in DRINK_NAMES:
    # Match addItem('Name',price,this) — no taxType yet
    pattern = r"addItem\('" + re.escape(name) + r"',([\d.]+),this\)"
    replacement = r"addItem('" + name + r"',\1,this,'drink')"
    html = re.sub(pattern, replacement, html)

# ── 2. All remaining addItem calls (food) — add 'food' where no taxType yet ──
html = re.sub(
    r"addItem\('([^']+)',([\d.]+),this\)(?!')",
    r"addItem('\1',\2,this,'food')",
    html
)

# ── 3. Replace the JS cart state block & addItem function ────────────────────
OLD_CART_STATE = """  // ── CART STATE ──
  var cart = [];
  var orderType = 'pickup';
  var payMethod = 'cash';

  function addItem(name, price, btn) {
    var existing = cart.find(function(c){ return c.name === name; });
    if (existing) {
      existing.qty++;
    } else {
      cart.push({name: name, price: price, qty: 1});
    }"""

NEW_CART_STATE = """  // ── TAX RATES (Swiss MwSt, gross-inclusive) ──
  var TAX_FOOD  = 0.026; // 2.6% Speisen
  var TAX_DRINK = 0.081; // 8.1% Getränke

  // ── CART STATE ──
  var cart = [];
  var orderType = 'pickup';
  var payMethod = 'cash';

  // calcTax: splits cart into food/drink and extracts net + tax from gross prices
  function calcTax() {
    var foodGross = 0, drinkGross = 0;
    cart.forEach(function(c) {
      var line = c.price * c.qty;
      if (c.taxType === 'drink') drinkGross += line;
      else foodGross += line;
    });
    var foodTax   = foodGross  - (foodGross  / (1 + TAX_FOOD));
    var drinkTax  = drinkGross - (drinkGross / (1 + TAX_DRINK));
    return {
      foodGross:  foodGross,
      drinkGross: drinkGross,
      foodNet:    foodGross  - foodTax,
      drinkNet:   drinkGross - drinkTax,
      foodTax:    foodTax,
      drinkTax:   drinkTax,
      total:      foodGross + drinkGross
    };
  }

  function addItem(name, price, btn, taxType) {
    var existing = cart.find(function(c){ return c.name === name; });
    if (existing) {
      existing.qty++;
    } else {
      cart.push({name: name, price: price, qty: 1, taxType: taxType || 'food'});
    }"""

html = html.replace(OLD_CART_STATE, NEW_CART_STATE, 1)

# ── 4. Replace openCheckout() order summary section ─────────────────────────
OLD_SUMMARY = """    var items = cart.map(function(c){
      return '<div class="os-item"><span>' + c.qty + 'x ' + c.name + '</span><span>CHF ' + (c.price*c.qty).toFixed(2) + '</span></div>';
    }).join('');
    document.getElementById('modalItems').innerHTML = items;
    document.getElementById('modalTotal').textContent = 'CHF ' + getTotal().toFixed(2);"""

NEW_SUMMARY = """    var items = cart.map(function(c){
      return '<div class="os-item"><span>' + c.qty + 'x ' + c.name + '</span><span>CHF ' + (c.price*c.qty).toFixed(2) + '</span></div>';
    }).join('');
    document.getElementById('modalItems').innerHTML = items;

    // Tax breakdown
    var t = calcTax();
    var taxHtml = '<hr style="border:none;border-top:1px dashed #ede8e0;margin:8px 0;">';
    if (t.foodGross > 0) {
      taxHtml += '<div style="display:flex;justify-content:space-between;font-size:12px;color:#6b6b6b;margin-bottom:3px;"><span>Speisen Netto</span><span>CHF ' + t.foodNet.toFixed(2) + '</span></div>';
      taxHtml += '<div style="display:flex;justify-content:space-between;font-size:12px;color:#6b6b6b;margin-bottom:3px;"><span>MwSt. 2.6% Speisen</span><span>CHF ' + t.foodTax.toFixed(2) + '</span></div>';
    }
    if (t.drinkGross > 0) {
      taxHtml += '<div style="display:flex;justify-content:space-between;font-size:12px;color:#6b6b6b;margin-bottom:3px;"><span>Getränke Netto</span><span>CHF ' + t.drinkNet.toFixed(2) + '</span></div>';
      taxHtml += '<div style="display:flex;justify-content:space-between;font-size:12px;color:#6b6b6b;margin-bottom:3px;"><span>MwSt. 8.1% Getränke</span><span>CHF ' + t.drinkTax.toFixed(2) + '</span></div>';
    }
    document.getElementById('modalTaxRows').innerHTML = taxHtml;
    document.getElementById('modalTotal').textContent = 'CHF ' + t.total.toFixed(2);"""

html = html.replace(OLD_SUMMARY, NEW_SUMMARY, 1)

# ── 5. Add tax rows placeholder in modal HTML ────────────────────────────────
OLD_MODAL_TOTAL = """        <div class="os-total"><span>Total</span><span id="modalTotal">CHF 0.00</span></div>"""
NEW_MODAL_TOTAL = """        <div id="modalTaxRows"></div>
        <div class="os-total"><span>Total (inkl. MwSt.)</span><span id="modalTotal">CHF 0.00</span></div>"""
html = html.replace(OLD_MODAL_TOTAL, NEW_MODAL_TOTAL, 1)

# ── 6. Remove WhatsApp from submitOrder ──────────────────────────────────────
# Remove the window.open wa.me line
html = re.sub(
    r'\s*// Send to WhatsApp\s*\n\s*window\.open\(\'https://wa\.me/[^\']+\?text=\' \+ encodeURIComponent\(msg\), \'_blank\'\);',
    '',
    html
)
# Remove the entire msg building block (not needed without WA)
html = re.sub(
    r"\s*// WhatsApp message\n.*?msg \+= '💳 \*Zahlung:\* ' \+ payTxt;",
    '',
    html,
    flags=re.DOTALL
)

# ── 7. Add tax to printData in submitOrder ───────────────────────────────────
OLD_PRINT_DATA = """  var printData = {
    orderNum: orderNum,
    orderType: orderType,
    name: name,
    phone: phone,
    address: address || '',
    notes: notes || '',
    payMethod: payTxt,
    items: cart.map(function(c){ return {name:c.name, price:c.price, qty:c.qty}; }),
    total: getTotal()
  };"""

NEW_PRINT_DATA = """  var _tax = calcTax();
  var printData = {
    orderNum:  orderNum,
    orderType: orderType,
    name:      name,
    phone:     phone,
    address:   address || '',
    notes:     notes || '',
    payMethod: payTxt,
    items:     cart.map(function(c){ return {name:c.name, price:c.price, qty:c.qty, taxType:c.taxType}; }),
    foodNet:   _tax.foodNet,
    foodTax:   _tax.foodTax,
    drinkNet:  _tax.drinkNet,
    drinkTax:  _tax.drinkTax,
    total:     _tax.total
  };"""

html = html.replace(OLD_PRINT_DATA, NEW_PRINT_DATA, 1)

# ── 8. Add tax lines to receipt HTML in printReceipt() ──────────────────────
OLD_RECEIPT_TOTAL = """    '<div style="display:flex;justify-content:space-between;font-weight:bold;font-size:13px;">' +
      '<span>TOTAL</span><span>CHF ' + total.toFixed(2) + '</span>' +
    '</div>' +"""

NEW_RECEIPT_TOTAL = """    (items.some(function(i){return i.taxType!=='drink';}) ?
      '<div style="display:flex;justify-content:space-between;font-size:10px;color:#555;">' +
        '<span>MwSt. 2.6% Speisen</span><span>CHF ' + (printData&&printData.foodTax?printData.foodTax.toFixed(2):'0.00') + '</span>' +
      '</div>' : '') +
    (items.some(function(i){return i.taxType==='drink';}) ?
      '<div style="display:flex;justify-content:space-between;font-size:10px;color:#555;">' +
        '<span>MwSt. 8.1% Getränke</span><span>CHF ' + (printData&&printData.drinkTax?printData.drinkTax.toFixed(2):'0.00') + '</span>' +
      '</div>' : '') +
    '<div style="border-top:1px dashed #000;margin:4px 0;"></div>' +
    '<div style="display:flex;justify-content:space-between;font-weight:bold;font-size:13px;">' +
      '<span>TOTAL (inkl. MwSt.)</span><span>CHF ' + total.toFixed(2) + '</span>' +
    '</div>' +"""

html = html.replace(OLD_RECEIPT_TOTAL, NEW_RECEIPT_TOTAL, 1)

# ── 9. Update success button label ──────────────────────────────────────────
html = html.replace(
    "document.getElementById('successNum').textContent = 'Bestellung #' + orderNum + ' · CHF ' + getTotal().toFixed(2);",
    "document.getElementById('successNum').textContent = 'Bestellung #' + orderNum + ' · CHF ' + _tax.total.toFixed(2);"
)

with open(DEST, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Written to", DEST)
print("Drink items tagged:", sum(1 for n in __import__('re').findall(r"addItem\('[^']+','[^']+',this,'(drink)'", html)))
print("wa.me remaining:", html.count("wa.me"))
