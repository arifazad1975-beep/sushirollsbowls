"""
rename_images.py
Renames image files to match exact names expected by index.html
Run: python rename_images.py
"""
import os

# Map: current filename -> expected filename by HTML
RENAMES = {
    # Wrong name -> correct name
    'californian-roll.jpg':              'california-roll.jpg',
    'californian-roll.jpeg':             'california-roll.jpeg',
    'candian-roll.jpg':                  'canadian-roll.jpg',
    'candian-roll.jpeg':                 'canadian-roll.jpeg',
    'crunchy -tempura-garnelen-roll.jpg':'crunchy-tempura-garnelen-roll.jpg',
    'deluxe-specail-box.jpg':            'deluxe-special-box.jpg',
    'california-special-bos.jpg':        'california-special-box.jpg',
    'flambe-salmon-roll.jpg':            'flamb-salmon-roll.jpg',
    'flameed-salmon-special-roll.jpg':   'flamb-ed-salmon-special-roll.jpg',
    'kokonuess-mochi.jpg':               'kokosnuss-mochi.jpg',
    'salmoh-roket-roll.jpg':             'salmon-rocket-roll.jpg',
    'salmoh-roket-roll.jpeg':            'salmon-rocket-roll.jpeg',
    'avocado-nigiri..jpg':               'avocado-nigiri.jpg',
    'tokyo-nigiri-box-singel.jpg':       'tokyo-nigiri-box-single.jpg',
    'tropical-pafific-roll-4-stueck.jpg':'tropical-pacific-roll-4-stueck.jpg',
    'vegerariseche-tofu-ramen-suppe.jpg':'vegetarische-tofu-ramen-suppe.jpg',
    'zuerich-specaial-box.jpg':          'zuerich-special-box.jpg',
    'mixed-gyoza-12-stueck.jpg':         'chicken-gyoza-12-stueck.jpg',
    'chicken-momo-5-stueck.jpg':         'vegetarische-momo-5-stueck.jpg',
    'vegetarische-gyoza-5-srueck.jpg':   'vegetarische-gyoza-6-stueck.jpg',
}

folder = 'images'
count = 0

for old, new in RENAMES.items():
    old_path = os.path.join(folder, old)
    new_path = os.path.join(folder, new)
    if os.path.exists(old_path):
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"  Renamed: {old} -> {new}")
            count += 1
        else:
            print(f"  Skipped (exists): {new}")
    else:
        print(f"  Not found: {old}")

print(f"\nDone! {count} files renamed.")
print("\nNote: Some images may still be missing (never had them).")
print("Those will just show no image on the card - that is OK.")
