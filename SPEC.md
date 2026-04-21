# Cafe POS System - India

## Concept & Vision

A straightforward point-of-sale system for a small Indian cafe. Handles menu management, order taking, and bill generation in INR. Designed for speed and simplicity — staff should be able to take orders quickly during rush hours.

## Design Language

- **Aesthetic**: Clean, functional dashboard with warm cafe vibes
- **Colors**: `#2D3436` (dark), `#FF6B6B` (coral accent), `#FFEAA7` (warm yellow), `#F5F5F5` (light bg)
- **Typography**: Inter for UI, system sans-serif fallback
- **Motion**: Minimal — fast interactions only

## Tech Stack

- **Backend**: Python Flask + SQLAlchemy
- **Database**: PostgreSQL (local)
- **Frontend**: HTML/CSS/JS served by Flask
- **Currency**: INR (Indian Rupees)

## Data Model

### Products
- `id`, `name`, `category`, `price` (in paisa), `is_available`, `image` (emoji), `created_at`

### Orders
- `id`, `order_number`, `table_number`, `status` (pending/prepared/paid), `total` (in paisa), `created_at`

### OrderItems
- `id`, `order_id`, `product_id`, `quantity`, `price` (paisa, snapshot at order time)

## Features

1. **Menu Display** — Grid of items by category (Beverages, Food, Snacks) with availability toggle
2. **Order Creation** — Tap items to add to order, adjust quantities with +/- buttons
3. **Bill Generation** — Calculate subtotal + 5% GST, print bill preview
4. **Order History** — View recent orders with status (pending/prepared/paid)
5. **Quick Stats** — Today's sales total, pending count, order count in header
6. **Admin Menu** — Add new items with emoji icons, toggle switch for enable/disable menu items visually
7. **Payment Modal** — Select cash, card/UPI, or QR code payment method
8. **Print Modal** — Preview and print bill before sending to kitchen
9. **Visual Menu Items** — Each menu item displays an emoji icon for quick visual recognition
10. **Image Picker** — When adding items, staff can select from emoji icons for visual representation

## API Endpoints

- `GET /api/products` — List all menu items
- `POST /api/orders` — Create new order
- `GET /api/orders` — List orders (with optional date filter)
- `PATCH /api/orders/:id` — Update order status
- `GET /api/stats` — Today's stats

## Running Locally

1. Install dependencies: `pip install flask flask-sqlalchemy psycopg2-binary`
2. Create PostgreSQL database: `createdb cafe_pos`
3. Set env var: `export DATABASE_URL=postgresql://localhost/cafe_pos`
4. Run: `python app.py`
5. Open: `http://localhost:5000`
