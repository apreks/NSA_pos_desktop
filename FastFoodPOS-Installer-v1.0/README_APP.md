# 🔥 BlazeBite Fast-Food ERP — Run Guide

## Requirements
- Python 3.10 or higher
- pip (comes with Python)

---

## ⚡ Quick Start (3 steps)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python main.py
```

> The SQLite database file (`blazebite.db`) is created automatically
> in the same folder on first run. No setup needed.

---

## 📦 Build Executable (Windows)

This project now includes a one-click build script and a PyInstaller spec file.

### One-click build

Double-click `build_exe.bat` in the project folder.

It will:
- activate `.venv`
- install/update `pyinstaller`
- build with `FastFoodPOS.spec`

### Output

After a successful build, use:

`dist/FastFoodPOS/FastFoodPOS.exe`

Copy the entire `dist/FastFoodPOS` folder to another Windows computer, then run the `.exe`.

---

## 🖥️ Features

| Feature | Details |
|---------|---------|
| **Digital Menu** | 4 categories (Burgers, Sides, Drinks, Desserts), 22 items |
| **Real-time Order** | Add/remove items with live subtotal |
| **Auto Tax** | 15% tax calculated instantly |
| **Checkout + Invoice** | Formatted receipt; saved as `.txt` on "Print" |
| **Payment Methods** | Cash · Card · Mobile |
| **SQLite Database** | Every transaction logged automatically |
| **Admin Dashboard** | Daily revenue card, all-time stats, full history table |

---

## 📁 File Structure

```
fast_food_erp/
├── main.py          ← The full application (single file)
├── requirements.txt ← One dependency: customtkinter
├── README.md        ← This file
└── blazebite.db     ← Auto-created SQLite database
```

---

## 🔧 Customisation Tips

- **Change restaurant name**: edit `APP_NAME` near line 20
- **Change tax rate**: edit `TAX_RATE` (e.g. `0.10` for 10%)
- **Add menu items**: add dicts to the `MENU` dictionary
- **Change accent color**: edit `COLORS["accent"]`

---

## 🗂️ Database Schema

Table: `transactions`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto PK |
| date | TEXT | YYYY-MM-DD |
| time | TEXT | HH:MM:SS |
| items_json | TEXT | JSON array of items sold |
| subtotal | REAL | Before tax |
| tax | REAL | 15% tax amount |
| total | REAL | Final amount charged |
| payment_method | TEXT | Cash / Card / Mobile |
| order_number | INTEGER | Sequential order ID |

You can open `blazebite.db` with any SQLite viewer (e.g. DB Browser for SQLite).
