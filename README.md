# NSA Fast Food POS

## Requirements
- Python 3.10 or higher
- pip

## Run locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
python main.py
```

App data is stored in %APPDATA%\NSAFastFood. The main database is created there automatically as blazebite.db, so updates do not wipe local data.

## Build the Windows executable

Run build_exe.bat from the project root. The script activates .venv, updates PyInstaller, and builds with FastFoodPOS.spec.

Build output:

- dist/FastFoodPOS/FastFoodPOS.exe

## Packaged update behavior

- The install folder only contains application binaries and launcher scripts.
- User data, settings, invoices, and backups remain under %APPDATA%\NSAFastFood.
- Replacing or reinstalling the packaged app should preserve existing data unless that AppData folder is manually deleted.

## Current release highlights

- Modernized UI across login, POS, and admin views
- Reduced lag during refreshes and category changes
- Admin item tables are limited to the active store
- Root admin still has full cross-store visibility

## Project files

- main.py: main application entry point
- updater.py: in-app update checker and downloader
- version.py: local application version
- version.json: remote update manifest consumed by updater.py
- FastFoodPOS.spec: PyInstaller build definition
