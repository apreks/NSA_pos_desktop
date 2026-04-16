@echo off
set "INSTALLED_EXE=%LocalAppData%\Programs\NSAFastFood\FastFoodPOS.exe"

if exist "%INSTALLED_EXE%" (
	start "" "%INSTALLED_EXE%"
) else (
	cd /d "%~dp0FastFoodPOS"
	start "" "FastFoodPOS.exe"
)
