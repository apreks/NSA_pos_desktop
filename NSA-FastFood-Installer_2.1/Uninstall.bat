@echo off
setlocal
echo ============================================
echo   NSA FAST FOOD - Uninstall
echo ============================================
echo.
echo This will remove shortcuts only.
echo Your data is stored in: %APPDATA%\NSAFastFood
echo.

set /p CONFIRM="Are you sure? (Y/N): "
if /I not "%CONFIRM%"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)

:: Remove Desktop shortcut
del "%USERPROFILE%\Desktop\NSA Fast Food.lnk" 2>nul
echo [OK] Desktop shortcut removed.

:: Remove Start Menu shortcut
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\NSA Fast Food.lnk" 2>nul
echo [OK] Start Menu shortcut removed.

echo.
echo Shortcuts removed. To fully remove the app,
echo delete this entire folder.
echo.
echo To also remove your data (transactions, products, etc.):
echo   Delete: %APPDATA%\NSAFastFood
echo.
pause
