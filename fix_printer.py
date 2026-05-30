NGROK = 'https://daintily-brute-expel.ngrok-free.dev'

FN = """
  function sendToPrinter(orderNum, name, phone, address, notes, payTxt, typeTxt) {
    var printData = {
      orderNum: orderNum, orderType: typeTxt, name: name, phone: phone,
      address: address||'', notes: notes||'', payMethod: payTxt,
      items: cart.map(function(c){ return {name:c.name, price:c.price, qty:c.qty}; }),
      total: getTotal()
    };
    fetch('""" + NGROK + """/print', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(printData)
    }).then(function(){ console.log('Bon gedruckt!'); })
      .catch(function(){ console.log('Drucker nicht erreichbar'); });
  }

"""

with open('index.html', encoding='utf-8') as f:
    html = f.read()

if 'function sendToPrinter' in html:
    print("sendToPrinter already exists!")
else:
    html = html.replace('  function submitOrder()', FN + '  function submitOrder()')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Done! sendToPrinter added.")
