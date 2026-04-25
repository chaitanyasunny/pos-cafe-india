# Cafe POS

A simple point-of-sale system for an Indian cafe, built with Python Flask and PostgreSQL.

## Features

- **Visual menu display** — Grid of items by category with emoji icons; **search** above the tabs (category + text filter); includes **Desserts** among categories
- **Order creation** — Tap items to add to order, adjust quantities with +/- buttons; **table number** on the order panel for service routing
- **Kitchen ticket & billing** — Preview a draft ticket, then **Send to kitchen** to save as `pending`; **Pay** saves as `paid` in one step; receipt shows the **server order number** (unique `ORD-HHMMSS-###`)
- **Bill generation** — Calculate subtotal + 18% GST; stored order totals are pre-GST line items
- **Order history** — View recent orders with status (pending/prepared/paid)
- **Quick stats** — Today's sales total, pending count, order count in header
- **Admin controls** — Add new items with emoji picker, toggle enable/disable menu items
- **Payment modal** — Cash, Card/UPI, or QR code payment selection
- **Kitchen ticket modal** — Draft vs sent state, backdrop click to dismiss, optional **Print receipt**
- **Manage Menu** — Toggle switches for quick enable/disable of items

## Tech Stack

- Backend: Python Flask + SQLAlchemy
- Database: PostgreSQL (local)
- Frontend: Vanilla HTML/CSS/JS
- Currency: INR (Indian Rupees, stored in paisa)

## Project Structure

```
pos/
├── app.py              # Flask backend, API routes, DB models
├── templates/
│   └── index.html      # POS frontend
├── SPEC.md             # Project specification
├── README.md           # This file
├── USAGE.md            # How to run and operate the POS
├── DEBUG.md            # Debugging guide
└── .gitignore         # Excludes memory files, venv, __pycache__
```

## Prerequisites

- Python 3.9+
- PostgreSQL 16+
- Homebrew (for PostgreSQL installation on macOS)

Install Python dependencies (from the project directory):

```bash
pip install flask flask-sqlalchemy psycopg2-binary pytz
```

## Quick Start

```bash
# 1. Start PostgreSQL
brew services start postgresql@16

# 2. Create database
createdb cafe_pos

# 3. Run the app (use your clone path)
cd /path/to/pos
/usr/bin/python3 app.py

# 4. Open in browser
http://127.0.0.1:5555
```

## GitHub

Repository: https://github.com/chaitanyasunny/pos-cafe-india.git
