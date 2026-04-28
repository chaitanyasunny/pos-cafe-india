# Cafe POS

**A point-of-sale system built for the rhythm of an Indian cafe.**

Flask + PostgreSQL backend, vanilla HTML/CSS/JS frontend. No dependencies, no build step — just open and run.

---

## What's inside

### Interface

| Feature | Details |
|---|---|
| **Menu grid** | Items grouped by category (Beverages, Food, Snacks, Desserts) with emoji icons |
| **Order panel** | Table number, line items with +/− controls, live subtotal + GST calculation |
| **Search** | `/` to focus, `Esc` to clear — keyboard-first UX |
| **Stats header** | Today's sales, pending count, order count, live clock |
| **Manage Menu** | Toggle switches for availability — no extra buttons |

### Workflows

- **Send to Kitchen** — saves order as `pending`, opens kitchen ticket modal with enhanced bill preview
- **Pay** — single-step create with `status: paid`, choose Cash/Card/UPI/QR, opens receipt modal
- **Print Receipt** — dedicated receipt layout (not full page), thermal size selector (58mm / 80mm)

### Admin

- Lock/unlock password gate blocks Add Item, Manage Menu, and availability toggles
- Add Item modal with emoji picker for icon selection
- Cashier name captured on payment for receipt tracking

### Receipt

Receipts include: cafe name, address, GSTIN, phone, order number, items, payment method, cashier name, timestamp

---

## Tech stack

```
Backend    Python Flask + SQLAlchemy
Database   PostgreSQL 16 (local)
Frontend   Vanilla HTML + CSS + JS
Currency   INR stored in paisa (1 INR = 100 paisa)
Timezone   IST via pytz
```

---

## Quick start

```bash
# 1. Start PostgreSQL
brew services start postgresql@16

# 2. Create database
createdb cafe_pos

# 3. Run
cd /path/to/pos
/usr/bin/python3 app.py

# 4. Open
open http://127.0.0.1:5555
```

**Dependencies:** `flask flask-sqlalchemy psycopg2-binary pytz`

---

## Project files

```
pos/
├── app.py              Flask API, SQLAlchemy models, menu seeding
├── templates/
│   └── index.html      Full POS frontend
├── SPEC.md             Data model and feature spec
├── UPDATES.md          Changelog
├── USAGE.md            How to run and operate
├── DEBUG.md            Debugging steps
└── CLAUDE.md           Developer context
```

---

## API reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/products` | List available products |
| `POST` | `/api/products` | Create product |
| `PATCH` | `/api/products/:id` | Update product |
| `GET` | `/api/orders` | List recent orders |
| `POST` | `/api/orders` | Create order (`status: paid` for immediate payment) |
| `PATCH` | `/api/orders/:id` | Update order status |
| `DELETE` | `/api/orders/:id` | Delete order and its items |
| `GET` | `/api/stats` | Today's sales, pending count, order count |

---

## Data model

**Products** — `id, name, category, price (paisa), is_available, image (emoji)`

**Orders** — `id, order_number (ORD-HHMMSS-###), table_number, status, total (paisa), created_at`

**OrderItems** — `id, order_id, product_id, quantity, price (snapshot at order time)`

---

## Receipt branding

Edit `RECEIPT_BRAND` in `templates/index.html` to set your cafe's name, address, GSTIN, and phone — shown on every printed receipt.

---

## GitHub

https://github.com/chaitanyasunny/pos-cafe-india.git