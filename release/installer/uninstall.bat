@echo off
setlocal enabledelayedexpansion

set "INSTALL_DIR=%LocalAppData%\Programs\NSAFastFood"
set "DESKTOP=%USERPROFILE%\Desktop"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\NSAFastFood"

echo ============================================
echo   NSA FAST FOOD - Uninstall
echo ============================================
echo.
echo This removes the installed app and shortcuts.
echo Your data stays in: %APPDATA%\NSAFastFood
echo.

set /p CONFIRM="Are you sure? (Y/N): "
if /I not "%CONFIRM%"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)

tasklist /FI "IMAGENAME eq FastFoodPOS.exe" 2>nul | find /I /N "FastFoodPOS.exe">nul
if "%ERRORLEVEL%"=="0" taskkill /IM FastFoodPOS.exe /F >nul 2>&1

if exist "%INSTALL_DIR%" rmdir /s /q "%INSTALL_DIR%"
del "%DESKTOP%\NSA Fast Food.lnk" 2>nul
if exist "%START_MENU%" rmdir /s /q "%START_MENU%"
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" /f >nul 2>&1

echo.
echo [OK] Application files and shortcuts removed.
echo To also remove your data, delete: %APPDATA%\NSAFastFood
echo.
pause
