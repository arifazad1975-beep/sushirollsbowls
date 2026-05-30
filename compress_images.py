"""
compress_images.py
Compresses all JPEG/PNG images in the images/ folder.
Run: python3 compress_images.py

Requirements: pip install pillow
"""

from PIL import Image
import os

INPUT_FOLDER  = 'images'        # your images folder
OUTPUT_FOLDER = 'images'        # overwrites in place (set to 'images_compressed' to keep originals)
MAX_WIDTH     = 800             # max width in pixels (enough for menu cards)
JPEG_QUALITY  = 75              # 75 is good balance — quality vs file size

SUPPORTED = ('.jpg', '.jpeg', '.png', '.webp')

def compress_images():
    if not os.path.exists(INPUT_FOLDER):
        print(f"Folder '{INPUT_FOLDER}' not found. Make sure this script is in the same folder as your images/ directory.")
        return

    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(SUPPORTED)]
    total = len(files)
    print(f"Found {total} images. Compressing...")

    total_before = 0
    total_after  = 0

    for i, filename in enumerate(files, 1):
        path = os.path.join(INPUT_FOLDER, filename)
        size_before = os.path.getsize(path)
        total_before += size_before

        try:
            img = Image.open(path)

            # Convert RGBA/P to RGB for JPEG saving
            if img.mode in ('RGBA', 'P', 'LA'):
                img = img.convert('RGB')

            # Resize if wider than MAX_WIDTH
            w, h = img.size
            if w > MAX_WIDTH:
                ratio   = MAX_WIDTH / w
                new_h   = int(h * ratio)
                img     = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)

            # Save — always as JPEG for smallest size
            out_path = os.path.join(OUTPUT_FOLDER, os.path.splitext(filename)[0] + '.jpeg')
            img.save(out_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)

            size_after = os.path.getsize(out_path)
            total_after += size_after
            saved = (1 - size_after / size_before) * 100

            print(f"[{i}/{total}] {filename} — {size_before//1024}KB → {size_after//1024}KB ({saved:.0f}% smaller)")

        except Exception as e:
            print(f"[{i}/{total}] SKIP {filename} — {e}")

    print()
    print(f"Done! {total_before//1024//1024:.1f}MB → {total_after//1024//1024:.1f}MB total")
    print(f"Saved {(total_before - total_after)//1024//1024:.1f}MB")

if __name__ == '__main__':
    compress_images()
