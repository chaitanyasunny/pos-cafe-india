# How to Run & Use Cafe POS

## Starting the Server

### 1. Start PostgreSQL (if not already running)

```bash
brew services start postgresql@16
```

### 2. Run the Flask app

```bash
cd /Users/chaitanya/Documents/claude/pos
/usr/bin/python3 app.py
```

The server starts at **http://127.0.0.1:5555**

> **Note**: If Chrome blocks localhost, use your IP address: `http://$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'):5555`

---

## Using the POS

### Menu Panel (left side)
- **Search** — Use the field above the category tabs to filter by item or category name (works together with the selected tab: pick a category, then search within it)
- Items are grouped by category (e.g. Beverages, Food, Snacks, Desserts)
- Click category tabs to filter
- Click any item to add it to the current order

### Order Panel (right side)
- **Table** — Enter table number (1–999); it is sent with each new order
- Shows all items in the current order
- Use `+`/`-` to adjust quantity (Print/Pay stay disabled until there is at least one line)
- **Clear** removes all items from the order

### Kitchen ticket & payment
- Subtotal, GST (18%), and total are shown automatically (GST is for display/receipt; stored `order.total` in the database is the sum of line items before GST)
- **Print** — Opens the **Kitchen ticket** modal with enhanced bill preview (table, item count, timestamp). The preview is a **draft** until you click **Send to kitchen**, which creates a `pending` order and shows the real **order number** from the server
- **Pay** — Choose Cash, Card/UPI, or QR, enter cashier name, then **Confirm**. Creates a `paid` order in one request and opens the receipt modal for an optional **Print receipt**
- Click outside a modal (dark backdrop) to close it, same as **Cancel**

### Stats Header
- **Today's Sales** — Total revenue from paid orders today
- **Pending** — Orders waiting to be prepared
- **Orders** — Total orders placed today
- **Live Clock** — Current time (IST)

### Admin Features
- Click the **lock icon** in the header to unlock admin actions
- Enter the admin password to gain access to:
  - **Add Item** — Create new menu items with emoji icon picker
  - **Manage Menu** — Edit names, prices, and toggle availability
  - **Availability Toggles** — Show/hide items from the menu grid
- Admin actions are blocked until unlocked

---

## Receipt Printing

### Thermal Printer Support
- **58mm** — Compact receipt format for small thermal printers
- **80mm** — Standard receipt format with more spacing

### Receipt Content
Every receipt includes:
- Cafe branding (name, address, GSTIN, phone)
- Order number and timestamp
- Itemized list with quantities and prices
- Payment method and cashier name
- Subtotal, GST (18%), and grand total

---

## Troubleshooting

For detailed debugging, see [DEBUG.md](DEBUG.md).

### Blank/white screen

1. **Check server is running:**
   ```bash
   curl http://127.0.0.1:5555/
   ```
   Should return HTML with `</html>` closing tag.

2. **Hard refresh**: `Cmd+Shift+R` (Mac) / `Ctrl+Shift+R`

3. **Open in private/incognito window**

4. **Try 127.0.0.1 instead of localhost**

5. **Chrome localhost blocked** — use your machine IP:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'
   ```
   Then access via `http://YOUR_IP:5555`

### Database issues

If you get database connection errors:
```bash
# Create the database
createdb cafe_pos

# Or connect to verify
psql -d cafe_pos -c '\dt'
```

Optional: point the app at another database (defaults to `postgresql://localhost/cafe_pos`):

```bash
export DATABASE_URL='postgresql://user:pass@host:5432/cafe_pos'
```

### Stopping the server

```bash
pkill -f "python3 app.py"
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | POS frontend |
| GET | `/api/products` | List all menu items |
| POST | `/api/products` | Add new menu item |
| PATCH | `/api/products/:id` | Update menu item (name, price, availability) |
| GET | `/api/orders` | List recent orders |
| POST | `/api/orders` | Create order (JSON: `items`, optional `table_number`, optional `status`: `pending` / `prepared` / `paid`; returns **400** if `items` is empty or no valid products) |
| PATCH | `/api/orders/:id` | Update order status or table |
| DELETE | `/api/orders/:id` | Cancel/delete order (line items are removed first so the delete succeeds) |
| GET | `/api/stats` | Today's stats |

---

## Future Work

### Planned Enhancements

| Priority | Feature | Description |
|----------|---------|-------------|
| High | Order history view | Browse and filter past orders with status badges |
| High | Kitchen display screen | Dedicated view for pending orders (KDS-style) |
| Medium | Daily/weekly reports | Sales analytics with charts and export |
| Medium | Multi-user login | Role-based access (cashier, manager, admin) |
| Low | Inventory tracking | Stock levels and low-stock alerts |
| Low | Customer loyalty | Points system and discount codes |

### Nice-to-Have

- Offline mode with sync-on-reconnect
- Barcode scanner support for packaged items
- Table status tracking (occupied/available)
- Split billing and partial payments
- Integration with UPI payment verification
