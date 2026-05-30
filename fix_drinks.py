"""
fix_drinks.py
Run after patch_sushi.py — tags Getraenke items with 'drink' taxType.
Run: python fix_drinks.py
"""

with open('index_updated.html', encoding='utf-8') as f:
    html = f.read()

DRINKS = [
    "Coca-Cola 0.5l", "Coca-Cola ZERO 0.5l", "Fanta Orange 0.5l",
    "Sprite 0.5l", "Apfelschorle 0.5l", "Arizona Green Tea 0.5l",
    "Arizona Mucho Mango 0.5l", "Mineralwasser 0.5l",
    "Stilles Wasser 0.5l", "RedBull 0.25l"
]

count = 0
for name in DRINKS:
    # Match both: addItem('Name',price,this) and addItem('Name',price,this,'food')
    old1 = f"addItem('{name}',"
    # Find every occurrence and fix taxType
    import re
    # Replace no taxType version
    pattern1 = r"addItem\('" + re.escape(name) + r"',([\d.]+),this\)"
    replacement1 = f"addItem('{name}'," + r"\1,this,'drink')"
    new_html, n1 = re.subn(pattern1, replacement1, html)
    # Replace 'food' version
    pattern2 = r"addItem\('" + re.escape(name) + r"',([\d.]+),this,'food'\)"
    replacement2 = f"addItem('{name}'," + r"\1,this,'drink')"
    new_html, n2 = re.subn(pattern2, replacement2, new_html)
    html = new_html
    total = n1 + n2
    count += total
    print(f"  {name}: {total} fixed")

with open('index_updated.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal drink items tagged: {count}")
print("Done — index_updated.html updated.")
