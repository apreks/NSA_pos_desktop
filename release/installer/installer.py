import ctypes
import os
import shutil
import subprocess
import sys
import winreg
import zipfile
from pathlib import Path


APP_NAME = "NSA Fast Food POS System"
APP_VERSION = "1.2.0"
INSTALL_DIR = Path(os.environ["LOCALAPPDATA"]) / "Programs" / "NSAFastFood"
DESKTOP_SHORTCUT = Path(os.environ["USERPROFILE"]) / "Desktop" / "NSA Fast Food.lnk"
START_MENU_DIR = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "NSAFastFood"
START_MENU_SHORTCUT = START_MENU_DIR / "NSA Fast Food POS.lnk"
UNINSTALL_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood"


def resource_path(name: str) -> Path:
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_path / name


def message_box(title: str, text: str, style: int = 0) -> None:
    ctypes.windll.user32.MessageBoxW(None, text, title, style)


def stop_running_app() -> None:
    subprocess.run(
        ["taskkill", "/IM", "FastFoodPOS.exe", "/F"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def extract_payload(payload_zip: Path) -> None:
    if INSTALL_DIR.exists():
        shutil.rmtree(INSTALL_DIR, ignore_errors=True)
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(payload_zip, "r") as archive:
        archive.extractall(INSTALL_DIR)


def install_uninstaller(uninstaller_source: Path) -> None:
    shutil.copy2(uninstaller_source, INSTALL_DIR / "uninstall.bat")


def create_shortcut(shortcut_path: Path, target_path: Path) -> None:
    shortcut_path.parent.mkdir(parents=True, exist_ok=True)
    powershell_script = (
        "$WshShell = New-Object -ComObject WScript.Shell; "
        f"$Shortcut = $WshShell.CreateShortcut('{shortcut_path}'); "
        f"$Shortcut.TargetPath = '{target_path}'; "
        f"$Shortcut.WorkingDirectory = '{target_path.parent}'; "
        f"$Shortcut.IconLocation = '{target_path}'; "
        "$Shortcut.Save()"
    )
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            powershell_script,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def register_uninstaller(uninstall_script: Path) -> None:
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, UNINSTALL_REG_PATH) as key:
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, APP_NAME)
        winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, str(INSTALL_DIR))
        winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, APP_VERSION)
        winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'"{uninstall_script}"')


def launch_app(executable: Path) -> None:
    subprocess.Popen([str(executable)], close_fds=True)


def main() -> int:
    payload_zip = resource_path("payload.zip")
    uninstall_bat = resource_path("uninstall.bat")
    app_executable = INSTALL_DIR / "FastFoodPOS.exe"

    if not payload_zip.exists() or not uninstall_bat.exists():
        message_box("NSA Fast Food Update", "Installer files are missing.", 0x10)
        return 1

    try:
        stop_running_app()
        extract_payload(payload_zip)
        install_uninstaller(uninstall_bat)
        create_shortcut(DESKTOP_SHORTCUT, app_executable)
        create_shortcut(START_MENU_SHORTCUT, app_executable)
        register_uninstaller(INSTALL_DIR / "uninstall.bat")
        launch_app(app_executable)
    except Exception as exc:
        message_box("NSA Fast Food Update", f"Installation failed.\n\n{exc}", 0x10)
        return 1

    message_box(
        "NSA Fast Food Update",
        "Update installed successfully. The application will now reopen.",
        0x40,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())