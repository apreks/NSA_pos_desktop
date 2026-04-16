@echo off
setlocal enabledelayedexpansion

REM ═══════════════════════════════════════════════════════════════
REM  NSA Fast Food POS - Uninstall Script
REM ═══════════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════╗
echo ║   NSA Fast Food POS - Uninstall           ║
echo ╚═══════════════════════════════════════════╝
echo.

set "INSTALL_DIR=%LocalAppData%\Programs\NSAFastFood"
set "DESKTOP=%USERPROFILE%\Desktop"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\NSAFastFood"

REM Check if app is running
tasklist /FI "IMAGENAME eq FastFoodPOS.exe" 2>nul | find /I /N "FastFoodPOS.exe">nul
if "%ERRORLEVEL%"=="0" (
    echo [INFO] Closing running application...
    taskkill /IM FastFoodPOS.exe /F >nul 2>&1
    timeout /t 2 /nobreak >nul
)

echo Uninstalling NSA Fast Food POS...
echo.

REM Remove application files
if exist "%INSTALL_DIR%" (
    echo [1/3] Removing application files...
    rmdir /s /q "%INSTALL_DIR%"
    echo        Files removed
) else (
    echo [INFO] Installation directory not found. Skipping file removal.
)

echo.
echo [2/3] Removing shortcuts...

REM Remove Desktop shortcut
if exist "%DESKTOP%\NSA Fast Food.lnk" (
    del /f /q "%DESKTOP%\NSA Fast Food.lnk"
    echo        Removed Desktop shortcut
)

REM Remove Start Menu folder
if exist "%START_MENU%" (
    rmdir /s /q "%START_MENU%"
    echo        Removed Start Menu folder
)

echo.
echo [3/3] Cleaning up registry...

REM Remove registry entries
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" /f >nul 2>&1

echo        Registry cleaned
echo.
echo ╔═══════════════════════════════════════════╗
echo ║     ✓ Uninstall Complete!                 ║
echo ╚═══════════════════════════════════════════╝
echo.
echo [INFO] User data preserved at:
echo        %%APPDATA%%\NSAFastFood
echo.
echo To completely remove all data, delete:
echo   - C:\Users\%USERNAME%\AppData\Roaming\NSAFastFood
echo.
pause
