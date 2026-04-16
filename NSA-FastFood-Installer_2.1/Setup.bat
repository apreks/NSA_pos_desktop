@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   NSA FAST FOOD - POS System Setup
echo   Version 1.2.0
echo ============================================
echo.

set "SOURCE_DIR=%~dp0FastFoodPOS"
set "INSTALL_DIR=%LocalAppData%\Programs\NSAFastFood"
set "DESKTOP=%USERPROFILE%\Desktop"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"

if not exist "%SOURCE_DIR%\FastFoodPOS.exe" (
	echo [ERROR] Cannot find the application files.
	pause
	exit /b 1
)

tasklist /FI "IMAGENAME eq FastFoodPOS.exe" 2>nul | find /I /N "FastFoodPOS.exe">nul
if "%ERRORLEVEL%"=="0" (
	echo [INFO] Closing running application...
	taskkill /IM FastFoodPOS.exe /F >nul 2>&1
)

echo [1/4] Preparing install directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [2/4] Copying application files...
robocopy "%SOURCE_DIR%" "%INSTALL_DIR%" /MIR /NFL /NDL /NJH /NJS /NC /NS > nul
if errorlevel 8 (
	echo [ERROR] Failed to copy files into %INSTALL_DIR%.
	pause
	exit /b 1
)
copy /Y "%~dp0Uninstall.bat" "%INSTALL_DIR%\uninstall.bat" > nul

echo [3/4] Creating shortcuts...
if not exist "%START_MENU%\NSAFastFood" mkdir "%START_MENU%\NSAFastFood"
powershell -Command ^
	"$WshShell = New-Object -ComObject WScript.Shell; ^
	$Shortcut = $WshShell.CreateShortcut('%START_MENU%\NSAFastFood\NSA Fast Food POS.lnk'); ^
	$Shortcut.TargetPath = '%INSTALL_DIR%\FastFoodPOS.exe'; ^
	$Shortcut.WorkingDirectory = '%INSTALL_DIR%'; ^
	$Shortcut.IconLocation = '%INSTALL_DIR%\FastFoodPOS.exe'; ^
	$Shortcut.Save()" 2> nul
powershell -Command ^
	"$WshShell = New-Object -ComObject WScript.Shell; ^
	$Shortcut = $WshShell.CreateShortcut('%DESKTOP%\NSA Fast Food.lnk'); ^
	$Shortcut.TargetPath = '%INSTALL_DIR%\FastFoodPOS.exe'; ^
	$Shortcut.WorkingDirectory = '%INSTALL_DIR%'; ^
	$Shortcut.IconLocation = '%INSTALL_DIR%\FastFoodPOS.exe'; ^
	$Shortcut.Save()" 2> nul

echo [4/4] Registering uninstaller information...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
	/v "DisplayName" /d "NSA Fast Food POS System" /f > nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
	/v "InstallLocation" /d "%INSTALL_DIR%" /f > nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
	/v "DisplayVersion" /d "1.2.0" /f > nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
	/v "UninstallString" /d "\"%INSTALL_DIR%\uninstall.bat\"" /f > nul 2>&1

echo.
echo [OK] Installation complete.
echo App location: %INSTALL_DIR%
echo Data location: %APPDATA%\NSAFastFood
echo.
pause
