# Cafe POS

A simple point-of-sale system for an Indian cafe, built with Python Flask and PostgreSQL.

## Features

- **Menu display** — Grid of items by category (Beverages, Food, Snacks)
- **Order creation** — Tap items to add to order, adjust quantities
- **Bill generation** — Calculate subtotal + 5% GST (Indian cafe standard)
- **Order history** — View recent orders with status (pending/prepared/paid)
- **Quick stats** — Today's sales total and order count in header
- **Admin controls** — Add new items, enable/disable menu items
- **Payment modal** — Cash or card payment selection
- **Print modal** — Preview and confirm bill before printing

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

## Quick Start

```bash
# 1. Start PostgreSQL
brew services start postgresql@16

# 2. Create database
createdb cafe_pos

# 3. Run the app
cd pos
/usr/bin/python3 app.py

# 4. Open in browser
http://127.0.0.1:5555
```

## GitHub

Repository: https://github.com/chaitanyasunny/pos-cafe-india.git
