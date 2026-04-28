# Cafe POS

A simple point-of-sale system for an Indian cafe, built with Python Flask and PostgreSQL.

## Features

- **Visual menu display** — Grid of items by category with emoji icons; includes **Desserts**
- **Polished POS UI** — Improved header, cards, spacing, controls, and responsive layout for counter/tablet usage
- **Search UX** — Search above category tabs with cleaner input UI, working clear button, and keyboard shortcuts (`/` focus, `Esc` clear)
- **Order creation** — Tap items to add to order, adjust quantities with +/- buttons; **table number** on the order panel for service routing
- **Kitchen ticket & billing** — Preview a draft ticket, then **Send to kitchen** to save as `pending`; **Pay** saves as `paid` in one step; receipt shows the **server order number** (unique `ORD-HHMMSS-###`)
- **Bill generation** — Calculate subtotal + 18% GST; stored order totals are pre-GST line items
- **Order history** — View recent orders with status (pending/prepared/paid)
- **Quick stats + live clock** — Today's sales total, pending count, order count, and live current time in header
- **Admin controls with lock** — Add items and manage availability behind lightweight lock/unlock password gate
- **Payment modal** — Cash, Card/UPI, or QR code selection with live bill preview
- **Kitchen ticket modal** — Draft/saved states with enhanced real-time bill details
- **Manage Menu** — Toggle switches for quick enable/disable of items
- **Receipt quality** — Receipt includes branding details (name/address/GSTIN/phone), payment method, cashier name
- **Thermal printing** — 58mm / 80mm paper-size selector; **Print receipt** outputs receipt-only content (not the full web page)

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

## Receipt Configuration

Current receipt brand details are set in `templates/index.html` via `RECEIPT_BRAND`:

- `name`
- `address`
- `gstin`
- `phone`

You can update these values to match your cafe identity and compliance details.

## GitHub

Repository: https://github.com/chaitanyasunny/pos-cafe-india.git
