@echo off
setlocal enabledelayedexpansion

set "INSTALL_DIR=%LocalAppData%\Programs\NSAFastFood"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "PAYLOAD=%~dp0payload.zip"
set "APP_EXE=%INSTALL_DIR%\FastFoodPOS.exe"

for /f "usebackq delims=" %%I in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "[Environment]::GetFolderPath('Desktop')"`) do set "DESKTOP=%%I"
if not defined DESKTOP set "DESKTOP=%USERPROFILE%\Desktop"

echo ============================================
echo   NSA FAST FOOD - POS Update Installer
echo   Version 1.2.1
echo ============================================
echo.

set "DATA_DIR=%APPDATA%\NSAFastFood"
set "BACKUP_ROOT=%APPDATA%\NSAFastFood-InstallerBackups"
set "BACKUP_FILE="

if not exist "%PAYLOAD%" (
    echo [ERROR] Installer payload is missing.
    pause
    exit /b 1
)

tasklist /FI "IMAGENAME eq FastFoodPOS.exe" 2>nul | find /I /N "FastFoodPOS.exe">nul
if "%ERRORLEVEL%"=="0" (
    echo [INFO] Closing running application...
    taskkill /IM FastFoodPOS.exe /F >nul 2>&1
    for /L %%S in (1,1,20) do (
        tasklist /FI "IMAGENAME eq FastFoodPOS.exe" 2>nul | find /I /N "FastFoodPOS.exe">nul
        if errorlevel 1 goto app_closed
        timeout /t 1 /nobreak >nul
    )
    echo [ERROR] Could not stop FastFoodPOS.exe. Please close it manually and retry.
    pause
    exit /b 1
)
:app_closed

if exist "%DATA_DIR%" (
    echo [0/4] Backing up existing app data...
    if not exist "%BACKUP_ROOT%" mkdir "%BACKUP_ROOT%"
    for /f %%I in ('powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set "STAMP=%%I"
    set "BACKUP_FILE=%BACKUP_ROOT%\NSAFastFood-preinstall-!STAMP!.zip"
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path '%DATA_DIR%\*' -DestinationPath '!BACKUP_FILE!' -Force"
    if errorlevel 1 (
        echo [ERROR] Failed to back up existing data from %DATA_DIR%.
        pause
        exit /b 1
    )
)

echo [1/4] Preparing install directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [2/4] Extracting application files...
set "STAGING=%TEMP%\NSAFastFood_update_!RANDOM!!RANDOM!"
if exist "!STAGING!" rmdir /s /q "!STAGING!"
mkdir "!STAGING!" >nul 2>&1
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%PAYLOAD%' -DestinationPath '!STAGING!' -Force"
if errorlevel 1 (
    echo [ERROR] Failed to extract the application payload.
    if exist "!STAGING!" rmdir /s /q "!STAGING!"
    pause
    exit /b 1
)
robocopy "!STAGING!" "%INSTALL_DIR%" /MIR /NFL /NDL /NJH /NJS /NC /NS >nul
if errorlevel 8 (
    echo [ERROR] Failed to copy files into the install directory.
    if exist "!STAGING!" rmdir /s /q "!STAGING!"
    pause
    exit /b 1
)
if exist "!STAGING!" rmdir /s /q "!STAGING!"
copy /Y "%~dp0uninstall.bat" "%INSTALL_DIR%\uninstall.bat" >nul

echo [3/4] Creating shortcuts...
if not exist "%START_MENU%\NSAFastFood" mkdir "%START_MENU%\NSAFastFood"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\NSAFastFood\NSA Fast Food POS.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\FastFoodPOS.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\FastFoodPOS.exe'; $Shortcut.Save()" 2>nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\NSA Fast Food.lnk'); $Shortcut.TargetPath = '%APP_EXE%'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%APP_EXE%'; $Shortcut.Save()" 2>nul

echo [4/4] Registering uninstaller information...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
    /v "DisplayName" /d "NSA Fast Food POS System" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
    /v "InstallLocation" /d "%INSTALL_DIR%" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
    /v "DisplayVersion" /d "1.2.1" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood" ^
    /v "UninstallString" /d "\"%INSTALL_DIR%\uninstall.bat\"" /f >nul 2>&1

echo.
echo Installation complete.
echo App location: %INSTALL_DIR%
echo Data location: %APPDATA%\NSAFastFood
if defined BACKUP_FILE echo Data backup: %BACKUP_FILE%
echo.
pause