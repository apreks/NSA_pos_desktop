@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found at .venv\Scripts\python.exe
    echo Create it first, then run this script again.
    pause
    exit /b 1
)

echo [1/3] Activating virtual environment...
call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

echo [2/3] Ensuring PyInstaller is installed...
python -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install or update PyInstaller.
    pause
    exit /b 1
)

echo [3/3] Building executable with FastFoodPOS.spec...
python -m PyInstaller --noconfirm --clean FastFoodPOS.spec
if errorlevel 1 (
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

echo.
echo Build completed successfully.
echo Output folder:
echo %cd%\dist\FastFoodPOS
echo.
echo Copy the entire dist\FastFoodPOS folder to another Windows PC and run FastFoodPOS.exe.
pause
