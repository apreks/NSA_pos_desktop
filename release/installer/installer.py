import ctypes
import datetime
import json
import os
import shutil
import subprocess
import sys
import time
import winreg
import zipfile
from pathlib import Path


APP_NAME = "NSA Fast Food POS System"
APP_VERSION = "1.2.1"
INSTALL_DIR = Path(os.environ["LOCALAPPDATA"]) / "Programs" / "NSAFastFood"
APP_DATA_DIR = Path(os.environ["APPDATA"]) / "NSAFastFood"
BACKUP_DIR = Path(os.environ["APPDATA"]) / "NSAFastFood-InstallerBackups"
START_MENU_DIR = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "NSAFastFood"
START_MENU_SHORTCUT = START_MENU_DIR / "NSA Fast Food POS.lnk"
UNINSTALL_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\NSAFastFood"


def resource_path(name: str) -> Path:
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_path / name


def message_box(title: str, text: str, style: int = 0) -> None:
    ctypes.windll.user32.MessageBoxW(None, text, title, style)


def get_desktop_shortcut_path() -> Path:
    desktop_dir = Path(os.path.expandvars(r"%USERPROFILE%\Desktop"))
    try:
        desktop_dir = Path(os.path.expandvars(r"%USERPROFILE%\Desktop"))
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                "[Environment]::GetFolderPath('Desktop')",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        resolved = (result.stdout or "").strip()
        if result.returncode == 0 and resolved:
            desktop_dir = Path(resolved)
    except Exception:
        pass
    return desktop_dir / "NSA Fast Food.lnk"


def is_app_running() -> bool:
    result = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq FastFoodPOS.exe"],
        capture_output=True,
        text=True,
        check=False,
    )
    return "FastFoodPOS.exe" in (result.stdout or "")


def stop_running_app(timeout_seconds: int = 20) -> None:
    subprocess.run(
        ["taskkill", "/IM", "FastFoodPOS.exe", "/F"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if not is_app_running():
            return
        time.sleep(0.5)
    raise RuntimeError("Could not stop FastFoodPOS.exe. Please close it and retry.")


def backup_existing_data() -> Path | None:
    if not APP_DATA_DIR.exists():
        return None

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_base = BACKUP_DIR / f"NSAFastFood-preinstall-{stamp}"
    archive_path = Path(shutil.make_archive(str(archive_base), "zip", root_dir=APP_DATA_DIR))
    return archive_path


def extract_payload(payload_zip: Path) -> None:
    staging_dir = INSTALL_DIR.parent / f"{INSTALL_DIR.name}.incoming"
    if staging_dir.exists():
        shutil.rmtree(staging_dir, ignore_errors=True)
    staging_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(payload_zip, "r") as archive:
        archive.extractall(staging_dir)

    if INSTALL_DIR.exists():
        shutil.rmtree(INSTALL_DIR, ignore_errors=True)
    staging_dir.replace(INSTALL_DIR)


def install_uninstaller(uninstaller_source: Path) -> None:
    shutil.copy2(uninstaller_source, INSTALL_DIR / "uninstall.bat")


def _ps_quote(value: str) -> str:
    return value.replace("'", "''")


def create_shortcut(shortcut_path: Path, target_path: Path) -> None:
    shortcut_path.parent.mkdir(parents=True, exist_ok=True)
    powershell_script = (
        "$WshShell = New-Object -ComObject WScript.Shell; "
        f"$Shortcut = $WshShell.CreateShortcut('{_ps_quote(str(shortcut_path))}'); "
        f"$Shortcut.TargetPath = '{_ps_quote(str(target_path))}'; "
        f"$Shortcut.WorkingDirectory = '{_ps_quote(str(target_path.parent))}'; "
        f"$Shortcut.IconLocation = '{_ps_quote(str(target_path))}'; "
        "$Shortcut.Save()"
    )
    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            powershell_script,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to create shortcut: {shortcut_path}")


def register_uninstaller(uninstall_script: Path, app_version: str) -> None:
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, UNINSTALL_REG_PATH) as key:
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, APP_NAME)
        winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, str(INSTALL_DIR))
        winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, app_version)
        winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'"{uninstall_script}"')


def get_payload_version(payload_zip: Path) -> str:
    try:
        with zipfile.ZipFile(payload_zip, "r") as archive:
            with archive.open("version.json") as vf:
                info = json.loads(vf.read().decode("utf-8"))
                version = str(info.get("version", "")).strip()
                if version:
                    return version
    except Exception:
        pass
    return APP_VERSION


def launch_app(executable: Path) -> None:
    subprocess.Popen([str(executable)], close_fds=True)


def main() -> int:
    payload_zip = resource_path("payload.zip")
    uninstall_bat = resource_path("uninstall.bat")
    app_executable = INSTALL_DIR / "FastFoodPOS.exe"
    desktop_shortcut = get_desktop_shortcut_path()
    app_version = get_payload_version(payload_zip)

    if not payload_zip.exists() or not uninstall_bat.exists():
        message_box("NSA Fast Food Update", "Installer files are missing.", 0x10)
        return 1

    try:
        stop_running_app()
        backup_path = backup_existing_data()
        extract_payload(payload_zip)
        install_uninstaller(uninstall_bat)
        create_shortcut(desktop_shortcut, app_executable)
        create_shortcut(START_MENU_SHORTCUT, app_executable)
        register_uninstaller(INSTALL_DIR / "uninstall.bat", app_version)
        launch_app(app_executable)
    except Exception as exc:
        message_box("NSA Fast Food Update", f"Installation failed.\n\n{exc}", 0x10)
        return 1

    backup_note = f"\nA backup of your data was saved to:\n{backup_path}" if backup_path else ""
    message_box(
        "NSA Fast Food Update",
        f"Update installed successfully. Your existing data was preserved in {APP_DATA_DIR}.{backup_note}\n\nThe application will now reopen.",
        0x40,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())