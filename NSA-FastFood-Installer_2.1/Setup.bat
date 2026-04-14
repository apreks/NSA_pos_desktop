@echo off
setlocal
echo ============================================
echo   NSA FAST FOOD - POS System Setup
echo ============================================
echo.

:: Create Desktop shortcut
set "SCRIPT=%TEMP%\create_shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%SCRIPT%"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\NSA Fast Food.lnk" >> "%SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%SCRIPT%"
echo oLink.TargetPath = "%~dp0FastFoodPOS\FastFoodPOS.exe" >> "%SCRIPT%"
echo oLink.WorkingDirectory = "%~dp0FastFoodPOS" >> "%SCRIPT%"
echo oLink.Description = "NSA Fast Food POS System" >> "%SCRIPT%"
echo oLink.Save >> "%SCRIPT%"
cscript //nologo "%SCRIPT%"
del "%SCRIPT%"

echo.
echo [OK] Desktop shortcut "NSA Fast Food" created.
echo.

:: Create Start Menu shortcut
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "SCRIPT2=%TEMP%\create_startmenu.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%SCRIPT2%"
echo sLinkFile = "%STARTMENU%\NSA Fast Food.lnk" >> "%SCRIPT2%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%SCRIPT2%"
echo oLink.TargetPath = "%~dp0FastFoodPOS\FastFoodPOS.exe" >> "%SCRIPT2%"
echo oLink.WorkingDirectory = "%~dp0FastFoodPOS" >> "%SCRIPT2%"
echo oLink.Description = "NSA Fast Food POS System" >> "%SCRIPT2%"
echo oLink.Save >> "%SCRIPT2%"
cscript //nologo "%SCRIPT2%"
del "%SCRIPT2%"

echo [OK] Start Menu shortcut created.
echo.
echo ============================================
echo   Setup complete! You can now:
echo     - Double-click "NSA Fast Food" on Desktop
echo     - Or run Launch.bat from this folder
echo ============================================
echo.
pause
