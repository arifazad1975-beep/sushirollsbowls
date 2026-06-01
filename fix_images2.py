"""
fix_images2.py
Fixes remaining missing images by:
1. Renaming .JPG (uppercase) to .jpg
2. Copying .jpeg files to .jpg where .jpg doesn't exist
3. Renaming files with wrong names
Run: python fix_images2.py
"""
import os
import shutil

folder = 'images'
files = os.listdir(folder)
count = 0

# Step 1: Rename .JPG uppercase to .jpg lowercase
for f in files:
    if f.endswith('.JPG'):
        old = os.path.join(folder, f)
        new = os.path.join(folder, f[:-4] + '.jpg')
        if not os.path.exists(new):
            os.rename(old, new)
            print(f"Renamed: {f} -> {f[:-4]}.jpg")
            count += 1
        else:
            # .jpg already exists, delete the .JPG
            os.remove(old)
            print(f"Removed duplicate: {f}")

# Refresh file list
files = os.listdir(folder)

# Step 2: Copy .jpeg to .jpg where .jpg missing
for f in files:
    if f.endswith('.jpeg'):
        base = f[:-5]  # remove .jpeg
        jpg_name = base + '.jpg'
        jpg_path = os.path.join(folder, jpg_name)
        jpeg_path = os.path.join(folder, f)
        if not os.path.exists(jpg_path):
            shutil.copy2(jpeg_path, jpg_path)
            print(f"Copied: {f} -> {jpg_name}")
            count += 1

# Refresh file list
files = os.listdir(folder)
files_lower = [f.lower() for f in files]

# Step 3: Fix specific wrong filenames
RENAMES = {
    'fitness-tuna-roll.jpg': None,  # need to check what we have
    'lachs-special-box.jpg': 'lachs-special-box.jpeg',
    'nigiri-mixed-big-box.jpg': 'nigiri-mixed-big-box.jpeg', 
    'nigiri-mixed-box-single.jpg': 'nigiri-mixed-box-single.jpeg',
    'inside-out-box.jpg': 'inside-out-box.jpeg',
    'tokyo-mixed-maki-box.jpg': 'tokyo-mixed-maki-box.jpeg',
    'fitness-special-box.jpg': None,
    'big-maki-fish-box-48-stueck.jpg': None,
    'maki-box.jpg': None,
}

print(f"\nDone! {count} files fixed.")
print("\nChecking what's still missing...")

MISSING = [
    'canadian-delux-spezial-roll.jpg', 'delux-salmon-roll.jpg',
    'mango-pacific-roll.jpg', 'fitness-roll.jpg', 'tuna-delux-special-roll.jpg',
    'fitness-tuna-roll.jpg', 'rainbow-roll.jpg', 'fitness-smart-roll.jpg',
    'vegetarian-roll.jpg', 'tuna-rocket-roll.jpg', 'tuna-roll.jpg',
    'fitness-maki.jpg', 'mango-maki.jpg', 'mango-pacific-roll-4-stueck.jpg',
    'kappa-maki.jpg', 'ebi-maki.jpg', 'spicy-tuna-maki.jpg', 'shake-maki.jpg',
    'surimi-mayo-maki.jpg', 'tamago-maki.jpg', 'tokyo-special-maki.jpg',
    'teriyaki-chicken-maki.jpg', 'avocado-maki.jpg', 'tekka-maki.jpg',
    'vegetarische-gyoza-12-stueck.jpg', 'rind-momo-5-stueck.jpg',
    'flambierter-lachs-nigiri.jpg', 'big-maki-fish-box-48-stueck.jpg',
    'inside-out-box.jpg', 'fitness-special-box.jpg', 'nigiri-mixed-big-box.jpg',
    'tokyo-mixed-maki-box.jpg', 'maki-box.jpg', 'lachs-special-box.jpg',
    'nigiri-mixed-box-single.jpg', 'maguro-nigiri.jpg',
    'sushi-reis.jpg', 'mineralwasser-0-5l.jpg', 'chilli-mayo-dip.jpg',
    'sojasauce.jpg', 'teriyaki-dip.jpg', 'erdnuss-dip.jpg', 'ingwer.jpg',
    'mango-dip.jpg', 'sesam-dip.jpg',
    'coca-cola-0-5l.jpg', 'coca-cola-zero-0-5l.jpg', 'fanta-orange-0-5l.jpg',
    'sprite-0-5l.jpg', 'arizona-green-tea-0-5l.jpg', 'apfelschorle-0-5l.jpg',
    'stilles-wasser-0-5l.jpg', 'arizona-mucho-mango-0-5l.jpg', 'redbull-0-25l.jpg',
]

current_files = os.listdir(folder)
still_missing = []
fixed_now = []

for m in MISSING:
    if m in current_files:
        fixed_now.append(m)
    else:
        still_missing.append(m)

print(f"\n✅ Fixed ({len(fixed_now)}):")
for f in fixed_now:
    print(f"  {f}")

print(f"\n❌ Still missing ({len(still_missing)}):")
for f in still_missing:
    print(f"  {f}")
