@echo off
setlocal enabledelayedexpansion

REM ═══════════════════════════════════════════════════════════════
REM  NSA Fast Food POS - Installation Script
REM ═══════════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════╗
echo ║   NSA Fast Food POS - Setup Wizard        ║
echo ║   Version 1.2.0                           ║
echo ╚═══════════════════════════════════════════╝
echo.

REM Get the installation directory
set "INSTALL_DIR=%LocalAppData%\Programs\NSAFastFood"
set "DESKTOP=%USERPROFILE%\Desktop"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"

echo Detecting installation location...
echo Default: %INSTALL_DIR%
echo.

REM Check if app is running
tasklist /FI "IMAGENAME eq FastFoodPOS.exe" 2>nul | find /I /N "FastFoodPOS.exe">nul
if "%ERRORLEVEL%"=="0" (
    echo [INFO] Closing running application...
    taskkill /IM FastFoodPOS.exe /F >nul 2>&1
)

REM Check if running from correct location
if not exist "dist\FastFoodPOS\FastFoodPOS.exe" (
    echo [ERROR] Cannot find FastFoodPOS.exe!
    echo Please run this script from the directory containing 'dist' folder.
    echo.
    pause
    exit /b 1
)

echo [1/4] Creating installation directory...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo        Created: %INSTALL_DIR%
) else (
    echo        Directory exists. Will update existing installation.
)

echo.
echo [2/4] Copying application files...
robocopy "dist\FastFoodPOS" "%INSTALL_DIR%" /MIR /NFL /NDL /NJH /NJS /NC /NS > nul
if errorlevel 8 (
    echo [ERROR] Failed to copy files into the install directory.
    pause
    exit /b 1
)
copy /Y "uninstall.bat" "%INSTALL_DIR%\uninstall.bat" > nul
echo        Files copied successfully.

echo.
echo [3/4] Creating shortcuts...

REM Create Start Menu folder
if not exist "%START_MENU%\NSAFastFood" (
    mkdir "%START_MENU%\NSAFastFood"
)

REM Create Start Menu shortcut using PowerShell (more reliable)
powershell -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; ^
    $Shortcut = $WshShell.CreateShortcut('%START_MENU%\NSAFastFood\NSA Fast Food POS.lnk'); ^
    $Shortcut.TargetPath = '%INSTALL_DIR%\FastFoodPOS.exe'; ^
    $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; ^
    $Shortcut.IconLocation = '%INSTALL_DIR%\FastFoodPOS.exe'; ^
    $Shortcut.Save()" 2> nul

REM Create Desktop shortcut
if not exist "%DESKTOP%\NSA Fast Food.lnk" (
    powershell -Command ^
        "$WshShell = New-Object -ComObject WScript.Shell; ^
        $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\NSA Fast Food.lnk'); ^
        $Shortcut.TargetPath = '%INSTALL_DIR%\FastFoodPOS.exe'; ^
        $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; ^
        $Shortcut.IconLocation = '%INSTALL_DIR%\FastFoodPOS.exe'; ^
        $Shortcut.Save()" 2> nul
    echo        Created Desktop shortcut
)
echo        Created Start Menu shortcut

echo.
echo [4/4] Registering uninstaller information...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
    /v "DisplayName" /d "NSA Fast Food POS System" /f > nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
    /v "InstallLocation" /d "%INSTALL_DIR%" /f > nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
    /v "DisplayVersion" /d "1.2.0" /f > nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
    /v "UninstallString" /d "\"%INSTALL_DIR%\uninstall.bat\"" /f > nul 2>&1
echo        Uninstaller info registered

echo.
echo ╔═══════════════════════════════════════════╗
echo ║     ✓ Installation Complete!              ║
echo ╚═══════════════════════════════════════════╝
echo.
echo Location: %INSTALL_DIR%
echo.
echo You can now launch the application from:
echo   - Start Menu ^> NSAFastFood ^> NSA Fast Food POS
echo   - Desktop shortcut (if created)
echo.
echo Database and invoices will be stored in:
echo   %%APPDATA%%\NSAFastFood
echo.
echo To uninstall, run uninstall.bat or go to Settings ^> Apps ^> Uninstall
echo.
pause
