================================================================================
                   NSA FAST FOOD POS SYSTEM v1.0
           Point of Sale System for Fast Food Restaurant
================================================================================

SYSTEM REQUIREMENTS
─────────────────────────────────────────────────────────────────────────────
✓ Windows 7 SP1 or later (Windows 10/11 recommended)
✓ 100 MB free disk space (includes application and dependencies)
✓ 2 GB RAM minimum (4 GB or more recommended)
✓ Write permissions to Program Files and user AppData folders
✓ No Python or additional runtime installation required (fully standalone EXE)

INSTALLATION INSTRUCTIONS
─────────────────────────────────────────────────────────────────────────────

Method 1: Using the Setup Wizard (Recommended)
1. Extract the downloaded ZIP file to your desired location
2. Double-click "setup.bat"
3. Wait for the installation to complete
4. The application will be installed to: C:\Program Files\NSAFastFood
5. Shortcuts will be created in:
   - Start Menu > NSAFastFood > NSA Fast Food POS
   - Desktop (optional)

Method 2: Manual Installation
1. Extract the ZIP file to your desired location (e.g., C:\NSAFastFood)
2. Run FastFoodPOS.exe directly from the dist\FastFoodPOS folder
3. Create shortcuts manually if desired

FIRST RUN SETUP
─────────────────────────────────────────────────────────────────────────────
On first launch, the application will:
✓ Create user data folder in: C:\Users\[YourUsername]\AppData\Roaming\NSAFastFood
✓ Initialize SQLite database: blazebite.db
✓ Load sample menu items and stores
✓ Display login screen

DEFAULT CREDENTIALS (Change these immediately!)
─────────────────────────────────────────────────────────────────────────────
Store: fast_food or cold_store
Username: admin or user1
Password: (Check with store administrator)
Admin Password: admin123

LAUNCHING THE APPLICATION
─────────────────────────────────────────────────────────────────────────────
► Run the application using any of these methods:
  • Double-click FastFoodPOS.exe in C:\Program Files\NSAFastFood
  • Click "NSA Fast Food POS" in Start Menu
  • Click the Desktop shortcut (if created)

APPLICATION FEATURES
─────────────────────────────────────────────────────────────────────────────
✓ Multi-store POS system (Fast Food & Cold Store)
✓ Real-time inventory management
✓ Comprehensive sales reporting and analytics
✓ Receipt printing (requires default printer setup in Windows)
✓ User role-based access (Attendant, Admin)
✓ Secure login with encrypted database
✓ Built-in audit trail for all transactions

DATA STORAGE
─────────────────────────────────────────────────────────────────────────────
All application data is stored in:
  C:\Users\[YourUsername]\AppData\Roaming\NSAFastFood

This includes:
  • blazebite.db - Main application database
  • invoice_XXXX.txt - Generated receipts and invoices

Note: If this folder is deleted, the application will start fresh on next run.

UNINSTALLING THE APPLICATION
─────────────────────────────────────────────────────────────────────────────

Method 1: Using Uninstall Script
1. Run "uninstall.bat" in the installation folder
2. Or from Start Menu > NSAFastFood > right-click > Uninstall
3. All application files will be removed (user data preserved)

Method 2: Windows Settings
1. Go to Settings > Apps > Installed Apps
2. Find "NSA Fast Food POS System" in the list
3. Click the app and select "Uninstall"

To completely remove all user data (optional):
  Delete: C:\Users\[YourUsername]\AppData\Roaming\NSAFastFood

TROUBLESHOOTING
─────────────────────────────────────────────────────────────────────────────

Problem: "FastFoodPOS.exe is not found"
Solution: Make sure you ran setup.bat from the folder containing the 'dist' directory,
          and that the extraction was completed successfully.

Problem: Application won't start
Solution: 1. Try running as Administrator
          2. Ensure you have write permissions to C:\Program Files
          3. Try reinstalling using setup.bat
          4. Check if any antivirus software is blocking the EXE

Problem: Cannot print receipts
Solution: 1. Set a default printer in Windows Settings > Devices > Printers
          2. Ensure your printer is turned on and connected
          3. Try printing a test page from Windows first

Problem: Database errors on startup
Solution: Delete the database file at:
          C:\Users\[YourUsername]\AppData\Roaming\NSAFastFood\blazebite.db
          The application will recreate it on next launch

PRINTING SETUP
─────────────────────────────────────────────────────────────────────────────
To enable receipt printing:
1. Open Windows Settings > Devices > Printers & Scanners
2. Click on your desired printer
3. Click "Manage" > "Set as default"
4. Restart the application

SUPPORT & DOCUMENTATION
─────────────────────────────────────────────────────────────────────────────
For issues, questions, or feature requests:
• Check the README.md file in this folder
• Run the application and check the Help menu
• Test with the demo credentials provided above

VERSION INFORMATION
─────────────────────────────────────────────────────────────────────────────
Version: 1.0
Build Date: March 2026
Built with: Python 3.x + CustomTkinter + SQLite
Available for: Windows 7+ (64-bit)

================================================================================
Thank you for using NSA Fast Food POS System!
================================================================================
