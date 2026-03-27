"""
╔══════════════════════════════════════════════════════════════════╗
║           BLAZEBITE FAST-FOOD ERP - Complete POS System          ║
║           Built with Python 3 + CustomTkinter + SQLite           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import sqlite3
import datetime
import os
import json
import re
import subprocess
import ctypes
from ctypes import wintypes
from tkinter import messagebox, ttk
import tkinter as tk

# ─────────────────────────────────────────────
#  APP DATA DIRECTORY SETUP
# ─────────────────────────────────────────────
def get_app_data_dir():
    """Get or create the application data directory in user's APPDATA."""
    app_data_path = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'NSAFastFood')
    if not os.path.exists(app_data_path):
        os.makedirs(app_data_path, exist_ok=True)
    return app_data_path

# ─────────────────────────────────────────────
#  APP SETTINGS
# ─────────────────────────────────────────────
APP_NAME = "NSA FAST FOOD"
TAX_RATE = 0.00 # No tax for fast food in this scenario
DB_FILE = os.path.join(get_app_data_dir(), "blazebite.db")
SETTINGS_FILE = os.path.join(get_app_data_dir(), "settings.json")
ADMIN_PASSWORD = "admin123"

# ─────────────────────────────────────────────
#  COLOUR PALETTE  (Modern, Fluid, Vibrant)
# ─────────────────────────────────────────────
COLORS = {
    "bg_dark":      "#0A0E27",        # Deep navy-blue
    "bg_panel":     "#0F1629",        # Panel background
    "bg_card":      "#151D3B",        # Card background with depth
    "bg_hover":     "#1A2447",        # Smooth hover state
    "accent":       "#00D9FF",        # Vibrant cyan (primary)
    "accent_soft":  "#00B8D4",        # Softer cyan
    "accent_glow":  "#00EAFF",        # Glowing cyan
    "gold":         "#FFD60A",        # Warm gold accent
    "text_primary": "#FFFFFF",        # Pure white
    "text_secondary":"#B0B8C8",       # Light gray-blue
    "text_muted":   "#7A8396",        # Muted gray
    "success":      "#10B981",        # Emerald green
    "warning":      "#F59E0B",        # Amber
    "error":        "#FF5757",        # Coral red
    "border":       "#2D3E5F",        # Subtle border
}

# ─────────────────────────────────────────────
#  MENU DATA
# ─────────────────────────────────────────────
MENU = {
    "🍔 Pastries": [
        {"name": "Classic Smash",     "price": 139.35,  "desc": "Double patty, cheddar, pickles"},
        {"name": "BBQ Blaze",         "price": 162.60, "desc": "Smoky BBQ, crispy onions, bacon"},
        {"name": "Spicy Inferno",     "price": 170.35, "desc": "Ghost pepper sauce, jalapeños"},
        {"name": "Mushroom Swiss",    "price": 154.85,  "desc": "Sautéed mushrooms, swiss cheese"},
        {"name": "Veggie Stack",      "price": 131.60,  "desc": "Black bean patty, avocado, pico"},
        {"name": "Triple Threat",     "price": 216.85, "desc": "Three patties, special sauce"},
    ],
    "🍟 Sides": [
        {"name": "Crispy Fries",      "price": 54.10,  "desc": "Golden, seasoned shoestring fries"},
        {"name": "Loaded Fries",      "price": 92.85,  "desc": "Cheese, bacon bits, jalapeños"},
        {"name": "Onion Rings",       "price": 61.85,  "desc": "Beer-battered, dipping sauce"},
        {"name": "Coleslaw",          "price": 38.60,  "desc": "Creamy house-made slaw"},
        {"name": "Corn Dog",          "price": 46.35,  "desc": "Classic beef frank, honey mustard"},
        {"name": "Mozzarella Sticks", "price": 69.60,  "desc": "6 sticks, marinara dip"},
    ],
    "🥤 Drinks": [
        {"name": "Cola",              "price": 35.50,  "desc": "Large fountain, free refills"},
        {"name": "Lemonade",          "price": 43.25,  "desc": "Fresh-squeezed, mint"},
        {"name": "Milkshake",         "price": 85.10,  "desc": "Vanilla, Choco, or Strawberry"},
        {"name": "Iced Coffee",       "price": 61.85,  "desc": "Cold brew, oat milk"},
        {"name": "Water",             "price": 15.50,  "desc": "Chilled still water"},
        {"name": "Root Beer Float",   "price": 69.60,  "desc": "Vanilla ice cream, root beer"},
    ],
    "🍨 Desserts": [
        {"name": "Churros (3)",       "price": 61.85,  "desc": "Cinnamon sugar, chocolate dip"},
        {"name": "Brownie Bite",      "price": 46.35,  "desc": "Warm fudge brownie, scoop of ice cream"},
        {"name": "Apple Pie Slice",   "price": 54.10,  "desc": "Flaky crust, cinnamon filling"},
        {"name": "Ice Cream Cone",    "price": 38.60,  "desc": "Soft serve, choice of flavor"},
    ],
}

COLD_STORE_MENU = {
    "🥩 Meat": [
        {"name": "Fresh Chicken",     "price": 450.00, "desc": "Whole chicken, farm fresh"},
        {"name": "Beef Cuts",        "price": 620.00, "desc": "Assorted steaks & roasts"},
        {"name": "Pork Shoulder",    "price": 510.00, "desc": "Great for slow cooking"},
    ],
    "🥚 Eggs": [
        {"name": "Farm Eggs (dozen)","price": 95.00,  "desc": "Free-range, grade A"},
        {"name": "Quail Eggs (dozen)","price": 120.00, "desc": "Rich flavor, gourmet"},
    ],
    "🍗 Poultry": [
        {"name": "Turkey Breast",     "price": 520.00, "desc": "Lean & tender"},
        {"name": "Duck Legs",        "price": 580.00, "desc": "Rich flavor, perfect for roasting"},
    ],
}

STORE_MENUS = {
    "fast_food": MENU,
    "cold_store": COLD_STORE_MENU,
}

STORE_LABELS = {
    "fast_food": "Fast Food",
    "cold_store": "Cold Store",
}

# Simple credential store for attendant/admin access per store
CREDENTIALS = {
    "fast_food": {
        "attendant": {"user": "ff_attendant", "pass": "ff_pass"},
        "admin":     {"user": "ff_admin",     "pass": "admin123"},
    },
    "cold_store": {
        "attendant": {"user": "cs_attendant", "pass": "cs_pass"},
        "admin":     {"user": "cs_admin",     "pass": "admin123"},
    },
}

# ══════════════════════════════════════════════════════════════════
#  DATABASE LAYER
# ══════════════════════════════════════════════════════════════════
class Database:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                date          TEXT    NOT NULL,
                time          TEXT    NOT NULL,
                items_json    TEXT    NOT NULL,
                subtotal      REAL    NOT NULL,
                tax           REAL    NOT NULL,
                total         REAL    NOT NULL,
                payment_method TEXT   NOT NULL,
                order_number  INTEGER NOT NULL
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT    NOT NULL,
                name     TEXT    NOT NULL,
                price    REAL    NOT NULL,
                desc     TEXT,
                quantity INTEGER DEFAULT 0
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                store    TEXT    NOT NULL,
                role     TEXT    NOT NULL,
                username TEXT    NOT NULL,
                password TEXT    NOT NULL
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp     TEXT    NOT NULL,
                actor_username TEXT   NOT NULL,
                actor_role    TEXT    NOT NULL,
                action        TEXT    NOT NULL,
                target        TEXT    NOT NULL,
                details       TEXT    NOT NULL,
                store         TEXT    NOT NULL
            )
        """)
        self.conn.commit()

        # Ensure schema has store information for filtering by POS
        self._ensure_column("transactions", "store", "TEXT", default="fast_food")
        self._ensure_column("products", "store", "TEXT", default="fast_food")
        self._ensure_column("products", "quantity", "INTEGER", default=0)
        self._ensure_column("users", "disabled", "INTEGER", default=0)

    def _has_column(self, table: str, column: str) -> bool:
        cur = self.conn.execute(f"PRAGMA table_info({table})")
        return any(row[1] == column for row in cur.fetchall())

    def _ensure_column(self, table: str, column: str, col_type: str, default=None):
        if not self._has_column(table, column):
            if default is not None:
                # SQLite will set existing rows to the default value when adding a column.
                # Use literal insertion because SQLite does not support parameter binding here.
                safe_default = str(default).replace("'", "''")
                self.conn.execute(
                    f"ALTER TABLE {table} ADD COLUMN {column} {col_type} DEFAULT '{safe_default}'"
                )
            else:
                self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
            self.conn.commit()

    def save_transaction(self, items: list, subtotal: float, tax: float,
                         total: float, payment_method: str, order_number: int, store: str = "fast_food"):
        now = datetime.datetime.now()
        self.conn.execute("""
            INSERT INTO transactions
            (date, time, items_json, subtotal, tax, total, payment_method, order_number, store)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            json.dumps(items),
            round(subtotal, 2),
            round(tax, 2),
            round(total, 2),
            payment_method,
            order_number,
            store,
        ))
        self.conn.commit()

    def get_all_transactions(self, store: str | None = None):
        if store:
            cur = self.conn.execute(
                "SELECT * FROM transactions WHERE store = ? ORDER BY id DESC",
                (store,),
            )
        else:
            cur = self.conn.execute("SELECT * FROM transactions ORDER BY id DESC")
        return cur.fetchall()

    def get_transactions_by_date_range(self, date_from: str, date_to: str,
                                       store: str | None = None):
        """Return transactions whose date falls within [date_from, date_to] (ISO strings)."""
        if store:
            cur = self.conn.execute(
                "SELECT * FROM transactions WHERE date >= ? AND date <= ? AND store = ? ORDER BY id DESC",
                (date_from, date_to, store),
            )
        else:
            cur = self.conn.execute(
                "SELECT * FROM transactions WHERE date >= ? AND date <= ? ORDER BY id DESC",
                (date_from, date_to),
            )
        return cur.fetchall()

    def get_today_summary(self, store: str | None = None):
        today = datetime.date.today().isoformat()
        if store:
            cur = self.conn.execute("""
                SELECT COUNT(*), COALESCE(SUM(total),0)
                FROM transactions WHERE date = ? AND store = ?
            """, (today, store))
        else:
            cur = self.conn.execute("""
                SELECT COUNT(*), COALESCE(SUM(total),0)
                FROM transactions WHERE date = ?
            """, (today,))
        return cur.fetchone()

    def get_daily_totals(self, limit=7, store: str | None = None):
        if store:
            cur = self.conn.execute("""
                SELECT date, COUNT(*), COALESCE(SUM(total),0)
                FROM transactions
                WHERE store = ?
                GROUP BY date
                ORDER BY date DESC
                LIMIT ?
            """, (store, limit))
        else:
            cur = self.conn.execute("""
                SELECT date, COUNT(*), COALESCE(SUM(total),0)
                FROM transactions
                GROUP BY date
                ORDER BY date DESC
                LIMIT ?
            """, (limit,))
        return cur.fetchall()

    def get_top_items(self, limit=5, store: str | None = None):
        """Parse JSON items and rank by frequency."""
        if store:
            rows = self.conn.execute(
                "SELECT items_json FROM transactions WHERE store = ?",
                (store,),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT items_json FROM transactions"
            ).fetchall()
        counts = {}
        for (items_json,) in rows:
            for item in json.loads(items_json):
                n = item["name"]
                counts[n] = counts.get(n, 0) + item["qty"]
        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:limit]

    def get_all_products(self, store: str | None = None):
        if store:
            cur = self.conn.execute(
                "SELECT * FROM products WHERE store = ? ORDER BY category, name",
                (store,),
            )
        else:
            cur = self.conn.execute("SELECT * FROM products ORDER BY store, category, name")
        return cur.fetchall()

    def add_product(self, category, name, price, desc, quantity: int = 0, store: str = "fast_food"):
        self.conn.execute(
            "INSERT INTO products (category, name, price, desc, quantity, store) VALUES (?, ?, ?, ?, ?, ?)",
            (category, name, price, desc, quantity, store),
        )
        self.conn.commit()

    def update_product(self, id, category, name, price, desc, quantity: int = 0, store: str = "fast_food"):
        self.conn.execute(
            "UPDATE products SET category=?, name=?, price=?, desc=?, quantity=?, store=? WHERE id=?",
            (category, name, price, desc, quantity, store, id),
        )
        self.conn.commit()

    def get_user(self, store: str, role: str):
        cur = self.conn.execute(
            "SELECT id, username, password FROM users WHERE store=? AND role=?",
            (store, role),
        )
        return cur.fetchone()

    def authenticate_user(self, store: str, role: str, username: str, password: str):
        if role == "root_admin":
            cur = self.conn.execute(
                """
                SELECT id, store, role, username
                FROM users
                WHERE role=? AND username=? AND password=? AND COALESCE(disabled,0)=0
                LIMIT 1
                """,
                ("root_admin", username, password),
            )
        else:
            cur = self.conn.execute(
                """
                SELECT id, store, role, username
                FROM users
                WHERE store=? AND role=? AND username=? AND password=? AND COALESCE(disabled,0)=0
                LIMIT 1
                """,
                (store, role, username, password),
            )
        return cur.fetchone()

    def get_users(self, store: str):
        cur = self.conn.execute(
            "SELECT id, role, username, password FROM users WHERE store=? ORDER BY role",
            (store,),
        )
        return cur.fetchall()

    def get_all_users(self):
        cur = self.conn.execute(
            """
            SELECT id, store, role, username, COALESCE(disabled,0)
            FROM users
            ORDER BY store, role, username
            """
        )
        return cur.fetchall()

    def add_or_update_user(self, store: str, role: str, username: str, password: str, create_if_missing: bool = False):
        existing = self.get_user(store, role)
        if existing:
            self.conn.execute(
                "UPDATE users SET username=?, password=? WHERE id=?",
                (username, password, existing[0]),
            )
        elif create_if_missing:
            self.conn.execute(
                "INSERT INTO users (store, role, username, password) VALUES (?, ?, ?, ?)",
                (store, role, username, password),
            )
        else:
            raise ValueError("User does not exist")
        self.conn.commit()

    def delete_user(self, id):
        self.conn.execute("DELETE FROM users WHERE id=?", (id,))
        self.conn.commit()

    def add_user(self, store: str, role: str, username: str, password: str):
        self.conn.execute(
            "INSERT INTO users (store, role, username, password, disabled) VALUES (?, ?, ?, ?, 0)",
            (store, role, username, password),
        )
        self.conn.commit()

    def set_user_disabled(self, user_id: int, disabled: bool):
        self.conn.execute(
            "UPDATE users SET disabled=? WHERE id=?",
            (1 if disabled else 0, user_id),
        )
        self.conn.commit()

    def log_activity(self, actor_username: str, actor_role: str, action: str,
                     target: str = "", details: str = "", store: str = "system"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute(
            """
            INSERT INTO activities
            (timestamp, actor_username, actor_role, action, target, details, store)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (now, actor_username, actor_role, action, target, details, store),
        )
        self.conn.commit()

    def get_activity_logs(self, limit: int = 300):
        cur = self.conn.execute(
            """
            SELECT id, timestamp, actor_username, actor_role, action, target, details, store
            FROM activities
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return cur.fetchall()

    def get_item_report(self, item_name: str, date_from: str, date_to: str,
                        store: str | None = None):
        """Return (total_qty, total_revenue) for a named item between two ISO dates."""
        if store:
            rows = self.conn.execute(
                "SELECT items_json FROM transactions WHERE date >= ? AND date <= ? AND store = ?",
                (date_from, date_to, store),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT items_json FROM transactions WHERE date >= ? AND date <= ?",
                (date_from, date_to),
            ).fetchall()
        total_qty = 0
        total_rev = 0.0
        for (items_json,) in rows:
            for it in json.loads(items_json):
                if it["name"].strip().lower() == item_name.strip().lower():
                    total_qty += it["qty"]
                    total_rev += it["price"] * it["qty"]
        return total_qty, total_rev

    def get_all_item_names(self, store: str | None = None) -> list[str]:
        """Return sorted unique item names from all transactions."""
        if store:
            rows = self.conn.execute(
                "SELECT items_json FROM transactions WHERE store = ?", (store,)
            ).fetchall()
        else:
            rows = self.conn.execute("SELECT items_json FROM transactions").fetchall()
        names = set()
        for (items_json,) in rows:
            for it in json.loads(items_json):
                names.add(it["name"])
        return sorted(names)

    def delete_product(self, id):
        self.conn.execute("DELETE FROM products WHERE id=?", (id,))
        self.conn.commit()

    def initialize_products(self):
        """Ensure all products and default users exist.

        This method is safe to run on every startup and will only insert
        missing rows.
        """
        for store_key, menu in STORE_MENUS.items():
            for cat, items in menu.items():
                for item in items:
                    exists = self.conn.execute(
                        "SELECT 1 FROM products WHERE name=? AND category=? AND store=?",
                        (item["name"], cat, store_key),
                    ).fetchone()
                    if not exists:
                        self.add_product(cat, item["name"], item["price"], item["desc"], store=store_key)

        # Create default users if missing
        for store_key, creds in CREDENTIALS.items():
            for role, info in creds.items():
                self.add_or_update_user(store_key, role, info["user"], info["pass"], create_if_missing=True)

        # Global root-admin account for system-wide operations
        self.add_or_update_user("system", "root_admin", "root_admin", "root123", create_if_missing=True)



# ══════════════════════════════════════════════════════════════════
#  DATE PICKER POPUP  (pure CTk / tkinter – no extra library needed)
# ══════════════════════════════════════════════════════════════════
class DatePickerPopup(ctk.CTkToplevel):
    """A lightweight calendar popup that returns a selected date as YYYY-MM-DD."""

    _DAY_ABBRS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    def __init__(self, parent, callback, initial_date=None):
        super().__init__(parent)
        self._callback = callback

        # Start from today or supplied date
        if initial_date:
            try:
                d = datetime.date.fromisoformat(initial_date)
            except ValueError:
                d = datetime.date.today()
        else:
            d = datetime.date.today()

        self._year  = d.year
        self._month = d.month
        self._sel   = d                # currently highlighted date

        self.title("Select Date")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=COLORS["bg_dark"])
        self.geometry("310x290")
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width()  // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"310x290+{pw - 155}+{ph - 145}")

        self._build()
        self.focus_force()

    # ── Layout ──────────────────────────────────────────────────
    def _build(self):
        # Navigation row
        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(fill="x", padx=10, pady=(12, 6))

        ctk.CTkButton(nav, text="◀", width=32, height=30, corner_radius=6,
                      fg_color=COLORS["bg_hover"], hover_color=COLORS["border"],
                      text_color=COLORS["text_primary"],
                      font=ctk.CTkFont("Helvetica", 13, "bold"),
                      command=self._prev_month).pack(side="left")

        self._month_lbl = ctk.CTkLabel(nav, text="",
                                        font=ctk.CTkFont("Helvetica", 13, "bold"),
                                        text_color=COLORS["text_primary"])
        self._month_lbl.pack(side="left", expand=True)

        ctk.CTkButton(nav, text="▶", width=32, height=30, corner_radius=6,
                      fg_color=COLORS["bg_hover"], hover_color=COLORS["border"],
                      text_color=COLORS["text_primary"],
                      font=ctk.CTkFont("Helvetica", 13, "bold"),
                      command=self._next_month).pack(side="right")

        # Day-of-week headers
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=10)
        for abbr in self._DAY_ABBRS:
            ctk.CTkLabel(hdr, text=abbr, width=38, height=24,
                         font=ctk.CTkFont("Helvetica", 10, "bold"),
                         text_color=COLORS["text_muted"]).pack(side="left")

        # Day grid container
        self._grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._grid_frame.pack(fill="both", expand=True, padx=10, pady=(2, 8))

        # Today button
        ctk.CTkButton(self, text="Today", height=30, corner_radius=6,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_glow"],
                      text_color="white", font=ctk.CTkFont("Helvetica", 11, "bold"),
                      command=self._select_today).pack(fill="x", padx=10, pady=(0, 10))

        self._draw_grid()

    def _draw_grid(self):
        for w in self._grid_frame.winfo_children():
            w.destroy()

        self._month_lbl.configure(
            text=datetime.date(self._year, self._month, 1).strftime("%B  %Y")
        )

        import calendar
        first_wd, days_in_month = calendar.monthrange(self._year, self._month)
        today = datetime.date.today()

        col = first_wd  # 0=Mon … 6=Sun
        # Fill blank cells before the 1st
        for _ in range(first_wd):
            ctk.CTkLabel(self._grid_frame, text="", width=38, height=32).grid(
                row=0, column=_)

        row = 0
        for day in range(1, days_in_month + 1):
            d = datetime.date(self._year, self._month, day)
            is_today = (d == today)
            is_sel   = (d == self._sel)

            if is_sel:
                fg   = COLORS["accent"]
                htxt = COLORS["text_primary"]
            elif is_today:
                fg   = COLORS["success"]
                htxt = "white"
            else:
                fg   = COLORS["bg_hover"]
                htxt = COLORS["text_primary"]

            btn = ctk.CTkButton(
                self._grid_frame, text=str(day),
                width=38, height=32, corner_radius=6,
                fg_color=fg,
                hover_color=COLORS["accent_glow"],
                text_color=htxt,
                font=ctk.CTkFont("Helvetica", 11),
                command=lambda d=d: self._pick(d),
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
            col += 1
            if col == 7:
                col = 0
                row += 1

    def _prev_month(self):
        if self._month == 1:
            self._month = 12
            self._year -= 1
        else:
            self._month -= 1
        self._draw_grid()

    def _next_month(self):
        if self._month == 12:
            self._month = 1
            self._year += 1
        else:
            self._month += 1
        self._draw_grid()

    def _pick(self, date: datetime.date):
        self._sel = date
        self._draw_grid()
        self.after(120, lambda: [self._callback(date.isoformat()), self.destroy()])

    def _select_today(self):
        today = datetime.date.today()
        self._year  = today.year
        self._month = today.month
        self._sel   = today
        self._draw_grid()
        self.after(120, lambda: [self._callback(today.isoformat()), self.destroy()])


# ══════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════
class BlazeBiteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ── Window setup ──
        self.title(f"{APP_NAME}  —  Point of Sale System")
        self.geometry("1500x860")
        self.minsize(1300, 750)
        self.configure(fg_color=COLORS["bg_dark"])

        # Performance optimizations
        self.resizable(True, True)
        self.attributes("-alpha", 1.0)  # Ensure full opacity for better performance

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # ── State ──
        self.db = Database(DB_FILE)
        self.db.initialize_products()
        self.active_store = None
        self.current_role = None  # 'attendant' or 'admin'
        self.current_user = None
        self.root_logged_in = False
        self.menu_data = {}
        self.order_items: dict[str, dict] = {}   # name -> {price, qty, desc}
        self.order_counter = 1001
        self.active_category = None
        self.receipt_paper_profile = "Auto"  # Auto | 80mm | 58mm
        self._load_app_settings()

        # ── Build UI ──
        self._build_layout()

        # Show login immediately
        self._show_login()

    # ─────────────────────────────────────────
    #  LAYOUT SKELETON
    # ─────────────────────────────────────────
    def _load_app_settings(self):
        """Load persisted app settings from disk."""
        try:
            if not os.path.exists(SETTINGS_FILE):
                return
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            profile = str(data.get("receipt_paper_profile", "Auto")).strip()
            if profile in ("Auto", "80mm", "58mm"):
                self.receipt_paper_profile = profile
        except Exception:
            # Keep defaults when settings are missing/corrupt.
            self.receipt_paper_profile = "Auto"

    def _save_app_settings(self):
        """Persist app settings to disk."""
        try:
            data = {
                "receipt_paper_profile": self.receipt_paper_profile,
            }
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def _on_receipt_profile_changed(self, value: str | None = None):
        selected = (value or "").strip()
        if selected not in ("Auto", "80mm", "58mm"):
            selected = "Auto"

        self.receipt_paper_profile = selected

        if hasattr(self, "admin_receipt_profile_var") and self.admin_receipt_profile_var.get() != selected:
            self.admin_receipt_profile_var.set(selected)
        if hasattr(self, "root_receipt_profile_var") and self.root_receipt_profile_var.get() != selected:
            self.root_receipt_profile_var.set(selected)

        self._save_app_settings()

    def _build_layout(self):
        # Top bar
        self._build_topbar()

        # Tab switcher (POS  |  Admin)
        self.tab_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_panel"],
                                      corner_radius=0, height=46)
        self.tab_frame.pack(fill="x")
        self._build_tabs()

        # Content area
        self.content = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"], corner_radius=0)
        self.content.pack(fill="both", expand=True)

        # Build both views (only one visible at a time)
        self.pos_view  = ctk.CTkFrame(self.content, fg_color=COLORS["bg_dark"], corner_radius=0)
        self.admin_view= ctk.CTkFrame(self.content, fg_color=COLORS["bg_dark"], corner_radius=0)
        self.root_view = ctk.CTkFrame(self.content, fg_color=COLORS["bg_dark"], corner_radius=0)

        self._build_pos_view(self.pos_view)
        self._build_admin_view(self.admin_view)
        self._build_root_admin_view(self.root_view)

        self._show_view("pos")

    def _build_topbar(self):
        bar = ctk.CTkFrame(self, fg_color=COLORS["bg_panel"],
                           corner_radius=0, height=70, border_width=1,
                           border_color=COLORS["border"])
        bar.pack(fill="x")
        bar.pack_propagate(False)

        # Logo
        ctk.CTkLabel(bar, text=APP_NAME,
                     font=ctk.CTkFont("Helvetica", 28, "bold"),
                     text_color=COLORS["accent_glow"]).pack(side="left", padx=24, pady=14)

        # ── Right-side container (stable pack order) ──
        rbox = ctk.CTkFrame(bar, fg_color="transparent")
        rbox.pack(side="right", fill="y")

        # Clock (rightmost)
        self.clock_lbl = ctk.CTkLabel(rbox, text="",
                                      font=ctk.CTkFont("Helvetica", 12),
                                      text_color=COLORS["text_secondary"])
        self.clock_lbl.pack(side="right", padx=20, pady=14)
        self._tick_clock()

        # Logout button
        self.topbar_logout_btn = ctk.CTkButton(
            rbox, text="🚪  Logout",
            width=110, height=36, corner_radius=8,
            fg_color=COLORS["error"], hover_color="#DC2626",
            text_color="white",
            font=ctk.CTkFont("Helvetica", 11, "bold"),
            command=self._logout_admin,
            state="disabled",
        )
        self.topbar_logout_btn.pack(side="right", padx=(0, 6), pady=17)

        # User profile pill
        self.topbar_user_btn = ctk.CTkButton(
            rbox, text="  👤  Not signed in",
            width=200, height=36, corner_radius=18,
            fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
            border_width=1, border_color=COLORS["border"],
            text_color=COLORS["text_muted"],
            font=ctk.CTkFont("Helvetica", 11),
            command=self._show_profile_dialog,
            anchor="center",
        )
        self.topbar_user_btn.pack(side="right", padx=(4, 6), pady=17)

        # Separator
        ctk.CTkFrame(rbox, width=1, height=36, fg_color=COLORS["border"]).pack(
            side="right", padx=10, pady=17
        )

        # Order badge
        self.order_badge = ctk.CTkLabel(
            rbox,
            text=f"Order  # {self.order_counter:04d}",
            font=ctk.CTkFont("Helvetica", 13, "bold"),
            text_color=COLORS["gold"],
        )
        self.order_badge.pack(side="right", padx=20, pady=14)


    def _build_tabs(self):
        self.active_tab = "pos"
        self.tab_buttons = {}

        # POS tab
        pos_btn = ctk.CTkButton(
            self.tab_frame, text="🧾  Point of Sale",
            width=200, height=46, corner_radius=0,
            fg_color="transparent",
            hover_color=COLORS["bg_hover"],
            text_color=COLORS["text_primary"],
            font=ctk.CTkFont("Helvetica", 13, "bold"),
            command=lambda: self._show_view("pos"),
        )
        pos_btn.pack(side="left")
        self.tab_buttons["pos"] = pos_btn

        # Admin tab
        admin_btn = ctk.CTkButton(
            self.tab_frame, text="📊  Admin Dashboard",
            width=200, height=46, corner_radius=0,
            fg_color="transparent",
            hover_color=COLORS["bg_hover"],
            text_color=COLORS["text_primary"],
            font=ctk.CTkFont("Helvetica", 13, "bold"),
            command=self._check_admin_access,
        )
        admin_btn.pack(side="left")
        self.tab_buttons["admin"] = admin_btn

        # Root admin tab
        root_btn = ctk.CTkButton(
            self.tab_frame, text="🛡️  Root Admin",
            width=180, height=46, corner_radius=0,
            fg_color="transparent",
            hover_color=COLORS["bg_hover"],
            text_color=COLORS["text_primary"],
            font=ctk.CTkFont("Helvetica", 13, "bold"),
            command=self._check_root_admin_access,
        )
        root_btn.pack(side="left")
        self.tab_buttons["root"] = root_btn

        self._apply_role_permissions()

    def _apply_role_permissions(self):
        # Disable admin tab unless logged in as admin
        admin_btn = self.tab_buttons.get("admin")
        root_btn = self.tab_buttons.get("root")
        if not admin_btn:
            return
        if getattr(self, "current_role", None) == "admin":
            admin_btn.configure(state="normal")
        else:
            admin_btn.configure(state="disabled")

        if root_btn:
            if getattr(self, "current_role", None) == "root_admin":
                root_btn.configure(state="normal")
            else:
                root_btn.configure(state="disabled")

        # Update topbar user pill and logout button
        role = getattr(self, "current_role", None)
        user = getattr(self, "current_user", None)
        if hasattr(self, "topbar_user_btn") and hasattr(self, "topbar_logout_btn"):
            if user and role:
                role_display = {
                    "admin": "Admin",
                    "root_admin": "Root Admin",
                    "attendant": "Attendant",
                }.get(role, role.replace("_", " ").title())
                pill_border = {
                    "admin": COLORS["accent"],
                    "root_admin": COLORS["gold"],
                    "attendant": COLORS["success"],
                }.get(role, COLORS["border"])
                initial = user[0].upper()
                self.topbar_user_btn.configure(
                    text=f"  {initial}  {user}  ·  {role_display}",
                    border_color=pill_border,
                    text_color=COLORS["text_primary"],
                )
                self.topbar_logout_btn.configure(state="normal")
            else:
                self.topbar_user_btn.configure(
                    text="  👤  Not signed in",
                    border_color=COLORS["border"],
                    text_color=COLORS["text_muted"],
                )
                self.topbar_logout_btn.configure(state="disabled")

    def _show_view(self, which: str):
        self.active_tab = which
        if which == "pos":
            self.admin_view.pack_forget()
            self.root_view.pack_forget()
            self.pos_view.pack(fill="both", expand=True)
        elif which == "admin":
            self.pos_view.pack_forget()
            self.root_view.pack_forget()
            self.admin_view.pack(fill="both", expand=True)
            self._refresh_admin()
        else:
            self.pos_view.pack_forget()
            self.admin_view.pack_forget()
            self.root_view.pack(fill="both", expand=True)
            self._refresh_root_admin()

    # ─────────────────────────────────────────
    #  POS VIEW
    # ─────────────────────────────────────────
    def _build_pos_view(self, parent):
        parent.columnconfigure(0, weight=3)
        parent.columnconfigure(1, weight=2)
        parent.rowconfigure(0, weight=1)

        # Left: menu panel
        left = ctk.CTkFrame(parent, fg_color=COLORS["bg_dark"], corner_radius=0)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,1))
        self._build_menu_panel(left)

        # Right: order panel
        right = ctk.CTkFrame(parent, fg_color=COLORS["bg_panel"], corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew")
        self._build_order_panel(right)

    # ── Category tabs ──
    def _build_menu_panel(self, parent):
        # Search frame
        search_frame = ctk.CTkFrame(parent, fg_color=COLORS["bg_panel"],
                                   corner_radius=0, height=56, border_width=1,
                                   border_color=COLORS["border"])
        search_frame.pack(fill="x")
        search_frame.pack_propagate(False)

        # Search entry
        search_label = ctk.CTkLabel(search_frame, text="🔍 Search:",
                                   font=ctk.CTkFont("Helvetica", 11),
                                   text_color=COLORS["text_secondary"])
        search_label.pack(side="left", padx=10, pady=8)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var,
                                         width=200, height=36, corner_radius=8,
                                         fg_color=COLORS["bg_hover"],
                                         border_color=COLORS["border"],
                                         placeholder_text="Search items...",
                                         font=ctk.CTkFont("Helvetica", 11))
        self.search_entry.pack(side="left", padx=5, pady=8)
        self.search_entry.bind("<Return>", lambda _: self._perform_search())

        # Search button
        search_btn = ctk.CTkButton(search_frame, text="Search",
                                  width=80, height=36, corner_radius=8,
                                  fg_color=COLORS["success"],
                                  hover_color="#059669",
                                  text_color="white",
                                  font=ctk.CTkFont("Helvetica", 11, "bold"),
                                  command=self._perform_search)
        search_btn.pack(side="left", padx=5, pady=8)

        # Clear search button
        clear_btn = ctk.CTkButton(search_frame, text="Clear",
                                 width=70, height=36, corner_radius=8,
                                 fg_color=COLORS["bg_hover"],
                                 hover_color=COLORS["border"],
                                 text_color=COLORS["text_secondary"],
                                 font=ctk.CTkFont("Helvetica", 11),
                                 command=self._clear_search)
        clear_btn.pack(side="left", padx=2, pady=8)

        # Category tab bar
        self.cat_bar = ctk.CTkFrame(parent, fg_color=COLORS["bg_panel"],
                               corner_radius=0, height=56, border_width=1,
                               border_color=COLORS["border"])
        self.cat_bar.pack(fill="x")
        self.cat_bar.pack_propagate(False)

        self.cat_buttons = {}
        self.category_frames = {}  # Cache frames per category for responsiveness
        self.search_active = False  # Track if we're viewing search results
        self.search_results = []  # Store search results
        self._refresh_category_buttons()

        # Scrollable item grid
        self.menu_scroll = ctk.CTkScrollableFrame(
            parent, fg_color=COLORS["bg_dark"], corner_radius=0,
            scrollbar_button_color=COLORS["border"],
        )
        self.menu_scroll.pack(fill="both", expand=True, padx=8, pady=8)

    def _refresh_category_buttons(self):
        # Rebuild category tab buttons for the active store
        for w in self.cat_bar.winfo_children():
            w.destroy()
        self.cat_buttons = {}
        for cat in self.menu_data.keys():
            btn = ctk.CTkButton(
                self.cat_bar, text=cat,
                width=150, height=50, corner_radius=0,
                fg_color="transparent",
                hover_color=COLORS["bg_hover"],
                text_color=COLORS["text_secondary"],
                font=ctk.CTkFont("Helvetica", 12, "bold"),
                command=lambda c=cat: self._select_category(c),
            )
            btn.pack(side="left", padx=2, pady=3)
            self.cat_buttons[cat] = btn

    def _select_category(self, cat: str):
        if cat is None or cat == self.active_category:
            return
        # Clear search when selecting a category
        self.search_var.set("")
        self.search_active = False
        self.search_results = []

        self.active_category = cat
        for c, btn in self.cat_buttons.items():
            if c == cat:
                btn.configure(
                    fg_color=COLORS["accent"],
                    text_color=COLORS["text_primary"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_secondary"],
                )
        self._render_category(cat)

    def _select_store(self, store_label: str):
        # Map the UI label back to the store key
        store_key = next((k for k, v in STORE_LABELS.items() if v == store_label), None)
        if not store_key or store_key == self.active_store:
            return

        self.active_store = store_key
        self.menu_data = self._load_menu()
        self._refresh_category_buttons()

        self.active_category = next(iter(self.menu_data.keys()), None)
        if self.active_category:
            self._select_category(self.active_category)

        # Reset order for new store
        self._clear_order()
        self.order_counter = self._get_next_order_number()
        self.order_badge.configure(text=f"Order  # {self.order_counter:04d}")

        if self.active_tab == "admin":
            self._refresh_admin()

    def _render_category(self, cat: str):
        print(f"Rendering category {cat}")
        # Clear old widgets efficiently
        for widget in self.menu_scroll.winfo_children():
            widget.destroy()

        items = self.menu_data.get(cat, [])
        if not items:
            return

        cols = 3
        for i, item in enumerate(items):
            row, col = divmod(i, cols)
            self._make_item_card(self.menu_scroll, item, row, col)

    def _perform_search(self):
        """Search for items across all categories by name or description."""
        query = self.search_var.get().strip().lower()
        if not query:
            return

        # Clear old widgets
        for widget in self.menu_scroll.winfo_children():
            widget.destroy()

        # Search through all items in all categories
        self.search_results = []
        for category, items in self.menu_data.items():
            for item in items:
                item_name = item["name"].lower()
                item_desc = item.get("desc", "").lower()
                if query in item_name or query in item_desc:
                    self.search_results.append(item)

        self.search_active = True
        self._render_search_results()

    def _render_search_results(self):
        """Display the search results in the menu scroll area."""
        # Clear old widgets
        for widget in self.menu_scroll.winfo_children():
            widget.destroy()

        if not self.search_results:
            no_results_label = ctk.CTkLabel(
                self.menu_scroll,
                text="No items found.\nTry a different search term.",
                text_color=COLORS["text_muted"],
                font=ctk.CTkFont("Helvetica", 13)
            )
            no_results_label.pack(pady=40)
            return

        # Display search results in grid (3 columns)
        cols = 3
        for i, item in enumerate(self.search_results):
            row, col = divmod(i, cols)
            self._make_item_card(self.menu_scroll, item, row, col)

    def _clear_search(self):
        """Clear the search and return to category view."""
        self.search_var.set("")
        self.search_active = False
        self.search_results = []

        # Clear menu scroll
        for widget in self.menu_scroll.winfo_children():
            widget.destroy()

        # Show the active category
        if self.active_category:
            self._render_category(self.active_category)

    def _make_item_card(self, parent, item: dict, row: int, col: int):
        # Use grid layout for better performance than pack
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_card"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        parent.columnconfigure(col, weight=1)

        # Item name
        name_label = ctk.CTkLabel(
            card, text=item["name"],
            font=ctk.CTkFont("Helvetica", 15, "bold"),
            text_color=COLORS["text_primary"],
            wraplength=150,
        )
        name_label.pack(padx=14, pady=(16, 4))

        # Description
        desc_label = ctk.CTkLabel(
            card, text=item["desc"],
            font=ctk.CTkFont("Helvetica", 11),
            text_color=COLORS["text_secondary"],
            wraplength=150,
        )
        desc_label.pack(padx=14, pady=(0, 10))

        # Price
        price_label = ctk.CTkLabel(
            card, text=f"₵{item['price']:.2f}",
            font=ctk.CTkFont("Helvetica", 20, "bold"),
            text_color=COLORS["accent_glow"],
        )
        price_label.pack(padx=14, pady=(0, 12))

        # Add button
        add_btn = ctk.CTkButton(
            card, text="＋  Add to Order",
            height=36, corner_radius=10,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_glow"],
            text_color="white",
            font=ctk.CTkFont("Helvetica", 12, "bold"),
            command=lambda i=item: self._add_item(i),
        )
        add_btn.pack(padx=14, pady=(0, 8), fill="x")

        if self.current_role == "admin":
            # Only admins can edit product details/prices.
            edit_btn = ctk.CTkButton(
                card, text="✏️ Edit",
                height=32, corner_radius=8,
                fg_color=COLORS["warning"],
                hover_color="#D97706",
                text_color="white",
                font=ctk.CTkFont("Helvetica", 11, "bold"),
                command=lambda i=item: self._edit_product(i),
            )
            edit_btn.pack(padx=14, pady=(0, 14), fill="x")

    # ─────────────────────────────────────────
    #  ORDER PANEL
    # ─────────────────────────────────────────
    def _build_order_panel(self, parent):
        # Header
        hdr = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=0, height=58,
                           border_width=1, border_color=COLORS["border"])
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text="🧾  Current Order",
                     font=ctk.CTkFont("Helvetica", 16, "bold"),
                     text_color=COLORS["text_primary"]).pack(side="left", padx=18, pady=12)
        ctk.CTkButton(hdr, text="Clear All", width=90, height=34,
                      fg_color=COLORS["error"], hover_color="#DC2626",
                      text_color="white", corner_radius=8,
                      font=ctk.CTkFont("Helvetica", 11, "bold"),
                      command=self._clear_order).pack(side="right", padx=14, pady=12)

        # Scrollable order list
        self.order_scroll = ctk.CTkScrollableFrame(
            parent, fg_color=COLORS["bg_panel"], corner_radius=0,
            scrollbar_button_color=COLORS["border"],
        )
        self.order_scroll.pack(fill="both", expand=True)

        # Totals area
        totals_frame = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"],
                                    corner_radius=0, border_width=1,
                                    border_color=COLORS["border"])
        totals_frame.pack(fill="x", padx=0, pady=(1, 0))

        for label_attr, val_attr, color in [
            ("Subtotal",  "sub_lbl",   COLORS["text_secondary"]),
            ("Tax (15%)", "tax_lbl",   COLORS["text_secondary"]),
            ("TOTAL",     "total_lbl", COLORS["accent_glow"]),
        ]:
            row = ctk.CTkFrame(totals_frame, fg_color="transparent")
            row.pack(fill="x", padx=18, pady=5)
            ctk.CTkLabel(row, text=label_attr,
                         font=ctk.CTkFont("Helvetica", 13,
                                          "bold" if label_attr == "TOTAL" else "normal"),
                         text_color=color).pack(side="left")
            lbl = ctk.CTkLabel(row, text="₵0.00",
                               font=ctk.CTkFont("Helvetica", 14 if label_attr == "TOTAL" else 13, "bold"),
                               text_color=color)
            lbl.pack(side="right")
            setattr(self, val_attr, lbl)

        # Payment method
        pay_frame = ctk.CTkFrame(parent, fg_color=COLORS["bg_panel"], corner_radius=0,
                                 border_width=1, border_color=COLORS["border"])
        pay_frame.pack(fill="x", padx=0, pady=(1, 0))
        ctk.CTkLabel(pay_frame, text="Payment Method:",
                     font=ctk.CTkFont("Helvetica", 13, "bold"),
                     text_color=COLORS["text_primary"]).pack(side="left", padx=18, pady=12)
        self.payment_var = ctk.StringVar(value="Cash")
        for method in ["Cash", "Card", "Mobile"]:
            ctk.CTkRadioButton(
                pay_frame, text=method, variable=self.payment_var,
                value=method,
                fg_color=COLORS["accent"],
                hover_color=COLORS["accent_glow"],
                border_color=COLORS["accent_soft"],
                text_color=COLORS["text_primary"],
                font=ctk.CTkFont("Helvetica", 12),
            ).pack(side="left", padx=18, pady=12)

        # Cash tendered and change
        cash_frame = ctk.CTkFrame(parent, fg_color=COLORS["bg_panel"], corner_radius=0,
                                  border_width=1, border_color=COLORS["border"])
        cash_frame.pack(fill="x", padx=0, pady=(1, 0))

        ctk.CTkLabel(cash_frame, text="Cash Tendered (₵):",
                     font=ctk.CTkFont("Helvetica", 13, "bold"),
                     text_color=COLORS["text_primary"]).pack(side="left", padx=(18, 10), pady=12)

        self.cash_tendered_var = ctk.StringVar(value="")
        self.cash_entry = ctk.CTkEntry(
            cash_frame,
            textvariable=self.cash_tendered_var,
            width=140,
            height=34,
            fg_color=COLORS["bg_card"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            placeholder_text="0.00",
        )
        self.cash_entry.pack(side="left", padx=(0, 12), pady=10)
        self.cash_entry.bind("<KeyRelease>", lambda _event: self._update_change_display())
        self.cash_entry.bind("<FocusOut>", lambda _event: self._update_change_display())

        ctk.CTkButton(
            cash_frame,
            text="Calculate",
            width=100,
            height=34,
            corner_radius=8,
            fg_color=COLORS["accent_soft"],
            hover_color=COLORS["accent"],
            text_color="#0A0E27",
            font=ctk.CTkFont("Helvetica", 12, "bold"),
            command=self._update_change_display,
        ).pack(side="left", padx=(0, 12), pady=10)

        self.change_lbl = ctk.CTkLabel(
            cash_frame,
            text="Change: enter valid cash amount",
            font=ctk.CTkFont("Helvetica", 12, "bold"),
            text_color=COLORS["warning"],
        )
        self.change_lbl.pack(side="left", padx=(0, 12), pady=10)

        self.payment_var.trace_add("write", lambda *_args: self._update_payment_fields())

        # Checkout button
        ctk.CTkButton(
            parent, text="💳  PROCESS PAYMENT",
            height=60, corner_radius=0,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_glow"],
            text_color="#0A0E27",
            font=ctk.CTkFont("Helvetica", 16, "bold"),
            command=self._checkout,
        ).pack(fill="x", pady=(0, 0))

    # ─────────────────────────────────────────
    #  ORDER LOGIC
    # ─────────────────────────────────────────
    def _add_item(self, item: dict):
        name = item["name"]
        if name in self.order_items:
            self.order_items[name]["qty"] += 1
        else:
            self.order_items[name] = {
                "price": item["price"],
                "qty":   1,
                "desc":  item["desc"],
            }
        self._refresh_order_panel()

    def _remove_item(self, name: str):
        if name in self.order_items:
            if self.order_items[name]["qty"] > 1:
                self.order_items[name]["qty"] -= 1
            else:
                del self.order_items[name]
        self._refresh_order_panel()

    def _clear_order(self):
        self.order_items.clear()
        self._refresh_order_panel()

    def _refresh_order_panel(self):
        # Clear list efficiently
        for widget in self.order_scroll.winfo_children():
            widget.destroy()

        if not self.order_items:
            ctk.CTkLabel(
                self.order_scroll, text="No items yet.\nTap ＋ to add!",
                text_color=COLORS["text_muted"],
                font=ctk.CTkFont("Helvetica", 13),
            ).pack(pady=40)
        else:
            for name, data in self.order_items.items():
                self._make_order_row(name, data)

        # Recalculate totals
        subtotal = sum(d["price"] * d["qty"] for d in self.order_items.values())
        tax      = subtotal * TAX_RATE
        total    = subtotal + tax

        self.sub_lbl.configure(text=f"₵{subtotal:.2f}")
        self.tax_lbl.configure(text=f"₵{tax:.2f}")
        self.total_lbl.configure(text=f"₵{total:.2f}")
        self._update_change_display()

    def _parse_cash_tendered(self):
        raw_cash = self.cash_tendered_var.get().strip().replace("₵", "").replace(",", "")
        if not raw_cash:
            return None
        try:
            value = float(raw_cash)
        except ValueError:
            return None
        if value < 0:
            return None
        return value

    def _update_payment_fields(self):
        is_cash = self.payment_var.get() == "Cash"
        self.cash_entry.configure(state="normal" if is_cash else "disabled")
        if not is_cash:
            self.change_lbl.configure(
                text="Change: N/A (non-cash)",
                text_color=COLORS["text_muted"],
            )
            return
        self._update_change_display()

    def _update_change_display(self):
        if self.payment_var.get() != "Cash":
            self.change_lbl.configure(text="Change: N/A (non-cash)", text_color=COLORS["text_muted"])
            return

        subtotal = sum(d["price"] * d["qty"] for d in self.order_items.values())
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        cash_tendered = self._parse_cash_tendered()

        if cash_tendered is None:
            self.change_lbl.configure(
                text="Change: enter valid cash amount",
                text_color=COLORS["warning"],
            )
            return

        change = cash_tendered - total
        if change < 0:
            self.change_lbl.configure(
                text=f"Insufficient: need ₵{abs(change):.2f} more",
                text_color=COLORS["error"],
            )
        else:
            self.change_lbl.configure(
                text=f"Change: ₵{change:.2f}",
                text_color=COLORS["success"],
            )

    def _make_order_row(self, name: str, data: dict):
        row = ctk.CTkFrame(self.order_scroll, fg_color=COLORS["bg_card"],
                           corner_radius=10, height=52, border_width=1,
                           border_color=COLORS["border"])
        row.pack(fill="x", padx=8, pady=4)
        row.pack_propagate(False)

        # Qty controls
        ctrl = ctk.CTkFrame(row, fg_color="transparent")
        ctrl.pack(side="left", padx=8)

        ctk.CTkButton(ctrl, text="−", width=32, height=32,
                      fg_color=COLORS["bg_hover"], hover_color=COLORS["error"],
                      text_color=COLORS["text_primary"], corner_radius=7,
                      font=ctk.CTkFont("Helvetica", 14, "bold"),
                      command=lambda n=name: self._remove_item(n)).pack(side="left")

        ctk.CTkLabel(ctrl, text=str(data["qty"]), width=32,
                     font=ctk.CTkFont("Helvetica", 13, "bold"),
                     text_color=COLORS["accent_glow"]).pack(side="left", padx=6)

        ctk.CTkButton(ctrl, text="＋", width=32, height=32,
                      fg_color=COLORS["bg_hover"], hover_color=COLORS["success"],
                      text_color=COLORS["text_primary"], corner_radius=7,
                      font=ctk.CTkFont("Helvetica", 14, "bold"),
                      command=lambda n=name, d=data: self._add_item({"name": n, "price": d["price"], "desc": d["desc"]})).pack(side="left")

        # Name
        ctk.CTkLabel(row, text=name, anchor="w",
                     font=ctk.CTkFont("Helvetica", 12, "bold"),
                     text_color=COLORS["text_primary"]).pack(side="left", padx=12, fill="x", expand=True)

        # Line total
        line_total = data["price"] * data["qty"]
        ctk.CTkLabel(row, text=f"₵{line_total:.2f}",
                     font=ctk.CTkFont("Helvetica", 13, "bold"),
                     text_color=COLORS["accent_glow"]).pack(side="right", padx=14)

    # ─────────────────────────────────────────
    #  CHECKOUT
    # ─────────────────────────────────────────
    def _checkout(self):
        if not self.order_items:
            messagebox.showwarning("Empty Order", "Please add items before checking out.")
            return

        subtotal = sum(d["price"] * d["qty"] for d in self.order_items.values())
        tax      = subtotal * TAX_RATE
        total    = subtotal + tax
        payment  = self.payment_var.get()
        cash_tendered = None
        change = None

        if payment == "Cash":
            cash_tendered = self._parse_cash_tendered()
            if cash_tendered is None:
                messagebox.showwarning("Invalid Cash Amount", "Please enter a valid cash amount tendered.")
                return

            change = round(cash_tendered - total, 2)
            if change < 0:
                messagebox.showerror(
                    "Insufficient Funds",
                    f"Cash tendered is not enough.\n"
                    f"Total: ₵{total:.2f}\n"
                    f"Tendered: ₵{cash_tendered:.2f}\n"
                    f"Need: ₵{abs(change):.2f} more",
                )
                return

        items_list = [{"name": n, "price": d["price"], "qty": d["qty"]}
                      for n, d in self.order_items.items()]

        # Save to DB (store-specific)
        self.db.save_transaction(items_list, subtotal, tax, total,
                                 payment, self.order_counter, store=self.active_store)
        self.db.log_activity(
            self.current_user or "unknown",
            self.current_role or "unknown",
            "CHECKOUT",
            f"order#{self.order_counter:04d}",
            f"total={total:.2f}, payment={payment}, cash={cash_tendered if cash_tendered is not None else 'N/A'}, change={change if change is not None else 'N/A'}",
            store=self.active_store or "system",
        )

        # Generate invoice
        invoice = self._build_invoice(items_list, subtotal, tax, total, payment, cash_tendered, change)

        # Show invoice window
        self._show_invoice_window(invoice)

        # Reset
        self._clear_order()
        self.order_counter += 1
        self.order_badge.configure(text=f"Order  # {self.order_counter:04d}")

    def _get_default_printer_name(self) -> str | None:
        """Return the default Windows printer name, or None if unavailable."""
        if os.name != "nt":
            return None

        try:
            needed = wintypes.DWORD(0)
            ctypes.windll.winspool.GetDefaultPrinterW(None, ctypes.byref(needed))
            if needed.value <= 0:
                return None

            buffer = ctypes.create_unicode_buffer(needed.value)
            if ctypes.windll.winspool.GetDefaultPrinterW(buffer, ctypes.byref(needed)):
                name = buffer.value.strip()
                return name if name else None
        except Exception:
            return None

        return None

    def _get_receipt_profile(self, printer_name: str | None = None) -> dict:
        """Choose receipt layout based on printer model/paper size hints."""
        forced_profile = getattr(self, "receipt_paper_profile", "Auto")
        if forced_profile == "80mm":
            return {"paper": "80mm", "line_width": 42, "qty_w": 3, "amt_w": 10}
        if forced_profile == "58mm":
            return {"paper": "58mm", "line_width": 32, "qty_w": 3, "amt_w": 9}

        name = (printer_name or "").lower()

        # Epson TM-T20II is typically an 80mm receipt printer.
        if "tm-t20ii" in name or ("epson" in name and "tm-t20" in name):
            return {"paper": "80mm", "line_width": 42, "qty_w": 3, "amt_w": 10}

        # Common 58mm thermal printers
        if any(token in name for token in ("58mm", "58 mm", "pos-58", "xp-58", "tm-p20")):
            return {"paper": "58mm", "line_width": 32, "qty_w": 3, "amt_w": 9}

        # Safe default for most POS thermal setups
        return {"paper": "80mm", "line_width": 42, "qty_w": 3, "amt_w": 10}

    def _center_receipt_text(self, text: str, width: int) -> str:
        text = (text or "").strip()
        if len(text) >= width:
            return text[:width]
        return text.center(width)

    def _send_raw_to_printer(self, printer_name: str, text_payload: str) -> tuple[bool, str]:
        """Send text directly to the Windows spooler as RAW data."""
        if os.name != "nt":
            return False, "Raw printing is only supported on Windows."

        try:
            winspool = ctypes.windll.winspool

            class DOCINFO1(ctypes.Structure):
                _fields_ = [
                    ("pDocName", wintypes.LPWSTR),
                    ("pOutputFile", wintypes.LPWSTR),
                    ("pDatatype", wintypes.LPWSTR),
                ]

            h_printer = wintypes.HANDLE()
            if not winspool.OpenPrinterW(printer_name, ctypes.byref(h_printer), None):
                raise OSError("OpenPrinterW failed")

            try:
                doc_info = DOCINFO1("Receipt", None, "RAW")
                if winspool.StartDocPrinterW(h_printer, 1, ctypes.byref(doc_info)) == 0:
                    raise OSError("StartDocPrinterW failed")

                try:
                    if not winspool.StartPagePrinter(h_printer):
                        raise OSError("StartPagePrinter failed")

                    payload = text_payload.encode("ascii", errors="replace")
                    written = wintypes.DWORD(0)
                    ok = winspool.WritePrinter(
                        h_printer,
                        payload,
                        len(payload),
                        ctypes.byref(written),
                    )
                    if not ok or written.value != len(payload):
                        raise OSError("WritePrinter failed")

                    if not winspool.EndPagePrinter(h_printer):
                        raise OSError("EndPagePrinter failed")
                finally:
                    winspool.EndDocPrinter(h_printer)
            finally:
                winspool.ClosePrinter(h_printer)

            return True, "Sent to printer via RAW spooler."
        except Exception as e:
            return False, str(e)

    def _build_invoice(self, items, subtotal, tax, total, payment, cash_tendered=None, change=None, printer_name: str | None = None):
        printer_name = printer_name or self._get_default_printer_name()
        profile = self._get_receipt_profile(printer_name)
        width = profile["line_width"]
        qty_w = profile["qty_w"]
        amt_w = profile["amt_w"]
        name_w = max(8, width - qty_w - amt_w - 2)

        now = datetime.datetime.now()

        def _row(name: str, qty: int | str, amount: str):
            name_txt = (name or "")[:name_w]
            qty_txt = str(qty)
            return f"{name_txt:<{name_w}} {qty_txt:>{qty_w}} {amount:>{amt_w}}"

        tax_pct = TAX_RATE * 100
        sep = "=" * width
        mid = "-" * width

        lines = [
            sep,
            self._center_receipt_text(f"{APP_NAME} Restaurant", width),
            self._center_receipt_text("46 Patrice Lumumba Road, Airport", width),
            self._center_receipt_text("P.O. Box 46, State House - Accra", width),
            self._center_receipt_text("GA-117-2059", width),
            sep,
            f"Date : {now.strftime('%Y-%m-%d')}",
            f"Time : {now.strftime('%H:%M:%S')}",
            f"Order: #{self.order_counter:04d}",
            mid,
            _row("ITEM", "Q", "AMOUNT"),
            mid,
        ]

        for item in items:
            line_total = item["price"] * item["qty"]
            lines.append(_row(item["name"], item["qty"], f"GHS{line_total:.2f}"))

        total_label_w = max(8, width - 13)
        lines += [
            mid,
            f"{'Subtotal':<{total_label_w}} GHS{subtotal:>9.2f}",
            f"{f'Tax ({tax_pct:.0f}%)':<{total_label_w}} GHS{tax:>9.2f}",
            sep,
            f"{'TOTAL':<{total_label_w}} GHS{total:>9.2f}",
            sep,
            f"Payment: {payment}",
        ]

        if payment == "Cash" and cash_tendered is not None and change is not None:
            lines.append(f"{'Cash Tendered':<{total_label_w}} GHS{cash_tendered:>9.2f}")
            lines.append(f"{'Change':<{total_label_w}} GHS{change:>9.2f}")

        lines += [
            "",
            self._center_receipt_text("Thank You For Your Patronage", width),
            self._center_receipt_text("See You Soon!", width),
            sep,
        ]

        return "\n".join(lines)

    def _show_invoice_window(self, invoice: str):
        printer_name = self._get_default_printer_name()
        active_profile = self._get_receipt_profile(printer_name)
        selected_mode = getattr(self, "receipt_paper_profile", "Auto")
        if selected_mode == "Auto":
            mode_detail = f"Auto ({printer_name if printer_name else 'No default printer'})"
        else:
            mode_detail = f"Manual ({selected_mode})"

        win = ctk.CTkToplevel(self)
        win.title("Order Receipt")
        win.geometry("500x640")
        win.configure(fg_color=COLORS["bg_dark"])
        win.grab_set()

        ctk.CTkLabel(win, text="✅  Order Complete!",
                     font=ctk.CTkFont("Helvetica", 18, "bold"),
                     text_color=COLORS["success"]).pack(pady=(18, 12))

        ctk.CTkLabel(
            win,
            text=f"Print Profile: {active_profile['paper']}  |  {mode_detail}",
            font=ctk.CTkFont("Helvetica", 10),
            text_color=COLORS["text_muted"],
        ).pack(pady=(0, 8))

        txt = ctk.CTkTextbox(win, fg_color=COLORS["bg_dark"],
                             text_color=COLORS["text_primary"],
                             font=ctk.CTkFont("Courier", 12),
                             corner_radius=8)
        txt.pack(fill="both", expand=True, padx=16, pady=4)
        txt.insert("end", invoice)
        txt.configure(state="disabled")

        def send_file_to_printer(file_path: str, printer_name: str | None) -> tuple[bool, str]:
            """Try multiple print mechanisms so printing works across typical Windows setups."""
            abs_path = os.path.abspath(file_path)

            # Preferred path for thermal printers: RAW spool preserves monospaced layout.
            if printer_name:
                try:
                    raw_text = open(abs_path, "r", encoding="utf-8", errors="ignore").read()
                except Exception:
                    raw_text = None
                if raw_text is not None:
                    ok_raw, raw_msg = self._send_raw_to_printer(printer_name, raw_text + "\n\n\n")
                    if ok_raw:
                        return True, raw_msg

            try:
                os.startfile(abs_path, "print")
                return True, "Sent to the default printer."
            except Exception as first_error:
                try:
                    subprocess.run(["notepad.exe", "/p", abs_path], check=True, timeout=20)
                    return True, "Sent to printer via Notepad fallback."
                except Exception as second_error:
                    printer_msg = f" Default printer: {printer_name}." if printer_name else ""
                    return False, (
                        f"Could not send the receipt to the printer.{printer_msg}\n"
                        f"Primary method error: {first_error}\n"
                        f"Fallback method error: {second_error}"
                    )

        def print_invoice():
            # Save invoice to file and send directly to printer.
            app_data_dir = get_app_data_dir()
            printer_name = self._get_default_printer_name()
            printable_invoice = invoice

            fname = os.path.join(app_data_dir, f"invoice_{self.order_counter:04d}.txt")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(printable_invoice)

            if not printer_name:
                messagebox.showerror(
                    "Printer Not Detected",
                    "No default printer was detected on this system.\n"
                    "Set a default printer in Windows Settings and try again.\n"
                    f"Receipt was still saved as '{fname}'."
                )
                return

            ok, detail = send_file_to_printer(fname, printer_name)
            try:
                if ok:
                    messagebox.showinfo(
                        "Print Sent",
                        f"Receipt sent to printer '{printer_name}'.\n"
                        f"File saved as '{fname}'.\n{detail}"
                    )
                else:
                    messagebox.showerror(
                        "Print Failed",
                        f"Detected printer: '{printer_name}', but printing failed.\n"
                        f"{detail}\n"
                        f"Receipt saved as '{fname}'."
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected print error: {str(e)}\nFile saved as '{fname}'")

        btn_row = ctk.CTkFrame(win, fg_color="transparent")
        btn_row.pack(pady=16)

        ctk.CTkButton(btn_row, text="🖨️  Print Receipt", width=140, height=42,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_glow"],
                      text_color="#0A0E27", corner_radius=9,
                      font=ctk.CTkFont("Helvetica", 13, "bold"),
                      command=print_invoice).pack(side="left", padx=8)

        ctk.CTkButton(btn_row, text="✖  Close", width=140, height=42,
                      fg_color=COLORS["border"], hover_color=COLORS["bg_card"],
                      text_color=COLORS["text_primary"], corner_radius=9,
                      font=ctk.CTkFont("Helvetica", 13, "bold"),
                      command=win.destroy).pack(side="left", padx=8)

    # ═══════════════════════════════════════════
    #  ADMIN VIEW
    # ═══════════════════════════════════════════
    def _build_admin_view(self, parent):
        # Scroll container so all admin sections remain reachable on any window size.
        admin_scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color=COLORS["bg_dark"],
            corner_radius=0,
            scrollbar_button_color=COLORS["border"],
        )
        admin_scroll.pack(fill="both", expand=True)

        # Top summary cards row
        self.admin_cards_frame = ctk.CTkFrame(admin_scroll, fg_color=COLORS["bg_dark"],
                                              corner_radius=0, height=110)
        self.admin_cards_frame.pack(fill="x", padx=16, pady=(12, 0))
        self.admin_cards_frame.pack_propagate(False)

        # Transaction history
        hist_lbl = ctk.CTkLabel(admin_scroll, text="📋  Transaction History",
                                font=ctk.CTkFont("Helvetica", 16, "bold"),
                                text_color=COLORS["text_primary"])
        hist_lbl.pack(anchor="w", padx=20, pady=(16, 4))

        # ── Date-range filter bar ──
        filter_bar = ctk.CTkFrame(admin_scroll, fg_color=COLORS["bg_card"],
                                   corner_radius=10, border_width=1,
                                   border_color=COLORS["border"])
        filter_bar.pack(fill="x", padx=16, pady=(0, 8))

        ctk.CTkLabel(filter_bar, text="🗓  From:",
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=COLORS["text_secondary"]).pack(side="left", padx=(14, 4), pady=10)

        self._tx_from_var = tk.StringVar()
        self._tx_from_entry = ctk.CTkEntry(filter_bar, textvariable=self._tx_from_var,
                                           width=110, height=34, corner_radius=8,
                                           fg_color=COLORS["bg_hover"],
                                           border_color=COLORS["border"],
                                           placeholder_text="YYYY-MM-DD",
                                           font=ctk.CTkFont("Helvetica", 11))
        self._tx_from_entry.pack(side="left", padx=(0, 4), pady=10)

        ctk.CTkButton(filter_bar, text="📅", width=34, height=34, corner_radius=8,
                      fg_color=COLORS["bg_hover"], hover_color=COLORS["border"],
                      text_color=COLORS["text_primary"],
                      font=ctk.CTkFont("Helvetica", 13),
                      command=lambda: DatePickerPopup(
                          self,
                          lambda d: self._tx_from_var.set(d),
                          self._tx_from_var.get() or None,
                      )).pack(side="left", padx=(0, 10), pady=10)

        ctk.CTkLabel(filter_bar, text="To:",
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=COLORS["text_secondary"]).pack(side="left", padx=(0, 4), pady=10)

        self._tx_to_var = tk.StringVar()
        self._tx_to_entry = ctk.CTkEntry(filter_bar, textvariable=self._tx_to_var,
                                         width=110, height=34, corner_radius=8,
                                         fg_color=COLORS["bg_hover"],
                                         border_color=COLORS["border"],
                                         placeholder_text="YYYY-MM-DD",
                                         font=ctk.CTkFont("Helvetica", 11))
        self._tx_to_entry.pack(side="left", padx=(0, 4), pady=10)

        ctk.CTkButton(filter_bar, text="📅", width=34, height=34, corner_radius=8,
                      fg_color=COLORS["bg_hover"], hover_color=COLORS["border"],
                      text_color=COLORS["text_primary"],
                      font=ctk.CTkFont("Helvetica", 13),
                      command=lambda: DatePickerPopup(
                          self,
                          lambda d: self._tx_to_var.set(d),
                          self._tx_to_var.get() or None,
                      )).pack(side="left", padx=(0, 12), pady=10)

        ctk.CTkButton(filter_bar, text="Apply Filter",
                      width=110, height=34, corner_radius=8,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_glow"],
                      text_color="white",
                      font=ctk.CTkFont("Helvetica", 11, "bold"),
                      command=self._apply_tx_filter).pack(side="left", padx=(0, 6), pady=10)

        ctk.CTkButton(filter_bar, text="Clear",
                      width=70, height=34, corner_radius=8,
                      fg_color=COLORS["bg_hover"], hover_color=COLORS["border"],
                      text_color=COLORS["text_secondary"],
                      font=ctk.CTkFont("Helvetica", 11),
                      command=self._clear_tx_filter).pack(side="left", padx=(0, 10), pady=10)

        self._tx_count_lbl = ctk.CTkLabel(filter_bar, text="",
                                           font=ctk.CTkFont("Helvetica", 10),
                                           text_color=COLORS["text_muted"])
        self._tx_count_lbl.pack(side="right", padx=14, pady=10)

        # Table
        table_frame = ctk.CTkFrame(admin_scroll, fg_color=COLORS["bg_card"],
                                   corner_radius=14, border_width=1,
                                   border_color=COLORS["border"], height=260)
        table_frame.pack(fill="x", padx=16, pady=(0, 12))
        table_frame.pack_propagate(False)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=COLORS["bg_card"],
                        foreground=COLORS["text_primary"],
                        fieldbackground=COLORS["bg_card"],
                        rowheight=30,
                        borderwidth=0,
                        relief="flat",
                        font=("Helvetica", 11))
        style.configure("Custom.Treeview.Heading",
                        background=COLORS["bg_hover"],
                        foreground=COLORS["accent"],
                        relief="flat",
                        font=("Helvetica", 11, "bold"))
        style.map("Custom.Treeview",
                  background=[("selected", COLORS["accent"])],
                  foreground=[("selected", "white")])

        cols = ("#", "Date", "Time", "Items", "Subtotal", "Tax", "Total", "Payment")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings",
                                 style="Custom.Treeview")

        widths = [60, 100, 80, 300, 90, 80, 90, 90]
        for col, width in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center" if col != "Items" else "w")

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical",
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=4, pady=4)

        # Product management
        prod_lbl = ctk.CTkLabel(admin_scroll, text="🛠️  Product Management",
                                font=ctk.CTkFont("Helvetica", 16, "bold"),
                                text_color=COLORS["text_primary"])
        prod_lbl.pack(anchor="w", padx=20, pady=(16, 8))

        prod_frame = ctk.CTkFrame(admin_scroll, fg_color=COLORS["bg_card"],
                      corner_radius=10, height=260)
        prod_frame.pack(fill="x", padx=16, pady=(0, 12))
        prod_frame.pack_propagate(False)

        self._build_product_management(prod_frame)

        # Receipt printer settings
        receipt_frame = ctk.CTkFrame(admin_scroll, fg_color=COLORS["bg_card"],
                                     corner_radius=10, border_width=1,
                                     border_color=COLORS["border"])
        receipt_frame.pack(fill="x", padx=16, pady=(0, 12))

        ctk.CTkLabel(receipt_frame, text="🖨️  Receipt Paper Profile",
                     font=ctk.CTkFont("Helvetica", 14, "bold"),
                     text_color=COLORS["text_primary"]).pack(anchor="w", padx=12, pady=(10, 4))

        receipt_row = ctk.CTkFrame(receipt_frame, fg_color="transparent")
        receipt_row.pack(fill="x", padx=12, pady=(0, 10))

        ctk.CTkLabel(receipt_row, text="Profile:",
                     font=ctk.CTkFont("Helvetica", 11, "bold"),
                     text_color=COLORS["text_secondary"]).pack(side="left", padx=(0, 8))

        self.admin_receipt_profile_var = tk.StringVar(value=self.receipt_paper_profile)
        ctk.CTkComboBox(
            receipt_row,
            width=170,
            height=32,
            values=["Auto", "80mm", "58mm"],
            variable=self.admin_receipt_profile_var,
            command=lambda v: self._on_receipt_profile_changed(v),
            fg_color=COLORS["bg_hover"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            dropdown_fg_color=COLORS["bg_card"],
            dropdown_text_color=COLORS["text_primary"],
            font=ctk.CTkFont("Helvetica", 11),
        ).pack(side="left")

        ctk.CTkLabel(receipt_row,
                     text="Auto uses detected printer model (TM-T20II -> 80mm).",
                     font=ctk.CTkFont("Helvetica", 10),
                     text_color=COLORS["text_muted"]).pack(side="left", padx=(10, 0))

        # All-system item list (read-only)
        ctk.CTkLabel(admin_scroll, text="🧾  All System Items",
                     font=ctk.CTkFont("Helvetica", 16, "bold"),
                     text_color=COLORS["text_primary"]).pack(anchor="w", padx=20, pady=(16, 8))

        admin_items_frame = ctk.CTkFrame(admin_scroll, fg_color=COLORS["bg_card"],
                                         corner_radius=10, border_width=1,
                                         border_color=COLORS["border"], height=240)
        admin_items_frame.pack(fill="x", padx=16, pady=(0, 12))
        admin_items_frame.pack_propagate(False)

        admin_items_filter_row = ctk.CTkFrame(admin_items_frame, fg_color="transparent")
        admin_items_filter_row.pack(fill="x", padx=8, pady=(8, 4))

        ctk.CTkLabel(admin_items_filter_row, text="Store:",
                     font=ctk.CTkFont("Helvetica", 11, "bold"),
                     text_color=COLORS["text_secondary"]).pack(side="left", padx=(4, 8))

        self.admin_items_store_var = tk.StringVar(value="All")
        ctk.CTkComboBox(
            admin_items_filter_row,
            width=150,
            height=30,
            values=["All", "Fast Food", "Cold Store"],
            variable=self.admin_items_store_var,
            command=lambda _v: self._on_admin_items_store_change(),
            fg_color=COLORS["bg_hover"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            dropdown_fg_color=COLORS["bg_card"],
            dropdown_text_color=COLORS["text_primary"],
            font=ctk.CTkFont("Helvetica", 11),
        ).pack(side="left")

        admin_item_cols = ("Store", "Category", "Item", "Price (₵)", "Stock")
        self.admin_items_tree = ttk.Treeview(
            admin_items_frame,
            columns=admin_item_cols,
            show="headings",
            style="Custom.Treeview",
            height=7,
        )
        for col, width in zip(admin_item_cols, [110, 150, 260, 120, 100]):
            self.admin_items_tree.heading(col, text=col)
            self.admin_items_tree.column(col, width=width, anchor="center" if col != "Item" else "w")

        admin_items_scroll = ttk.Scrollbar(admin_items_frame, orient="vertical",
                                           command=self.admin_items_tree.yview)
        self.admin_items_tree.configure(yscrollcommand=admin_items_scroll.set)
        admin_items_scroll.pack(side="right", fill="y", padx=(0, 4), pady=6)
        self.admin_items_tree.pack(fill="both", expand=True, padx=8, pady=(0, 6))

        # User management (credentials)
        # ── Item Sales Report ──
        ctk.CTkLabel(admin_scroll, text="📈  Item Sales Report",
                     font=ctk.CTkFont("Helvetica", 16, "bold"),
                     text_color=COLORS["text_primary"]).pack(anchor="w", padx=20, pady=(16, 8))

        report_frame = ctk.CTkFrame(admin_scroll, fg_color=COLORS["bg_card"],
                                    corner_radius=10, border_width=1,
                                    border_color=COLORS["border"])
        report_frame.pack(fill="x", padx=16, pady=(0, 12))
        self._build_item_report_panel(report_frame)

        # Logout button
        logout_btn = ctk.CTkButton(admin_scroll, text="🚪 Logout Admin", height=40, fg_color=COLORS["error"], hover_color="#DC2626", text_color="white", font=ctk.CTkFont("Helvetica", 12, "bold"), corner_radius=8, command=self._logout_admin)
        logout_btn.pack(pady=(0, 20))

    def _build_root_admin_view(self, parent):
        header = ctk.CTkFrame(parent, fg_color=COLORS["bg_panel"], corner_radius=10,
                              border_width=1, border_color=COLORS["border"])
        header.pack(fill="x", padx=16, pady=(16, 10))

        ctk.CTkLabel(
            header,
            text="🛡️ Root Admin Dashboard",
            font=ctk.CTkFont("Helvetica", 20, "bold"),
            text_color=COLORS["accent_glow"],
        ).pack(side="left", padx=16, pady=14)

        ctk.CTkButton(
            header,
            text="+ Add User",
            width=110,
            fg_color=COLORS["success"],
            hover_color="#059669",
            text_color="white",
            command=self._open_root_add_user_dialog,
        ).pack(side="right", padx=(8, 8), pady=10)

        ctk.CTkButton(
            header,
            text="Refresh",
            width=100,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_glow"],
            text_color="#0A0E27",
            command=self._refresh_root_admin,
        ).pack(side="right", padx=(8, 4), pady=10)

        self.root_receipt_profile_var = tk.StringVar(value=self.receipt_paper_profile)
        ctk.CTkComboBox(
            header,
            width=110,
            height=30,
            values=["Auto", "80mm", "58mm"],
            variable=self.root_receipt_profile_var,
            command=lambda v: self._on_receipt_profile_changed(v),
            fg_color=COLORS["bg_hover"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            dropdown_fg_color=COLORS["bg_card"],
            dropdown_text_color=COLORS["text_primary"],
            font=ctk.CTkFont("Helvetica", 10),
        ).pack(side="right", padx=(8, 4), pady=10)

        ctk.CTkLabel(header, text="Receipt:",
                     font=ctk.CTkFont("Helvetica", 10, "bold"),
                     text_color=COLORS["text_secondary"]).pack(side="right", padx=(8, 2), pady=10)

        # User list section
        user_section = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=10,
                                    border_width=1, border_color=COLORS["border"])
        user_section.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        ctk.CTkLabel(user_section, text="Users In System",
                     font=ctk.CTkFont("Helvetica", 15, "bold"),
                     text_color=COLORS["text_primary"]).pack(anchor="w", padx=12, pady=(10, 6))

        user_cols = ("ID", "Store", "Role", "Username", "Status")
        self.root_user_tree = ttk.Treeview(user_section, columns=user_cols, show="headings", height=10,
                                           style="Custom.Treeview")
        for col, width in zip(user_cols, [80, 120, 120, 190, 100]):
            self.root_user_tree.heading(col, text=col)
            self.root_user_tree.column(col, width=width, anchor="center")

        user_scroll = ttk.Scrollbar(user_section, orient="vertical", command=self.root_user_tree.yview)
        self.root_user_tree.configure(yscrollcommand=user_scroll.set)
        user_scroll.pack(side="right", fill="y", padx=(0, 6), pady=6)
        self.root_user_tree.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        user_actions = ctk.CTkFrame(user_section, fg_color="transparent")
        user_actions.pack(fill="x", padx=8, pady=(0, 10))

        ctk.CTkButton(
            user_actions,
            text="Disable Selected",
            fg_color=COLORS["warning"],
            hover_color="#D97706",
            text_color="white",
            command=lambda: self._toggle_user_status(True),
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            user_actions,
            text="Enable Selected",
            fg_color=COLORS["success"],
            hover_color="#059669",
            text_color="white",
            command=lambda: self._toggle_user_status(False),
        ).pack(side="left", padx=4)

        # All-system item list (read-only)
        items_section = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=10,
                                     border_width=1, border_color=COLORS["border"])
        items_section.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        ctk.CTkLabel(items_section, text="System Items",
                     font=ctk.CTkFont("Helvetica", 15, "bold"),
                     text_color=COLORS["text_primary"]).pack(anchor="w", padx=12, pady=(10, 6))

        root_items_filter_row = ctk.CTkFrame(items_section, fg_color="transparent")
        root_items_filter_row.pack(fill="x", padx=8, pady=(0, 4))

        ctk.CTkLabel(root_items_filter_row, text="Store:",
                     font=ctk.CTkFont("Helvetica", 11, "bold"),
                     text_color=COLORS["text_secondary"]).pack(side="left", padx=(4, 8))

        self.root_items_store_var = tk.StringVar(value="All")
        ctk.CTkComboBox(
            root_items_filter_row,
            width=150,
            height=30,
            values=["All", "Fast Food", "Cold Store"],
            variable=self.root_items_store_var,
            command=lambda _v: self._on_root_items_store_change(),
            fg_color=COLORS["bg_hover"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            dropdown_fg_color=COLORS["bg_card"],
            dropdown_text_color=COLORS["text_primary"],
            font=ctk.CTkFont("Helvetica", 11),
        ).pack(side="left")

        root_item_cols = ("Store", "Category", "Item", "Price (₵)", "Stock")
        self.root_items_tree = ttk.Treeview(items_section, columns=root_item_cols,
                                            show="headings", height=10,
                                            style="Custom.Treeview")
        for col, width in zip(root_item_cols, [110, 150, 260, 120, 100]):
            self.root_items_tree.heading(col, text=col)
            self.root_items_tree.column(col, width=width, anchor="center" if col != "Item" else "w")

        root_items_scroll = ttk.Scrollbar(items_section, orient="vertical", command=self.root_items_tree.yview)
        self.root_items_tree.configure(yscrollcommand=root_items_scroll.set)
        root_items_scroll.pack(side="right", fill="y", padx=(0, 6), pady=6)
        self.root_items_tree.pack(fill="both", expand=True, padx=8, pady=(0, 10))

        # Activity log section
        log_section = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=10,
                                   border_width=1, border_color=COLORS["border"])
        log_section.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        ctk.CTkLabel(log_section, text="System Activity Log",
                     font=ctk.CTkFont("Helvetica", 15, "bold"),
                     text_color=COLORS["text_primary"]).pack(anchor="w", padx=12, pady=(10, 6))

        log_cols = ("Time", "Actor", "Role", "Action", "Target", "Store")
        self.root_log_tree = ttk.Treeview(log_section, columns=log_cols, show="headings", height=10,
                                          style="Custom.Treeview")
        for col, width in zip(log_cols, [170, 150, 110, 220, 220, 120]):
            self.root_log_tree.heading(col, text=col)
            self.root_log_tree.column(col, width=width, anchor="center")

        log_scroll = ttk.Scrollbar(log_section, orient="vertical", command=self.root_log_tree.yview)
        self.root_log_tree.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side="right", fill="y", padx=(0, 6), pady=6)
        self.root_log_tree.pack(fill="both", expand=True, padx=8, pady=(0, 10))

        ctk.CTkButton(
            parent,
            text="🚪 Logout Root Admin",
            height=40,
            fg_color=COLORS["error"],
            hover_color="#DC2626",
            text_color="white",
            corner_radius=8,
            command=self._logout_admin,
        ).pack(pady=(0, 16))

    def _refresh_root_admin(self):
        if getattr(self, "current_role", None) != "root_admin":
            return

        if hasattr(self, "root_user_tree"):
            for row in self.root_user_tree.get_children():
                self.root_user_tree.delete(row)
            for uid, store, role, username, disabled in self.db.get_all_users():
                status = "Disabled" if disabled else "Active"
                self.root_user_tree.insert("", "end", values=(uid, store, role, username, status))

        if hasattr(self, "root_log_tree"):
            for row in self.root_log_tree.get_children():
                self.root_log_tree.delete(row)
            for _id, timestamp, actor_username, actor_role, action, target, details, store in self.db.get_activity_logs():
                self.root_log_tree.insert("", "end", values=(timestamp, actor_username, actor_role, action, target, store))

        if hasattr(self, "root_items_tree"):
            self._populate_system_items_tree(
                self.root_items_tree,
                self.root_items_store_var.get() if hasattr(self, "root_items_store_var") else "All",
            )

    def _open_root_add_user_dialog(self):
        if self.current_role != "root_admin":
            messagebox.showerror("Access Denied", "Only root admin can add users.")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Add System User")
        dialog.geometry("420x360")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color=COLORS["bg_dark"])

        ctk.CTkLabel(dialog, text="Store:").pack(pady=(14, 4))
        store_var = tk.StringVar(value="fast_food")
        ctk.CTkComboBox(dialog, values=["fast_food", "cold_store", "system"], variable=store_var).pack(fill="x", padx=20)

        ctk.CTkLabel(dialog, text="Role:").pack(pady=(10, 4))
        role_var = tk.StringVar(value="attendant")
        ctk.CTkComboBox(dialog, values=["attendant", "admin", "root_admin"], variable=role_var).pack(fill="x", padx=20)

        ctk.CTkLabel(dialog, text="Username:").pack(pady=(10, 4))
        username_entry = ctk.CTkEntry(dialog)
        username_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(dialog, text="Password:").pack(pady=(10, 4))
        password_entry = ctk.CTkEntry(dialog, show="*")
        password_entry.pack(fill="x", padx=20)

        def save_user():
            store = store_var.get().strip().lower()
            role = role_var.get().strip().lower()
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showerror("Error", "Username and password are required")
                return

            if role == "root_admin":
                store = "system"

            try:
                self.db.add_user(store, role, username, password)
                self.db.log_activity(
                    self.current_user or "root_admin",
                    "root_admin",
                    "CREATE_USER",
                    username,
                    f"role={role}, store={store}",
                    store="system",
                )
                self._refresh_root_admin()
                dialog.destroy()
                messagebox.showinfo("Success", f"User '{username}' created")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Could not create user (duplicate or invalid data)")

        btns = ctk.CTkFrame(dialog, fg_color="transparent")
        btns.pack(pady=18)
        ctk.CTkButton(btns, text="Save", width=110, command=save_user).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Cancel", width=110, command=dialog.destroy).pack(side="left", padx=6)

    def _toggle_user_status(self, disable: bool):
        if self.current_role != "root_admin":
            messagebox.showerror("Access Denied", "Only root admin can enable or disable users.")
            return

        selected = self.root_user_tree.selection() if hasattr(self, "root_user_tree") else []
        if not selected:
            messagebox.showwarning("No Selection", "Select a user first.")
            return

        values = self.root_user_tree.item(selected[0], "values")
        if not values:
            return

        user_id = int(values[0])
        store = values[1]
        role = values[2]
        username = values[3]

        if role == "root_admin" and disable:
            messagebox.showwarning("Not Allowed", "Root admin account cannot be disabled.")
            return

        self.db.set_user_disabled(user_id, disable)
        action = "DISABLE_USER" if disable else "ENABLE_USER"
        self.db.log_activity(
            self.current_user or "root_admin",
            "root_admin",
            action,
            username,
            f"role={role}, store={store}",
            store="system",
        )
        self._refresh_root_admin()

    def _apply_tx_filter(self):
        """Apply the From/To date filter to the transaction table."""
        from_str = self._tx_from_var.get().strip()
        to_str   = self._tx_to_var.get().strip()

        # Validate both dates
        for val, label in [(from_str, "From"), (to_str, "To")]:
            if val:
                try:
                    datetime.date.fromisoformat(val)
                except ValueError:
                    messagebox.showerror("Invalid Date",
                                         f"{label} date '{val}' is not valid.\n"
                                         "Use the format YYYY-MM-DD.")
                    return

        if from_str and to_str and from_str > to_str:
            messagebox.showerror("Invalid Range",
                                 "The 'From' date must be on or before the 'To' date.")
            return

        self._populate_tx_table()

    def _clear_tx_filter(self):
        """Clear the date filter and show all transactions."""
        self._tx_from_var.set("")
        self._tx_to_var.set("")
        self._populate_tx_table()

    def _populate_tx_table(self):
        """Fill the transaction Treeview respecting any active date filter."""
        from_str = self._tx_from_var.get().strip()
        to_str   = self._tx_to_var.get().strip()

        if from_str or to_str:
            # Default missing bound to extreme values
            f = from_str or "0001-01-01"
            t = to_str   or "9999-12-31"
            txs = self.db.get_transactions_by_date_range(f, t, store=self.active_store)
        else:
            txs = self.db.get_all_transactions(store=self.active_store)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for tx in txs:
            items = json.loads(tx[3])
            items_str = ", ".join(f"{i['qty']}× {i['name']}" for i in items)
            self.tree.insert("", "end", values=(
                f"#{tx[8]:04d}", tx[1], tx[2],
                items_str,
                f"₵{tx[4]:.2f}", f"₵{tx[5]:.2f}", f"₵{tx[6]:.2f}",
                tx[7],
            ))

        # Update result count label
        if hasattr(self, "_tx_count_lbl"):
            if from_str or to_str:
                self._tx_count_lbl.configure(
                    text=f"{len(txs)} result{'s' if len(txs) != 1 else ''} found"
                )
            else:
                self._tx_count_lbl.configure(text=f"{len(txs)} total")

    def _refresh_admin(self):
        # ── Summary cards ──
        for widget in self.admin_cards_frame.winfo_children():
            widget.destroy()

        today_orders, today_revenue = self.db.get_today_summary(store=self.active_store)
        top_items = self.db.get_top_items(3, store=self.active_store)
        all_tx = self.db.get_all_transactions(store=self.active_store)
        all_revenue = sum(r[6] for r in all_tx)

        card_data = [
            ("📦  Today's Orders",   str(today_orders),     COLORS["accent_glow"]),
            ("💰  Today's Revenue",  f"₵{today_revenue:.2f}", COLORS["success"]),
            ("🏆  All-time Revenue", f"₵{all_revenue:.2f}",   COLORS["gold"]),
            ("🔥  Top Seller",       top_items[0][0] if top_items else "—",
             COLORS["accent"]),
        ]

        for label, value, color in card_data:
            card = ctk.CTkFrame(self.admin_cards_frame, fg_color=COLORS["bg_card"],
                                corner_radius=12, border_width=1,
                                border_color=COLORS["border"])
            card.pack(side="left", fill="both", expand=True, padx=8)
            label_widget = ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont("Helvetica", 12),
                         text_color=COLORS["text_secondary"])
            label_widget.pack(pady=(14, 4))
            value_widget = ctk.CTkLabel(card, text=value,
                         font=ctk.CTkFont("Helvetica", 22, "bold"),
                         text_color=color)
            value_widget.pack(pady=(0, 14))

        # ── Populate table (respects active date filter) ──
        self._populate_tx_table()

        # Refresh item report combo list
        if hasattr(self, "report_item_combo"):
            self._refresh_item_report_items()

        if hasattr(self, "admin_items_tree"):
            self._populate_system_items_tree(
                self.admin_items_tree,
                self.admin_items_store_var.get() if hasattr(self, "admin_items_store_var") else "All",
            )

    def _on_admin_items_store_change(self):
        if hasattr(self, "admin_items_tree") and hasattr(self, "admin_items_store_var"):
            self._populate_system_items_tree(self.admin_items_tree, self.admin_items_store_var.get())

    def _on_root_items_store_change(self):
        if hasattr(self, "root_items_tree") and hasattr(self, "root_items_store_var"):
            self._populate_system_items_tree(self.root_items_tree, self.root_items_store_var.get())

    def _populate_system_items_tree(self, tree_widget, store_filter: str = "All"):
        for row in tree_widget.get_children():
            tree_widget.delete(row)

        store_map = {
            "All": None,
            "Fast Food": "fast_food",
            "Cold Store": "cold_store",
        }
        selected_store = store_map.get(store_filter, None)

        for row in self.db.get_all_products(store=selected_store):
            store = STORE_LABELS.get(row[6], row[6])
            category = row[1]
            name = row[2]
            price = f"{row[3]:,.2f}"
            stock = str(row[5])
            tree_widget.insert("", "end", values=(store, category, name, price, stock))

    # ─────────────────────────────────────────
    #  UTILITIES
    # ─────────────────────────────────────────
    def _tick_clock(self):
        now = datetime.datetime.now().strftime("%A, %d %b %Y   %H:%M:%S")
        self.clock_lbl.configure(text=now)
        self.after(1000, self._tick_clock)

    def _get_next_order_number(self) -> int:
        rows = self.db.get_all_transactions(store=self.active_store)
        if rows:
            return max(r[8] for r in rows) + 1
        return 1001

    def _normalize_category(self, category: str) -> str:
        # Normalize categories by removing emojis and non-alphanumeric characters.
        return re.sub(r"[^A-Za-z0-9]", "", category).strip().lower()

    def _load_menu(self):
        if not self.active_store:
            return {}
        products = self.db.get_all_products(store=self.active_store)
        base_menu = STORE_MENUS.get(self.active_store, {})
        menu = {cat: [] for cat in base_menu}

        # Map database categories to the UI categories (e.g., "Pastries" -> "🍔 Pastries")
        def find_category_key(db_cat: str) -> str | None:
            if db_cat in menu:
                return db_cat
            norm = self._normalize_category(db_cat)
            for key in menu:
                if self._normalize_category(key) == norm:
                    return key
            return None

        for row in products:
            # row: id, category, name, price, desc, store
            cat = row[1]
            key = find_category_key(cat)
            item = {
                'id': row[0],
                'category': row[1],
                'name': row[2],
                'price': row[3],
                'desc': row[4],
                'store': row[5] if len(row) > 5 else self.active_store,
            }
            if key:
                menu[key].append(item)
            else:
                # Unknown category: keep it so it doesn't get lost (use raw name)
                if cat not in menu:
                    menu[cat] = []
                menu[cat].append(item)

        # Sort items within each category for consistent display
        for cat_items in menu.values():
            cat_items.sort(key=lambda x: x['name'])

        return menu

    def _build_item_report_panel(self, parent):
        """Build the Item Sales Report controls inside the given frame."""
        inner = ctk.CTkFrame(parent, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=14)

        # ── Row 1: period selector + item picker ──
        row1 = ctk.CTkFrame(inner, fg_color="transparent")
        row1.pack(fill="x")

        ctk.CTkLabel(row1, text="Period:",
                     font=ctk.CTkFont("Helvetica", 12, "bold"),
                     text_color=COLORS["text_secondary"]).pack(side="left")

        self.report_period_var = tk.StringVar(value="Daily")

        def _on_period_change():
            self._refresh_item_report_items()
            if self.report_period_var.get() == "Custom":
                self._report_date_row.pack(fill="x", pady=(8, 0))
            else:
                self._report_date_row.pack_forget()

        for label in ("Daily", "Weekly", "Monthly", "Custom"):
            ctk.CTkRadioButton(
                row1, text=label,
                variable=self.report_period_var, value=label,
                fg_color=COLORS["accent"], hover_color=COLORS["accent_glow"],
                border_color=COLORS["accent_soft"],
                text_color=COLORS["text_primary"],
                font=ctk.CTkFont("Helvetica", 12),
                command=_on_period_change,
            ).pack(side="left", padx=(14, 0))

        ctk.CTkFrame(row1, fg_color=COLORS["border"], width=1, height=28).pack(
            side="left", padx=18)

        ctk.CTkLabel(row1, text="Item:",
                     font=ctk.CTkFont("Helvetica", 12, "bold"),
                     text_color=COLORS["text_secondary"]).pack(side="left")

        self.report_item_var = tk.StringVar(value="")
        self.report_item_combo = ctk.CTkComboBox(
            row1, variable=self.report_item_var,
            values=[], width=240, height=34,
            fg_color=COLORS["bg_hover"], border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            dropdown_fg_color=COLORS["bg_card"],
            dropdown_text_color=COLORS["text_primary"],
            font=ctk.CTkFont("Helvetica", 12),
        )
        self.report_item_combo.pack(side="left", padx=(10, 16))

        ctk.CTkButton(
            row1, text="Generate Report",
            height=34, width=150, corner_radius=8,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_glow"],
            text_color="#0A0E27",
            font=ctk.CTkFont("Helvetica", 12, "bold"),
            command=self._run_item_report,
        ).pack(side="left")

        # ── Row 1b: Custom date-range picker (hidden until "Custom" is selected) ──
        self._report_date_row = ctk.CTkFrame(inner, fg_color=COLORS["bg_panel"],
                                              corner_radius=8, border_width=1,
                                              border_color=COLORS["border"])
        # Not packed yet – shown only when Custom period is active

        ctk.CTkLabel(self._report_date_row, text="🗓  From:",
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=COLORS["text_secondary"]).pack(side="left", padx=(14, 4), pady=8)

        self._rpt_from_var = tk.StringVar()
        ctk.CTkEntry(self._report_date_row, textvariable=self._rpt_from_var,
                     width=110, height=32, corner_radius=7,
                     fg_color=COLORS["bg_hover"], border_color=COLORS["border"],
                     placeholder_text="YYYY-MM-DD",
                     font=ctk.CTkFont("Helvetica", 11)).pack(side="left", padx=(0, 4), pady=8)

        ctk.CTkButton(self._report_date_row, text="📅", width=32, height=32, corner_radius=7,
                      fg_color=COLORS["bg_hover"], hover_color=COLORS["border"],
                      text_color=COLORS["text_primary"], font=ctk.CTkFont("Helvetica", 13),
                      command=lambda: DatePickerPopup(
                          self, lambda d: self._rpt_from_var.set(d),
                          self._rpt_from_var.get() or None,
                      )).pack(side="left", padx=(0, 16), pady=8)

        ctk.CTkLabel(self._report_date_row, text="To:",
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=COLORS["text_secondary"]).pack(side="left", padx=(0, 4), pady=8)

        self._rpt_to_var = tk.StringVar()
        ctk.CTkEntry(self._report_date_row, textvariable=self._rpt_to_var,
                     width=110, height=32, corner_radius=7,
                     fg_color=COLORS["bg_hover"], border_color=COLORS["border"],
                     placeholder_text="YYYY-MM-DD",
                     font=ctk.CTkFont("Helvetica", 11)).pack(side="left", padx=(0, 4), pady=8)

        ctk.CTkButton(self._report_date_row, text="📅", width=32, height=32, corner_radius=7,
                      fg_color=COLORS["bg_hover"], hover_color=COLORS["border"],
                      text_color=COLORS["text_primary"], font=ctk.CTkFont("Helvetica", 13),
                      command=lambda: DatePickerPopup(
                          self, lambda d: self._rpt_to_var.set(d),
                          self._rpt_to_var.get() or None,
                      )).pack(side="left", padx=(0, 10), pady=8)

        ctk.CTkLabel(self._report_date_row,
                     text="Slots auto-selected: daily ≤31 days · weekly ≤91 days · monthly otherwise",
                     font=ctk.CTkFont("Helvetica", 9),
                     text_color=COLORS["text_muted"]).pack(side="left", padx=(4, 16), pady=8)

        # ── Row 2: results display ──
        row2 = ctk.CTkFrame(inner, fg_color=COLORS["bg_panel"],
                             corner_radius=10, border_width=1,
                             border_color=COLORS["border"])
        row2.pack(fill="x", pady=(16, 0))

        # Period label
        self.report_period_lbl = ctk.CTkLabel(
            row2, text="—  Select a period and item, then click Generate Report",
            font=ctk.CTkFont("Helvetica", 11),
            text_color=COLORS["text_muted"],
        )
        self.report_period_lbl.pack(anchor="w", padx=16, pady=(12, 0))

        # Metric cards row
        metrics_row = ctk.CTkFrame(row2, fg_color="transparent")
        metrics_row.pack(fill="x", padx=12, pady=12)

        def _metric(parent_frame, label, attr):
            card = ctk.CTkFrame(parent_frame, fg_color=COLORS["bg_card"],
                                corner_radius=10, border_width=1,
                                border_color=COLORS["border"])
            card.pack(side="left", fill="both", expand=True, padx=4)
            ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont("Helvetica", 11),
                         text_color=COLORS["text_muted"]).pack(pady=(10, 2))
            val_lbl = ctk.CTkLabel(card, text="—",
                                   font=ctk.CTkFont("Helvetica", 24, "bold"),
                                   text_color=COLORS["accent_glow"])
            val_lbl.pack(pady=(0, 10))
            setattr(self, attr, val_lbl)

        _metric(metrics_row, "📦  Total Units Sold", "report_qty_lbl")
        _metric(metrics_row, "💰  Total Revenue",    "report_rev_lbl")
        _metric(metrics_row, "📅  Period",           "report_range_lbl")

        # Breakdown treeview (per-day/per-week/per-month)
        breakdown_frame = ctk.CTkFrame(row2, fg_color="transparent")
        breakdown_frame.pack(fill="x", padx=12, pady=(0, 12))

        br_cols = ("Period", "Units Sold", "Revenue (₵)")
        self.report_tree = ttk.Treeview(
            breakdown_frame, columns=br_cols, show="headings",
            height=6, style="Custom.Treeview",
        )
        for col, w in zip(br_cols, [200, 120, 160]):
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=w, anchor="center")
        br_scroll = ttk.Scrollbar(breakdown_frame, orient="vertical",
                                  command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=br_scroll.set)
        br_scroll.pack(side="right", fill="y")
        self.report_tree.pack(fill="x")

    def _refresh_item_report_items(self):
        """Update the item combo-box list for the current user's access scope."""
        if self.current_role in ("admin", "root_admin"):
            names = sorted({row[2] for row in self.db.get_all_products(store=None)})
        else:
            names = self.db.get_all_item_names(store=self.active_store)
        self.report_item_combo.configure(values=names if names else ["(no transactions yet)"])
        if names and not self.report_item_var.get():
            self.report_item_var.set(names[0])

    def _run_item_report(self):
        """Query the DB and populate the report results panel."""
        import calendar as _cal
        item_name = self.report_item_var.get().strip()
        period    = self.report_period_var.get()

        if not item_name or item_name == "(no transactions yet)":
            messagebox.showwarning("No Item Selected", "Please select an item from the list.")
            return

        today      = datetime.date.today()
        date_slots: list[tuple[str, str, str]] = []  # (slot_label, date_from, date_to)
        period_display = period
        date_from = date_to = None  # set explicitly for Custom; derived from slots otherwise

        if period == "Custom":
            from_str = self._rpt_from_var.get().strip()
            to_str   = self._rpt_to_var.get().strip()
            if not from_str or not to_str:
                messagebox.showwarning("Date Required",
                                       "Please enter both From and To dates for the custom range.")
                return
            try:
                cust_from = datetime.date.fromisoformat(from_str)
                cust_to   = datetime.date.fromisoformat(to_str)
            except ValueError:
                messagebox.showerror("Invalid Date",
                                     "Dates must be in YYYY-MM-DD format (e.g. 2024-01-15).")
                return
            if cust_from > cust_to:
                messagebox.showerror("Invalid Range", "'From' date must be on or before 'To' date.")
                return

            span = (cust_to - cust_from).days + 1
            if span <= 31:
                slot_label = "daily"
                d = cust_from
                while d <= cust_to:
                    label = d.strftime("%Y-%m-%d")
                    date_slots.append((label, label, label))
                    d += datetime.timedelta(days=1)
            elif span <= 91:
                slot_label = "weekly"
                week_start = cust_from - datetime.timedelta(days=cust_from.weekday())
                while week_start <= cust_to:
                    week_end  = week_start + datetime.timedelta(days=6)
                    slot_from = max(week_start, cust_from).isoformat()
                    slot_to   = min(week_end,   cust_to).isoformat()
                    label = f"Week {week_start.strftime('%d %b')} – {week_end.strftime('%d %b %Y')}"
                    date_slots.append((label, slot_from, slot_to))
                    week_start += datetime.timedelta(weeks=1)
            else:
                slot_label = "monthly"
                yr, mo = cust_from.year, cust_from.month
                while datetime.date(yr, mo, 1) <= cust_to:
                    _, last = _cal.monthrange(yr, mo)
                    m_start = max(datetime.date(yr, mo, 1),    cust_from).isoformat()
                    m_end   = min(datetime.date(yr, mo, last), cust_to).isoformat()
                    label   = datetime.date(yr, mo, 1).strftime("%B %Y")
                    date_slots.append((label, m_start, m_end))
                    mo += 1
                    if mo > 12:
                        mo, yr = 1, yr + 1

            period_display = f"Custom ({slot_label})"
            date_from = cust_from.isoformat()
            date_to   = cust_to.isoformat()

        elif period == "Daily":
            # Last 30 days, one slot per day
            for d in range(30):
                day = today - datetime.timedelta(days=d)
                label = day.strftime("%Y-%m-%d")
                date_slots.append((label, label, label))

        elif period == "Weekly":
            # Last 12 complete weeks + current week
            for w in range(12):
                week_start = today - datetime.timedelta(days=today.weekday() + 7 * w)
                week_end   = week_start + datetime.timedelta(days=6)
                label = f"Week {week_start.strftime('%d %b')} – {week_end.strftime('%d %b %Y')}"
                date_slots.append((label, week_start.isoformat(), week_end.isoformat()))

        else:  # Monthly — fixed to use calendar.monthrange
            # Last 12 months
            for m in range(12):
                year  = today.year
                month = today.month - m
                while month <= 0:
                    month += 12
                    year  -= 1
                first = datetime.date(year, month, 1)
                _, last = _cal.monthrange(year, month)
                last_day = datetime.date(year, month, last)
                label = first.strftime("%B %Y")
                date_slots.append((label, first.isoformat(), last_day.isoformat()))

        if date_from is None:
            date_from = date_slots[-1][1]
            date_to   = date_slots[0][2]

        total_qty, total_rev = self.db.get_item_report(
            item_name, date_from, date_to, store=self.active_store
        )

        # Update metric cards
        self.report_qty_lbl.configure(text=str(total_qty))
        self.report_rev_lbl.configure(text=f"₵{total_rev:,.2f}")
        self.report_range_lbl.configure(text=f"{date_from}  →  {date_to}")
        self.report_period_lbl.configure(
            text=f"  {period_display} breakdown for  '{item_name}'"
        )

        # Clear and fill breakdown tree  (skip zero rows)
        for row in self.report_tree.get_children():
            self.report_tree.delete(row)
        for label, d_from, d_to in date_slots:
            qty, rev = self.db.get_item_report(
                item_name, d_from, d_to, store=self.active_store
            )
            if qty > 0:
                self.report_tree.insert("", "end", values=(label, qty, f"{rev:,.2f}"))

    def _build_product_management(self, parent):
        self.prod_scroll = ctk.CTkScrollableFrame(parent, fg_color=COLORS["bg_dark"], corner_radius=0)
        self.prod_scroll.pack(fill="both", expand=True, padx=8, pady=8)
        self._build_product_management_content()

    def _build_product_management_content(self):
        self.product_frames = []
        # Add new product button
        add_btn = ctk.CTkButton(self.prod_scroll, text="+ Add New Product", height=38, corner_radius=10, fg_color=COLORS["success"], hover_color="#059669", text_color="white", font=ctk.CTkFont("Helvetica", 12, "bold"), command=self._add_new_product)
        add_btn.pack(pady=(12, 20), padx=10, fill="x")
        for cat, items in self.menu_data.items():
            # Category header
            cat_label = ctk.CTkLabel(self.prod_scroll, text=cat, font=ctk.CTkFont("Helvetica", 16, "bold"), text_color=COLORS["accent_glow"])
            cat_label.pack(anchor="w", pady=(16, 8), padx=10)
            for item in items:
                item_frame = ctk.CTkFrame(self.prod_scroll, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
                item_frame.pack(fill="x", padx=4, pady=3)
                # Name
                name_label = ctk.CTkLabel(item_frame, text=item['name'], font=ctk.CTkFont("Helvetica", 12, "bold"), text_color=COLORS["text_primary"])
                name_label.pack(side="left", padx=12, pady=10)
                # Stock quantity badge
                qty = item.get('quantity', 0)
                qty_color = COLORS["success"] if qty > 0 else COLORS["error"]
                qty_label = ctk.CTkLabel(item_frame, text=f"Stock: {qty}", font=ctk.CTkFont("Helvetica", 10, "bold"), text_color=qty_color)
                qty_label.pack(side="left", padx=8, pady=10)
                # Current price
                price_var = ctk.StringVar(value=f"{item['price']:.2f}")
                price_entry = ctk.CTkEntry(item_frame, textvariable=price_var, width=80, fg_color=COLORS["bg_hover"], border_color=COLORS["border"])
                price_entry.pack(side="right", padx=10, pady=10)
                # Save button
                save_btn = ctk.CTkButton(item_frame, text="Save", width=65, height=32, corner_radius=7, fg_color=COLORS["success"], text_color="white", font=ctk.CTkFont("Helvetica", 11, "bold"), command=lambda i=item, v=price_var: self._update_product_price(i, v))
                save_btn.pack(side="right", padx=5, pady=10)
                # Edit button
                edit_btn = ctk.CTkButton(item_frame, text="Edit", width=65, height=32, corner_radius=7, fg_color=COLORS["warning"], text_color="white", font=ctk.CTkFont("Helvetica", 11, "bold"), command=lambda i=item: self._edit_product(i))
                edit_btn.pack(side="right", padx=5, pady=10)
                # Delete button
                delete_btn = ctk.CTkButton(item_frame, text="Delete", width=65, height=32, corner_radius=7, fg_color=COLORS["error"], text_color="white", font=ctk.CTkFont("Helvetica", 11, "bold"), command=lambda i=item: self._delete_product(i))
                delete_btn.pack(side="right", padx=5, pady=10)
                self.product_frames.append((item_frame, price_var))

    def _update_product_price(self, item, price_var):
        if self.current_role != "admin":
            messagebox.showerror("Access Denied", "Only admin accounts can edit item prices.")
            return
        try:
            old_price = float(item['price'])
            new_price = float(price_var.get())
            store = item.get('store', self.active_store)
            self.db.update_product(item['id'], item['category'], item['name'], new_price, item['desc'], store)
            self.menu_data = self._load_menu()
            self.db.log_activity(
                self.current_user or "unknown",
                self.current_role or "admin",
                "UPDATE_PRICE",
                item['name'],
                f"{old_price:.2f} -> {new_price:.2f}",
                store=store,
            )
            messagebox.showinfo("Success", f"Price updated for {item['name']}")
            self._refresh_product_management()
        except ValueError:
            messagebox.showerror("Error", "Invalid price")

    def _delete_product(self, item):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item['name']}'?"):
            store = item.get('store', self.active_store)
            self.db.delete_product(item['id'])
            self.menu_data = self._load_menu()
            self.db.log_activity(
                self.current_user or "unknown",
                self.current_role or "admin",
                "DELETE_PRODUCT",
                item['name'],
                f"category={item.get('category', '')}",
                store=store or "system",
            )
            self._refresh_product_management()

    def _refresh_product_management(self):
        # Clear efficiently
        for widget in self.prod_scroll.winfo_children():
            widget.destroy()
        self._build_product_management_content()

    def _build_user_management(self, parent):
        self.user_scroll = ctk.CTkScrollableFrame(parent, fg_color=COLORS["bg_dark"], corner_radius=0)
        self.user_scroll.pack(fill="both", expand=True, padx=8, pady=8)
        self._refresh_user_management()

    def _refresh_user_management(self):
        if hasattr(self, "user_scroll"):
            for w in self.user_scroll.winfo_children():
                w.destroy()

        users = self.db.get_users(self.active_store) if self.active_store else []

        for uid, role, username, password in users:
            user_frame = ctk.CTkFrame(self.user_scroll, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
            user_frame.pack(fill="x", padx=4, pady=3)

            ctk.CTkLabel(user_frame, text=f"{role.title()}", font=ctk.CTkFont("Helvetica", 12, "bold"), text_color=COLORS["accent_glow"]).pack(side="left", padx=12, pady=10)
            ctk.CTkLabel(user_frame, text=f"{username}", font=ctk.CTkFont("Helvetica", 12), text_color=COLORS["text_secondary"]).pack(side="left", padx=12, pady=10)
            ctk.CTkLabel(user_frame, text="•••••", font=ctk.CTkFont("Helvetica", 12), text_color=COLORS["text_muted"]).pack(side="left", padx=12, pady=10)

            edit_btn = ctk.CTkButton(user_frame, text="Edit", width=70, height=32, corner_radius=7, fg_color=COLORS["warning"], text_color="white", font=ctk.CTkFont("Helvetica", 11, "bold"),
                                     command=lambda u=(uid, role, username, password): self._edit_user(u))
            edit_btn.pack(side="right", padx=10, pady=10)

    def _edit_user(self, user_entry):
        uid, role, username, password = user_entry
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Edit {role.title()} Credentials")
        dialog.geometry("420x320")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color=COLORS["bg_dark"])

        ctk.CTkLabel(dialog, text=f"Role: {role.title()}").pack(pady=(14, 6))

        ctk.CTkLabel(dialog, text="Username:").pack(pady=(8, 2))
        username_entry = ctk.CTkEntry(dialog)
        username_entry.pack(fill="x", padx=20)
        username_entry.insert(0, username)

        ctk.CTkLabel(dialog, text="Password:").pack(pady=(8, 2))
        pwd_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        pwd_frame.pack(fill="x", padx=20)
        password_entry = ctk.CTkEntry(pwd_frame, show="*")
        password_entry.pack(side="left", fill="x", expand=True)
        password_entry.insert(0, password)

        def _toggle_user_password():
            if password_entry.cget("show") == "*":
                password_entry.configure(show="")
                toggle_btn.configure(text="Hide")
            else:
                password_entry.configure(show="*")
                toggle_btn.configure(text="Show")

        toggle_btn = ctk.CTkButton(pwd_frame, text="Show", width=70, command=_toggle_user_password)
        toggle_btn.pack(side="right", padx=(8, 0))

        strength_lbl = ctk.CTkLabel(dialog, text="", font=ctk.CTkFont("Helvetica", 10), text_color=COLORS["text_secondary"])
        strength_lbl.pack(fill="x", padx=20, pady=(4, 0))

        ctk.CTkLabel(dialog, text="Confirm Password:").pack(pady=(10, 2))
        confirm_entry = ctk.CTkEntry(dialog, show="*")
        confirm_entry.pack(fill="x", padx=20)
        confirm_entry.insert(0, password)

        def _update_strength(_=None):
            pwd = password_entry.get()
            score = 0
            if len(pwd) >= 8:
                score += 1
            if any(c.islower() for c in pwd) and any(c.isupper() for c in pwd):
                score += 1
            if any(c.isdigit() for c in pwd):
                score += 1
            if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in pwd):
                score += 1
            if not pwd:
                strength_lbl.configure(text="")
                return
            if score <= 1:
                strength_lbl.configure(text="Strength: Weak", text_color=COLORS["error"])
            elif score == 2:
                strength_lbl.configure(text="Strength: Fair", text_color=COLORS["warning"])
            else:
                strength_lbl.configure(text="Strength: Strong", text_color=COLORS["success"])

        password_entry.bind("<KeyRelease>", _update_strength)
        _update_strength()

        def save():
            new_user = username_entry.get().strip()
            new_pass = password_entry.get().strip()
            confirm_pass = confirm_entry.get().strip()
            if not new_user or not new_pass:
                messagebox.showerror("Error", "Username and password are required")
                return
            if new_pass != confirm_pass:
                messagebox.showerror("Error", "Passwords do not match")
                return
            self.db.add_or_update_user(self.active_store, role, new_user, new_pass, create_if_missing=True)
            self.db.log_activity(
                self.current_user or "unknown",
                self.current_role or "admin",
                "UPDATE_USER_CREDENTIALS",
                new_user,
                f"role={role}",
                store=self.active_store or "system",
            )
            self._refresh_user_management()
            dialog.destroy()

        btns = ctk.CTkFrame(dialog, fg_color="transparent")
        btns.pack(pady=12)
        ctk.CTkButton(btns, text="Save", width=100, command=save).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Cancel", width=100, command=dialog.destroy).pack(side="left", padx=6)

    def _show_profile_dialog(self):
        if not self.current_user:
            self._show_login()
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("User Profile")
        dialog.geometry("360x490")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.focus_force()
        dialog.configure(fg_color=COLORS["bg_dark"])
        dialog.update_idletasks()
        sw, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
        dialog.geometry(f"360x490+{(sw - 360) // 2}+{(sh - 490) // 2}")

        role = self.current_role or "attendant"
        role_color = {
            "admin": COLORS["accent"],
            "root_admin": COLORS["gold"],
            "attendant": COLORS["success"],
        }.get(role, COLORS["accent"])
        role_name = {
            "admin": "Admin",
            "root_admin": "Root Admin",
            "attendant": "Attendant",
        }.get(role, role.replace("_", " ").title())
        store_name = STORE_LABELS.get(self.active_store, self.active_store or "System")
        initial = self.current_user[0].upper()

        ctk.CTkFrame(dialog, fg_color="transparent", height=30).pack()

        # Avatar circle
        avatar = ctk.CTkFrame(dialog, fg_color=role_color,
                              width=84, height=84, corner_radius=42)
        avatar.pack()
        avatar.pack_propagate(False)
        ctk.CTkLabel(avatar, text=initial,
                     font=ctk.CTkFont("Helvetica", 38, "bold"),
                     text_color="#0A0E27").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkFrame(dialog, fg_color="transparent", height=14).pack()

        # Username
        ctk.CTkLabel(dialog, text=self.current_user,
                     font=ctk.CTkFont("Helvetica", 22, "bold"),
                     text_color=COLORS["text_primary"]).pack()

        # Role badge
        badge_row = ctk.CTkFrame(dialog, fg_color=role_color, corner_radius=12)
        badge_row.pack(pady=(6, 0))
        ctk.CTkLabel(badge_row, text=f"  {role_name}  ",
                     font=ctk.CTkFont("Helvetica", 11, "bold"),
                     text_color="#0A0E27").pack(padx=4, pady=4)

        ctk.CTkFrame(dialog, fg_color="transparent", height=8).pack()

        # Store
        ctk.CTkLabel(dialog, text=f"📍  {store_name}",
                     font=ctk.CTkFont("Helvetica", 12),
                     text_color=COLORS["text_secondary"]).pack()

        ctk.CTkFrame(dialog, fg_color=COLORS["border"], height=1).pack(
            fill="x", padx=32, pady=20)

        # Change Password button
        ctk.CTkButton(
            dialog, text="🔑  Change Password",
            height=42, corner_radius=10,
            fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
            border_width=1, border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            font=ctk.CTkFont("Helvetica", 12, "bold"),
            command=lambda: [dialog.destroy(), self._change_password_dialog()],
        ).pack(fill="x", padx=32, pady=(0, 10))

        # Sign Out button
        ctk.CTkButton(
            dialog, text="🚪  Sign Out",
            height=42, corner_radius=10,
            fg_color=COLORS["error"], hover_color="#DC2626",
            text_color="white",
            font=ctk.CTkFont("Helvetica", 12, "bold"),
            command=lambda: [dialog.destroy(), self._logout_admin()],
        ).pack(fill="x", padx=32, pady=(0, 10))

        # Close button
        ctk.CTkButton(
            dialog, text="Close",
            height=36, corner_radius=10,
            fg_color="transparent", hover_color=COLORS["bg_hover"],
            border_width=1, border_color=COLORS["border"],
            text_color=COLORS["text_muted"],
            font=ctk.CTkFont("Helvetica", 11),
            command=dialog.destroy,
        ).pack(fill="x", padx=32)

    def _change_password_dialog(self):
        if not self.current_user:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Change Password")
        dialog.geometry("360x400")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.focus_force()
        dialog.configure(fg_color=COLORS["bg_dark"])
        dialog.update_idletasks()
        sw, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
        dialog.geometry(f"360x400+{(sw - 360) // 2}+{(sh - 400) // 2}")

        ctk.CTkFrame(dialog, fg_color="transparent", height=24).pack()
        ctk.CTkLabel(dialog, text="🔑  Change Password",
                     font=ctk.CTkFont("Helvetica", 18, "bold"),
                     text_color=COLORS["text_primary"]).pack()
        ctk.CTkLabel(dialog, text=f"Account: {self.current_user}",
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=COLORS["text_muted"]).pack(pady=(4, 18))

        def _lbl(text):
            ctk.CTkLabel(dialog, text=text,
                         font=ctk.CTkFont("Helvetica", 10, "bold"),
                         text_color=COLORS["text_muted"]).pack(anchor="w", padx=32)
            ctk.CTkFrame(dialog, fg_color="transparent", height=4).pack()

        _lbl("CURRENT PASSWORD")
        cur_entry = ctk.CTkEntry(dialog, placeholder_text="Current password",
                                  show="*", height=42, corner_radius=8,
                                  border_color=COLORS["border"],
                                  fg_color=COLORS["bg_card"],
                                  text_color=COLORS["text_primary"])
        cur_entry.pack(fill="x", padx=32, pady=(0, 10))

        _lbl("NEW PASSWORD")
        new_entry = ctk.CTkEntry(dialog, placeholder_text="New password",
                                  show="*", height=42, corner_radius=8,
                                  border_color=COLORS["border"],
                                  fg_color=COLORS["bg_card"],
                                  text_color=COLORS["text_primary"])
        new_entry.pack(fill="x", padx=32, pady=(0, 10))

        _lbl("CONFIRM NEW PASSWORD")
        conf_entry = ctk.CTkEntry(dialog, placeholder_text="Confirm new password",
                                   show="*", height=42, corner_radius=8,
                                   border_color=COLORS["border"],
                                   fg_color=COLORS["bg_card"],
                                   text_color=COLORS["text_primary"])
        conf_entry.pack(fill="x", padx=32, pady=(0, 8))

        status_lbl = ctk.CTkLabel(dialog, text="",
                                   font=ctk.CTkFont("Helvetica", 11),
                                   text_color=COLORS["error"])
        status_lbl.pack(anchor="w", padx=32, pady=(0, 10))

        def _save():
            cur_pw  = cur_entry.get().strip()
            new_pw  = new_entry.get().strip()
            conf_pw = conf_entry.get().strip()
            if not cur_pw or not new_pw or not conf_pw:
                status_lbl.configure(text="⚠  All fields are required.")
                return
            if new_pw != conf_pw:
                status_lbl.configure(text="✖  New passwords do not match.")
                return
            if len(new_pw) < 4:
                status_lbl.configure(text="⚠  Minimum 4 characters required.")
                return
            store = self.active_store or "system"
            role  = self.current_role
            if not self.db.authenticate_user(store, role, self.current_user, cur_pw):
                status_lbl.configure(text="✖  Current password is incorrect.")
                cur_entry.delete(0, "end")
                return
            self.db.add_or_update_user(store, role, self.current_user, new_pw)
            self.db.log_activity(self.current_user, role, "CHANGE_PASSWORD",
                                 self.current_user, "Password changed", store=store)
            dialog.destroy()
            messagebox.showinfo("Success", "Password changed successfully.")

        ctk.CTkButton(
            dialog, text="Update Password",
            height=42, corner_radius=10,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_glow"],
            text_color="#0A0E27",
            font=ctk.CTkFont("Helvetica", 12, "bold"),
            command=_save,
        ).pack(fill="x", padx=32)

    def _logout_admin(self):
        # Reset state and return to login screen
        actor_user = self.current_user
        actor_role = self.current_role
        actor_store = self.active_store
        if actor_user and actor_role:
            self.db.log_activity(
                actor_user,
                actor_role,
                "LOGOUT",
                actor_user,
                "",
                store=actor_store or "system",
            )
        self.current_role = None
        self.current_user = None
        self.admin_logged_in = False
        self.root_logged_in = False
        self.active_store = None
        self.active_category = None
        self.menu_data = {}
        self.order_items.clear()
        self._refresh_order_panel()
        self._apply_role_permissions()
        self._show_login()

    def _add_new_product(self):
        self._product_dialog()

    def _edit_product(self, product):
        if self.current_role != "admin":
            messagebox.showerror("Access Denied", "Only admin accounts can edit products.")
            return
        self._product_dialog(product)

    def _product_dialog(self, product=None):
        if self.current_role != "admin":
            messagebox.showerror("Access Denied", "Only admin accounts can modify products.")
            return
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Product" if product is None else "Edit Product")
        dialog.geometry("420x440")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color=COLORS["bg_dark"])

        # Determine which store this product belongs to (fast food or cold store)
        store = product.get('store', self.active_store) if product else self.active_store
        store_menu = STORE_MENUS.get(store, {})

        # Category
        ctk.CTkLabel(dialog, text="Category:").pack(pady=5)
        cat_values = list(store_menu.keys())
        cat_var = ctk.StringVar(value=product['category'] if product else (cat_values[0] if cat_values else ""))
        cat_combo = ctk.CTkComboBox(dialog, values=cat_values, variable=cat_var)
        cat_combo.pack(pady=5)

        # Name
        ctk.CTkLabel(dialog, text="Name:").pack(pady=5)
        name_entry = ctk.CTkEntry(dialog)
        name_entry.pack(pady=5)
        if product:
            name_entry.insert(0, product['name'])

        # Price
        ctk.CTkLabel(dialog, text="Price:").pack(pady=5)
        price_entry = ctk.CTkEntry(dialog)
        price_entry.pack(pady=5)
        if product:
            price_entry.insert(0, str(product['price']))

        # Quantity in Stock
        ctk.CTkLabel(dialog, text="Quantity in Stock:").pack(pady=5)
        qty_entry = ctk.CTkEntry(dialog)
        qty_entry.pack(pady=5)
        if product:
            qty_entry.insert(0, str(product.get('quantity', 0)))
        else:
            qty_entry.insert(0, "0")

        # Desc
        ctk.CTkLabel(dialog, text="Description:").pack(pady=5)
        desc_entry = ctk.CTkEntry(dialog)
        desc_entry.pack(pady=5)
        if product:
            desc_entry.insert(0, product.get('desc', ''))

        # Buttons
        def save():
            try:
                cat = cat_var.get()
                name = name_entry.get().strip()
                price = float(price_entry.get())
                quantity = int(qty_entry.get().strip() or "0")
                desc = desc_entry.get().strip()
                if not name:
                    raise ValueError("Name required")
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative")
                if product:
                    action = "EDIT_PRODUCT"
                    target = product['name']
                    self.db.update_product(product['id'], cat, name, price, desc, quantity, store)
                else:
                    action = "ADD_PRODUCT"
                    target = name
                    self.db.add_product(cat, name, price, desc, quantity, store)
                self.menu_data = self._load_menu()
                self.db.log_activity(
                    self.current_user or "unknown",
                    self.current_role or "admin",
                    action,
                    target,
                    f"category={cat}, price={price:.2f}, qty={quantity}",
                    store=store or "system",
                )
                self._render_category(self.active_category)
                if hasattr(self, 'prod_scroll'):
                    self._refresh_product_management()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Save", command=save).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)

    def _show_login(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"{APP_NAME}  —  Sign In")
        dialog.geometry("980x640")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.focus_force()
        dialog.configure(fg_color=COLORS["bg_dark"])

        # Centre on screen
        dialog.update_idletasks()
        sw, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
        dialog.geometry(f"980x640+{(sw - 980) // 2}+{(sh - 640) // 2}")

        # ── Shared state ──
        store_var = tk.StringVar(value=STORE_LABELS.get(
            self.active_store, list(STORE_LABELS.values())[0]))
        role_var = tk.StringVar(value="Attendant")

        # ── Logic helpers (widgets referenced lazily via closure) ──
        def _update_login_hint(*_):
            s_label = store_var.get()
            s_key   = next((k for k, v in STORE_LABELS.items() if v == s_label), None)
            if s_label == "System":
                s_key = "system"
            role = role_var.get().strip().lower().replace(" ", "_")
            if role == "root_admin":
                s_key = "system"
            creds = CREDENTIALS.get(s_key, {}).get(role)
            u = p = ""
            if creds:
                u, p = creds["user"], creds["pass"]
            elif role == "root_admin":
                u, p = "root_admin", "root123"
            username_entry.delete(0, "end")
            if u:
                username_entry.insert(0, u)
            password_entry.delete(0, "end")
            if p:
                password_entry.insert(0, p)
            status_lbl.configure(text="")

        def attempt_login():
            s_label  = store_var.get()
            s_key    = next((k for k, v in STORE_LABELS.items() if v == s_label), None)
            if s_label == "System":
                s_key = "system"
            role     = role_var.get().strip().lower().replace(" ", "_")
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if role == "root_admin":
                s_key = "system"
            if not username or not password:
                status_lbl.configure(text="⚠  Please enter your username and password.")
                return
            status_lbl.configure(text="")
            user_row = self.db.authenticate_user(s_key, role, username, password)
            if not user_row:
                status_lbl.configure(text="✖  Invalid credentials or account is disabled.")
                password_entry.delete(0, "end")
                password_entry.focus()
                return
            _user_id, user_store, user_role, user_name = user_row
            self.active_store    = user_store if user_role != "root_admin" else "system"
            self.current_role    = user_role
            self.current_user    = user_name
            self.admin_logged_in = (user_role == "admin")
            self.root_logged_in  = (user_role == "root_admin")
            self.menu_data       = self._load_menu()
            self.order_counter   = self._get_next_order_number()
            self.active_category = next(iter(self.menu_data.keys()), None)
            self.db.log_activity(user_name, user_role, "LOGIN", user_name,
                                 f"store={self.active_store}", store=self.active_store)
            self._apply_role_permissions()
            self._refresh_category_buttons()
            if self.active_category:
                self._select_category(self.active_category)
            self._refresh_order_panel()
            self.order_badge.configure(text=f"Order  # {self.order_counter:04d}")
            if user_role == "root_admin":
                self._show_view("root")
            elif user_role == "admin":
                self._show_view("admin")
            else:
                self._show_view("pos")
            dialog.destroy()

        # ════════════════ ROOT GRID: 2 columns ════════════════
        dialog.columnconfigure(0, weight=5)
        dialog.columnconfigure(1, weight=7)
        dialog.rowconfigure(0, weight=1)

        # ─────────────── LEFT — BRAND PANEL ───────────────
        brand = ctk.CTkFrame(dialog, fg_color=COLORS["bg_panel"],
                             corner_radius=0, border_width=0)
        brand.grid(row=0, column=0, sticky="nsew")

        # Cyan accent strip at top
        ctk.CTkFrame(brand, fg_color=COLORS["accent"], height=5,
                     corner_radius=0).pack(fill="x")

        ctk.CTkFrame(brand, fg_color="transparent", height=64).pack()

        ctk.CTkLabel(brand, text="🍔",
                     font=ctk.CTkFont("Helvetica", 72)).pack()

        ctk.CTkLabel(brand, text=APP_NAME,
                     font=ctk.CTkFont("Helvetica", 22, "bold"),
                     text_color=COLORS["accent_glow"]).pack(pady=(10, 2))

        ctk.CTkLabel(brand, text="Restaurant  •  Point of Sale",
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=COLORS["text_muted"]).pack(pady=(0, 36))

        ctk.CTkFrame(brand, fg_color=COLORS["border"], height=1).pack(fill="x", padx=30)
        ctk.CTkFrame(brand, fg_color="transparent", height=22).pack()

        for icon, info_text in [
            ("📍", "Airport Residential, Accra"),
            ("⏰", "24 / 7 Operations"),
            ("🔒", "Secured & Audited System"),
        ]:
            ir = ctk.CTkFrame(brand, fg_color="transparent")
            ir.pack(anchor="w", padx=30, pady=7)
            ctk.CTkLabel(ir, text=icon,
                         font=ctk.CTkFont("Helvetica", 13)).pack(side="left", padx=(0, 10))
            ctk.CTkLabel(ir, text=info_text,
                         font=ctk.CTkFont("Helvetica", 11),
                         text_color=COLORS["text_secondary"]).pack(side="left")

        ctk.CTkLabel(brand, text="ERP v2.0",
                     font=ctk.CTkFont("Helvetica", 9),
                     text_color=COLORS["text_muted"]).pack(side="bottom", pady=14)

        # ─────────────── RIGHT — FORM PANEL ───────────────
        form_outer = ctk.CTkFrame(dialog, fg_color=COLORS["bg_dark"], corner_radius=0)
        form_outer.grid(row=0, column=1, sticky="nsew")

        form = ctk.CTkScrollableFrame(form_outer, fg_color="transparent",
                                      corner_radius=0,
                                      scrollbar_button_color=COLORS["border"])
        form.pack(fill="both", expand=True)

        ctk.CTkFrame(form, fg_color="transparent", height=44).pack()

        ctk.CTkLabel(form, text="Welcome Back",
                     font=ctk.CTkFont("Helvetica", 28, "bold"),
                     text_color=COLORS["text_primary"]).pack(anchor="w", padx=40)

        ctk.CTkLabel(form, text="Select your role and sign in to continue",
                     font=ctk.CTkFont("Helvetica", 12),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=40, pady=(4, 26))

        def _field_label(text):
            ctk.CTkLabel(form, text=text,
                         font=ctk.CTkFont("Helvetica", 10, "bold"),
                         text_color=COLORS["text_muted"]).pack(anchor="w", padx=40)
            ctk.CTkFrame(form, fg_color="transparent", height=5).pack()

        # ── Store segmented selector ──
        _field_label("STORE")
        seg_outer = ctk.CTkFrame(form, fg_color=COLORS["bg_panel"], corner_radius=10,
                                 border_width=1, border_color=COLORS["border"])
        seg_outer.pack(fill="x", padx=40, pady=(0, 22))

        store_options = list(STORE_LABELS.values()) + ["System"]
        store_btns: dict[str, ctk.CTkButton] = {}

        def _pick_store(label: str):
            store_var.set(label)
            for lbl, sb in store_btns.items():
                active = lbl == label
                sb.configure(
                    fg_color=COLORS["accent"] if active else "transparent",
                    text_color="#0A0E27" if active else COLORS["text_secondary"],
                )
            _update_login_hint()

        for idx, s in enumerate(store_options):
            seg_outer.columnconfigure(idx, weight=1)
        for idx, s in enumerate(store_options):
            is_active = s == store_var.get()
            sb = ctk.CTkButton(
                seg_outer, text=s, height=38, corner_radius=8,
                fg_color=COLORS["accent"] if is_active else "transparent",
                hover_color=COLORS["bg_hover"],
                text_color="#0A0E27" if is_active else COLORS["text_secondary"],
                font=ctk.CTkFont("Helvetica", 12, "bold"),
                command=lambda l=s: _pick_store(l),
            )
            sb.grid(row=0, column=idx, padx=3, pady=3, sticky="ew")
            store_btns[s] = sb

        # ── Role card selector ──
        _field_label("LOGIN AS")
        role_row = ctk.CTkFrame(form, fg_color="transparent")
        role_row.pack(fill="x", padx=40, pady=(0, 22))

        role_cards: dict[str, tuple] = {}
        ROLE_DEF = [("Attendant", "🧑‍💼"), ("Admin", "📊"), ("Root Admin", "🛡️")]

        def _pick_role(r: str):
            role_var.set(r)
            for rname, (rf, ri, rl) in role_cards.items():
                active = rname == r
                rf.configure(
                    border_color=COLORS["accent"] if active else COLORS["border"],
                    fg_color=COLORS["bg_hover"] if active else COLORS["bg_card"],
                )
                ri.configure(text_color=COLORS["accent_glow"] if active else COLORS["text_secondary"])
                rl.configure(text_color=COLORS["accent_glow"] if active else COLORS["text_secondary"])
            _update_login_hint()

        for col, (rname, ricon) in enumerate(ROLE_DEF):
            role_row.columnconfigure(col, weight=1)

        for col, (rname, ricon) in enumerate(ROLE_DEF):
            first = col == 0
            rf = ctk.CTkFrame(
                role_row,
                fg_color=COLORS["bg_hover"] if first else COLORS["bg_card"],
                corner_radius=14, border_width=2,
                border_color=COLORS["accent"] if first else COLORS["border"],
                cursor="hand2",
            )
            rf.grid(row=0, column=col, padx=5, sticky="ew")

            ri = ctk.CTkLabel(rf, text=ricon, font=ctk.CTkFont("Helvetica", 32),
                               text_color=COLORS["accent_glow"] if first else COLORS["text_secondary"])
            ri.pack(pady=(18, 4))

            rl = ctk.CTkLabel(rf, text=rname, font=ctk.CTkFont("Helvetica", 11, "bold"),
                               text_color=COLORS["accent_glow"] if first else COLORS["text_secondary"])
            rl.pack(pady=(0, 18))

            role_cards[rname] = (rf, ri, rl)
            for w in (rf, ri, rl):
                w.bind("<Button-1>", lambda e, rx=rname: _pick_role(rx))

        # ── Username field ──
        _field_label("USERNAME")
        username_entry = ctk.CTkEntry(
            form,
            placeholder_text="Enter your username",
            height=46, corner_radius=10,
            border_color=COLORS["border"], fg_color=COLORS["bg_card"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_muted"],
            font=ctk.CTkFont("Helvetica", 13),
        )
        username_entry.pack(fill="x", padx=40, pady=(0, 18))

        # ── Password field with eye toggle ──
        _field_label("PASSWORD")
        pwd_row_frame = ctk.CTkFrame(form, fg_color="transparent")
        pwd_row_frame.pack(fill="x", padx=40, pady=(0, 4))
        pwd_row_frame.columnconfigure(0, weight=1)

        password_entry = ctk.CTkEntry(
            pwd_row_frame,
            placeholder_text="Enter your password",
            show="*", height=46, corner_radius=10,
            border_color=COLORS["border"], fg_color=COLORS["bg_card"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_muted"],
            font=ctk.CTkFont("Helvetica", 13),
        )
        password_entry.grid(row=0, column=0, sticky="ew")

        def _toggle_password():
            if password_entry.cget("show") == "*":
                password_entry.configure(show="")
                eye_btn.configure(text="🙈")
            else:
                password_entry.configure(show="*")
                eye_btn.configure(text="👁")

        eye_btn = ctk.CTkButton(
            pwd_row_frame, text="👁",
            width=46, height=46, corner_radius=10,
            fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
            border_width=1, border_color=COLORS["border"],
            text_color=COLORS["text_secondary"],
            font=ctk.CTkFont("Helvetica", 18),
            command=_toggle_password,
        )
        eye_btn.grid(row=0, column=1, padx=(8, 0))

        # ── Inline status / error ──
        status_lbl = ctk.CTkLabel(form, text="",
                                   font=ctk.CTkFont("Helvetica", 11),
                                   text_color=COLORS["error"])
        status_lbl.pack(anchor="w", padx=40, pady=(8, 14))

        # ── Sign In button ──
        ctk.CTkButton(
            form, text="Sign In  →",
            height=52, corner_radius=12,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_glow"],
            text_color="#0A0E27",
            font=ctk.CTkFont("Helvetica", 15, "bold"),
            command=attempt_login,
        ).pack(fill="x", padx=40, pady=(0, 16))

        # ── Footer ──
        ctk.CTkLabel(form,
                     text=f"{APP_NAME}  •  ERP v2.0  •  All rights reserved",
                     font=ctk.CTkFont("Helvetica", 9),
                     text_color=COLORS["text_muted"]).pack(pady=(0, 20))

        # ── Key bindings & initialise hint ──
        username_entry.bind("<Return>", lambda e: password_entry.focus())
        password_entry.bind("<Return>", lambda e: attempt_login())
        _update_login_hint()

        dialog.update()
        self.wait_window(dialog)

    def _check_admin_access(self):
        if self.current_role == "admin":
            self._show_view("admin")
        else:
            messagebox.showinfo("Admin Only", "Please log in as an admin to access the dashboard.")
            self._show_login()

    def _check_root_admin_access(self):
        if self.current_role == "root_admin":
            self._show_view("root")
        else:
            messagebox.showinfo("Root Admin Only", "Please log in as root admin to access this dashboard.")
            self._show_login()


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = BlazeBiteApp()
    app.mainloop()
