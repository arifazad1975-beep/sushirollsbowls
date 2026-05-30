"""
add_print.py
Injects kitchen printer fetch code into index.html
Run: python add_print.py
"""

NGROK_URL = 'https://daintily-brute-expel.ngrok-free.dev'

PRINT_CODE = """
  // ── KITCHEN PRINTER ──
  function sendToPrinter(orderNum, name, phone, address, notes, payTxt, typeTxt) {
    var printData = {
      orderNum:  orderNum,
      orderType: typeTxt,
      name:      name,
      phone:     phone,
      address:   address || '',
      notes:     notes  || '',
      payMethod: payTxt,
      items:     cart.map(function(c){ return {name:c.name, price:c.price, qty:c.qty}; }),
      total:     getTotal()
    };
    fetch('""" + NGROK_URL + """/print', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(printData)
    }).then(function(){
      console.log('Bon gedruckt!');
    }).catch(function(){
      console.log('Drucker nicht erreichbar');
    });
  }
"""

SUBMIT_SEARCH = 'function submitOrder()'

SUBMIT_CODE = """  function submitOrder() {
    var name    = document.getElementById('co_name').value.trim();
    var phone   = document.getElementById('co_phone').value.trim();
    var address = document.getElementById('co_address') ? document.getElementById('co_address').value.trim() : '';
    var notes   = document.getElementById('co_notes').value.trim();

    if (!name || !phone) { alert('Bitte Name und Telefon eingeben!'); return; }
    if (orderType === 'delivery' && !address) { alert('Bitte Lieferadresse eingeben!'); return; }

    var orderNum = Math.floor(Math.random() * 9000) + 1000;
    var typeTxt  = orderType === 'pickup' ? 'PICKUP' : 'DELIVERY';
    var payTxt   = {cash:'Bar',twint:'TWINT',card:'Karte',online:'Online'}[payMethod] || payMethod;

    // Send to kitchen printer
    sendToPrinter(orderNum, name, phone, address, notes, payTxt, typeTxt);

    closeCheckout();
    document.getElementById('successNum').textContent = 'Bestellung #' + orderNum + ' · CHF ' + getTotal().toFixed(2);
    document.getElementById('successOverlay').classList.add('show');

    cart = [];
    updateCartUI();
  }
"""

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Check if submitOrder already exists
if 'function submitOrder()' in html:
    print("submitOrder() found — replacing it...")
    # Find and replace existing submitOrder
    start = html.find('function submitOrder()')
    # Find the closing of the function (next function or </script>)
    end = html.find('\n  function ', start + 1)
    if end == -1:
        end = html.find('\n</script>', start)
    if end == -1:
        print("ERROR: Could not find end of submitOrder function")
    else:
        html = html[:start] + SUBMIT_CODE.strip() + '\n' + html[end:]
        print("submitOrder() replaced.")
else:
    print("submitOrder() NOT found — appending before </script>")
    html = html.replace('</script>', PRINT_CODE + '\n' + SUBMIT_CODE + '\n</script>', 1)

# Add sendToPrinter function before submitOrder
if 'sendToPrinter' not in html:
    html = html.replace('function submitOrder()', PRINT_CODE + '\n  function submitOrder()')
    print("sendToPrinter() injected.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! index.html updated with printer code.")
print(f"Ngrok URL: {NGROK_URL}")
