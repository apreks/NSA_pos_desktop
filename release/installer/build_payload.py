"""Rebuild payload.zip from dist/FastFoodPOS and version.json."""
import zipfile, os

SRC = "dist/FastFoodPOS"
OUT = "release/installer/payload.zip"

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(SRC):
        for f in files:
            full = os.path.join(root, f)
            arc = os.path.relpath(full, SRC)
            z.write(full, arc)
    # Include version.json at root of payload
    z.write("version.json", "version.json")

size_mb = os.path.getsize(OUT) / 1024 / 1024
print(f"payload.zip: {size_mb:.2f} MB")
