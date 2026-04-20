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
- Items are grouped by category: Beverages, Food, Snacks
- Click category tabs to filter
- Click any item to add it to the current order

### Order Panel (right side)
- Shows all items in current order
- Use `+`/`-` buttons to adjust quantity
- **Clear** removes all items from the order

### Billing
- Subtotal, GST (5%), and Total are calculated automatically
- **Print** — Saves order with status "pending" (for kitchen display)
- **Pay** — Saves order with status "paid" (records today's sales)

### Stats Header
- **Today's Sales** — Total revenue from paid orders today
- **Pending** — Orders waiting to be prepared
- **Orders** — Total orders placed today

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
| GET | `/api/orders` | List recent orders |
| POST | `/api/orders` | Create new order |
| PATCH | `/api/orders/:id` | Update order status |
| GET | `/api/stats` | Today's stats |
