"""Build release/POS_Update.zip with update scripts and payload."""
import os
import zipfile

FILES = [
    ("release/installer/install_update.bat", "install_update.bat"),
    ("release/installer/uninstall.bat", "uninstall.bat"),
    ("release/installer/payload.zip", "payload.zip"),
]
OUT = "release/POS_Update.zip"

for src, _ in FILES:
    if not os.path.exists(src):
        raise FileNotFoundError(f"Missing required file: {src}")

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as archive:
    for src, arc in FILES:
        archive.write(src, arc)

size_mb = os.path.getsize(OUT) / 1024 / 1024
print(f"POS_Update.zip: {size_mb:.2f} MB")
