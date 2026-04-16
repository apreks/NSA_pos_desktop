"""
Auto-updater for NSA POINT OF SALE (BlazeBite ERP).
Checks a remote version.json, prompts the user, downloads and launches the installer.
Designed to run entirely in the background — never freezes the UI, fails silently.
"""

import os
import sys
import json
import threading
import tempfile
import subprocess
import requests
import customtkinter as ctk

from version import VERSION

# ── Configuration ──────────────────────────────────────────────────
UPDATE_CHECK_URLS = [
    "https://github.com/apreks/NSA_pos_desktop/releases/latest/download/version.json",
]
REQUEST_TIMEOUT = 15  # seconds


# ── Helpers ────────────────────────────────────────────────────────

def _parse_version(v: str):
    """Convert '1.2.3' → (1, 2, 3) for comparison."""
    try:
        return tuple(int(x) for x in v.strip().split("."))
    except (ValueError, AttributeError):
        return (0, 0, 0)


def _get_settings_path():
    app_data = os.path.join(
        os.environ.get("APPDATA", os.path.expanduser("~")), "NSAFastFood"
    )
    os.makedirs(app_data, exist_ok=True)
    return os.path.join(app_data, "settings.json")


def _load_settings() -> dict:
    path = _get_settings_path()
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_settings(data: dict):
    path = _get_settings_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def _merge_and_save_setting(key: str, value):
    """Read existing settings, update one key, write back."""
    settings = _load_settings()
    settings[key] = value
    _save_settings(settings)


# ── Public API ─────────────────────────────────────────────────────

def check_for_updates(app_instance, colors: dict, is_transaction_active: bool = False):
    """
    Kick off a silent background update check.
    Call from the main thread; the network + UI work is handled internally.

    Parameters
    ----------
    app_instance : BlazeBiteApp (ctk.CTk)
        The running application window — used as parent for dialogs.
    colors : dict
        The COLORS theme dictionary from main.
    is_transaction_active : bool
        If True the check is skipped so an in-progress sale is never interrupted.
    """
    if is_transaction_active:
        return
    threading.Thread(target=_check_worker, args=(app_instance, colors), daemon=True).start()


# ── Background worker ─────────────────────────────────────────────

def _check_worker(app, colors):
    """Run on a daemon thread — fetch version info, then schedule UI on main thread."""
    try:
        info = None
        for update_url in UPDATE_CHECK_URLS:
            try:
                resp = requests.get(update_url, timeout=REQUEST_TIMEOUT)
                resp.raise_for_status()
                info = resp.json()
                break
            except Exception:
                continue

        if not info:
            return

        remote_ver = info.get("version", "")
        download_url = info.get("download_url", "")
        release_notes = info.get("release_notes", "")

        if not remote_ver or not download_url:
            return

        if _parse_version(remote_ver) <= _parse_version(VERSION):
            return  # already up to date

        # Check if user previously skipped this version
        settings = _load_settings()
        skipped = settings.get("skipped_update_version", "")
        if skipped == remote_ver:
            return

        # Schedule dialog on the main (UI) thread
        app.after(0, lambda: _show_update_dialog(app, colors, remote_ver, download_url, release_notes))

    except Exception:
        # Fail silently — no internet, server down, bad JSON, etc.
        pass


# ── Update dialog ──────────────────────────────────────────────────

def _show_update_dialog(app, colors: dict, new_version: str, download_url: str, release_notes: str):
    """Display the update-available dialog (runs on the main thread)."""
    COLORS = colors

    dlg = ctk.CTkToplevel(app)
    dlg.title("Update Available")
    dlg.geometry("480x380")
    dlg.resizable(False, False)
    dlg.configure(fg_color=COLORS["bg_dark"])
    dlg.transient(app)
    dlg.grab_set()
    dlg.lift()
    dlg.focus_force()

    # ── Header ──
    ctk.CTkLabel(
        dlg,
        text="🚀  A New Version Is Available",
        font=ctk.CTkFont("Helvetica", 20, "bold"),
        text_color=COLORS["accent"],
    ).pack(pady=(24, 6))

    # ── Version info card ──
    card = ctk.CTkFrame(dlg, fg_color=COLORS["bg_card"], corner_radius=10)
    card.pack(padx=28, pady=10, fill="x")

    ctk.CTkLabel(
        card,
        text=f"Current version:   {VERSION}",
        font=ctk.CTkFont("Helvetica", 13),
        text_color=COLORS["text_muted"],
        anchor="w",
    ).pack(padx=16, pady=(12, 2), anchor="w")

    ctk.CTkLabel(
        card,
        text=f"New version:        {new_version}",
        font=ctk.CTkFont("Helvetica", 14, "bold"),
        text_color=COLORS["text_primary"],
        anchor="w",
    ).pack(padx=16, pady=(2, 12), anchor="w")

    # ── Release notes ──
    if release_notes:
        ctk.CTkLabel(
            dlg,
            text="Release Notes",
            font=ctk.CTkFont("Helvetica", 13, "bold"),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(padx=30, pady=(6, 2), anchor="w")

        notes_frame = ctk.CTkFrame(dlg, fg_color=COLORS["bg_panel"], corner_radius=8)
        notes_frame.pack(padx=28, pady=(0, 10), fill="x")

        ctk.CTkLabel(
            notes_frame,
            text=release_notes,
            font=ctk.CTkFont("Helvetica", 12),
            text_color=COLORS["text_muted"],
            wraplength=400,
            justify="left",
            anchor="w",
        ).pack(padx=14, pady=10, anchor="w")

    # ── Buttons ──
    btn_frame = ctk.CTkFrame(dlg, fg_color="transparent")
    btn_frame.pack(padx=28, pady=(4, 20), fill="x")

    ctk.CTkButton(
        btn_frame,
        text="Update Now",
        width=140,
        height=36,
        corner_radius=8,
        font=ctk.CTkFont("Helvetica", 13, "bold"),
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_glow"],
        text_color="#0A0E27",
        command=lambda: _on_update_now(dlg, app, colors, download_url, new_version),
    ).pack(side="left", padx=(0, 8))

    ctk.CTkButton(
        btn_frame,
        text="Remind Me Later",
        width=140,
        height=36,
        corner_radius=8,
        font=ctk.CTkFont("Helvetica", 13, "bold"),
        fg_color=COLORS["bg_hover"],
        hover_color=COLORS["border"],
        text_color=COLORS["text_primary"],
        command=dlg.destroy,
    ).pack(side="left", padx=(0, 8))

    ctk.CTkButton(
        btn_frame,
        text="Skip This Version",
        width=140,
        height=36,
        corner_radius=8,
        font=ctk.CTkFont("Helvetica", 13, "bold"),
        fg_color=COLORS["bg_hover"],
        hover_color=COLORS["border"],
        text_color=COLORS["text_muted"],
        command=lambda: _on_skip_version(dlg, new_version),
    ).pack(side="left")


# ── Button callbacks ───────────────────────────────────────────────

def _on_skip_version(dlg, version: str):
    _merge_and_save_setting("skipped_update_version", version)
    dlg.destroy()


def _on_update_now(dlg, app, colors, download_url: str, new_version: str):
    dlg.destroy()
    _show_download_progress(app, colors, download_url, new_version)


# ── Download progress window ──────────────────────────────────────

def _show_download_progress(app, colors: dict, download_url: str, new_version: str):
    COLORS = colors

    state = {"cancelled": False, "thread": None}

    win = ctk.CTkToplevel(app)
    win.title("Downloading Update")
    win.geometry("440x220")
    win.resizable(False, False)
    win.configure(fg_color=COLORS["bg_dark"])
    win.transient(app)
    win.grab_set()
    win.lift()
    win.focus_force()

    ctk.CTkLabel(
        win,
        text=f"Downloading v{new_version}…",
        font=ctk.CTkFont("Helvetica", 16, "bold"),
        text_color=COLORS["text_primary"],
    ).pack(pady=(24, 8))

    progress_bar = ctk.CTkProgressBar(
        win,
        width=360,
        height=14,
        corner_radius=7,
        progress_color=COLORS["accent"],
        fg_color=COLORS["bg_card"],
    )
    progress_bar.pack(pady=(4, 6))
    progress_bar.set(0)

    status_label = ctk.CTkLabel(
        win,
        text="Starting download…",
        font=ctk.CTkFont("Helvetica", 12),
        text_color=COLORS["text_muted"],
    )
    status_label.pack(pady=(0, 10))

    cancel_btn = ctk.CTkButton(
        win,
        text="Cancel",
        width=120,
        height=34,
        corner_radius=8,
        font=ctk.CTkFont("Helvetica", 13, "bold"),
        fg_color=COLORS["bg_hover"],
        hover_color=COLORS["border"],
        text_color=COLORS["text_primary"],
        command=lambda: _cancel_download(state, win),
    )
    cancel_btn.pack(pady=(0, 16))

    # Prevent closing via the [X] button while downloading
    win.protocol("WM_DELETE_WINDOW", lambda: _cancel_download(state, win))

    t = threading.Thread(
        target=_download_worker,
        args=(app, win, download_url, progress_bar, status_label, cancel_btn, state),
        daemon=True,
    )
    state["thread"] = t
    t.start()


def _cancel_download(state: dict, win):
    state["cancelled"] = True
    try:
        win.destroy()
    except Exception:
        pass


def _download_worker(app, win, url, progress_bar, status_label, cancel_btn, state):
    """Stream-download the installer, updating the progress bar via app.after()."""
    tmp_dir = tempfile.gettempdir()
    # Derive filename from URL, fallback to generic name
    filename = url.rsplit("/", 1)[-1] if "/" in url else "POS_Setup.exe"
    # Sanitize filename
    filename = "".join(c for c in filename if c.isalnum() or c in "._-")
    if not filename:
        filename = "POS_Setup.exe"
    dest_path = os.path.join(tmp_dir, filename)

    try:
        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()

        total = int(resp.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 65536  # 64 KB

        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if state["cancelled"]:
                    # Clean up partial file
                    f.close()
                    try:
                        os.remove(dest_path)
                    except OSError:
                        pass
                    return

                f.write(chunk)
                downloaded += len(chunk)

                if total > 0:
                    pct = downloaded / total
                    mb_done = downloaded / (1024 * 1024)
                    mb_total = total / (1024 * 1024)
                    text = f"{pct:.0%}  —  {mb_done:.1f} MB / {mb_total:.1f} MB"
                else:
                    pct = 0
                    mb_done = downloaded / (1024 * 1024)
                    text = f"{mb_done:.1f} MB downloaded"

                # Schedule UI update
                app.after(0, lambda p=pct, t=text: _update_progress_ui(progress_bar, status_label, p, t))

        if state["cancelled"]:
            try:
                os.remove(dest_path)
            except OSError:
                pass
            return

        # Download complete — launch installer
        app.after(0, lambda: _launch_installer(win, dest_path))

    except Exception:
        # Fail silently — close progress window
        if not state["cancelled"]:
            app.after(0, lambda: _download_failed(win, status_label, cancel_btn))


def _update_progress_ui(progress_bar, status_label, pct, text):
    try:
        progress_bar.set(pct)
        status_label.configure(text=text)
    except Exception:
        pass


def _download_failed(win, status_label, cancel_btn):
    try:
        status_label.configure(text="Download failed. Please try again later.", text_color="#FF5757")
        cancel_btn.configure(text="Close")
    except Exception:
        try:
            win.destroy()
        except Exception:
            pass


def _launch_installer(win, installer_path: str):
    """Close the progress window, launch the installer, and exit the app."""
    try:
        win.destroy()
    except Exception:
        pass

    try:
        subprocess.Popen(
            [installer_path],
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    except Exception:
        pass

    sys.exit(0)
