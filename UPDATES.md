# Updates Log

## 2026-04-25 — Orders reliability, kitchen ticket UX, docs, Desserts

### Backend (`app.py`)

- **Order create (`POST /api/orders`)**: Rejects empty `items` or orders where no line resolves to a product (**400**). Optional **`status`** in JSON (`pending` / `prepared` / `paid`) so payment can save as paid in one request instead of POST + PATCH.
- **Order numbers**: `ORD-HHMMSS-###` with a random suffix to reduce same-second collisions (`secrets`).
- **Delete order (`DELETE /api/orders/:id`)**: Deletes related **`order_items`** first so PostgreSQL foreign keys do not block cancellation.
- **Desserts**: New category with eight default products; definitions live in **`_DESSERT_SEED`** and **`default_dessert_products()`**. **`ensure_desserts_category()`** runs on startup so databases seeded before desserts still get the new items once.
- Removed unused **`date`** import from `datetime`.

### Frontend (`templates/index.html`)

- **Table number** on the current order panel (sent with each new order).
- **Kitchen ticket flow**: Bill preview shows a **draft** line until the order exists; after **Send to kitchen** or **Pay**, the preview shows the **server `order_number`**. Modal title **Kitchen ticket**; actions **Send to kitchen** / **Print receipt**.
- **Pay**: Single API create with `status: paid`; loading state on confirm; opens receipt modal with saved order id; **backdrop click** closes modals.
- **Print/Pay** disabled when the cart is empty; slightly larger **quantity** tap targets; **`data-emoji`** on add-item icon grid so the default selection works without an extra click.
- **Manage Menu**: Availability **`PATCH`** sends **`this.checked`** (explicit state, not a stale flip).
- **Add to order**: Ignores missing or unavailable products.
- **Category tabs**: Sorted alphabetically (e.g. All, Beverages, Desserts, Food, Snacks).
- **Add Item** modal: **Desserts** in the category dropdown.

### Documentation

- **`README.md`**: Table field, kitchen ticket / pay flow, server order numbers, pre-GST stored totals vs GST on screen, `pip install` line (including **pytz**), generic clone path in Quick Start.
- **`USAGE.md`**: Table field, ticket/payment behaviour, GST note, duplicate troubleshooting step removed, optional **`DATABASE_URL`**, API table updated for `POST /api/orders` and `DELETE` behaviour.

### Git

- `7d014eb` — Harden orders API, kitchen ticket UX, and refresh README/USAGE  
- `a9f46b1` — Add Desserts menu category with seed and upgrade path  

---

## 2026-04-22 - Visual Menu Items & QR Payment

### Changes Made

**1. Menu Item Images (Emoji Icons)**
- Added `image` column to `products` table (VARCHAR 255)
- All menu items now display emoji icons for quick visual recognition
- Each menu item shows: emoji (2rem), name, and price
- Existing products seeded with appropriate food/drink emojis

**2. Toggle Switches in Manage Menu**
- Replaced Enable/Disable buttons with iOS-style toggle switches
- Toggle switches are inline with item info (icon, name, price)
- Clicking toggle instantly enables/disables item
- Visual feedback: red (#FF6B6B) when enabled, gray when disabled

**3. QR Code Payment Option**
- Added third payment option "QR Code" in payment modal
- Shows QR placeholder area for future UPI payment integration
- Icon: 📱

**4. Add Item Modal with Image Picker**
- Old: Used browser prompts (name, category, price)
- New: Proper modal dialog with form fields
- Image picker: 27 emoji options in a grid
- Staff can select icon before adding item

### Files Modified

- `app.py` - Added `image` field to Product model, updated seed data with emojis
- `templates/index.html` - Added emoji display, toggle switches, QR payment option, add item modal
- `SPEC.md` - Updated data model and features list
- `README.md` - Updated feature list
- Database: Added `image` column to products table

### Technical Details

**Database Migration:**
```sql
ALTER TABLE products ADD COLUMN image VARCHAR(255);
UPDATE products SET image = '☕' WHERE name = 'Masala Chai';
-- etc. for all 28 products
```

**Image Picker Emojis:**
['☕', '🥤', '🧊', '🍋', '🍵', '🍫', '🧃', '🥛', '🥪', '🧀', '🍚', '🥘', '🍛', '🫘', '🌶️', '🥞', '🥟', '🍞', '🍳', '🟤', '🟡', '🫛', '🍪', '🍽️', '🍺', '🧁', '🥗']

---

## 2026-04-21 - Print/Pay Modals & Admin Bar

### Changes Made

**Print Modal**
- Bill preview with order number, items, subtotal, GST, total
- Confirm button sends order to kitchen (pending status)

**Payment Modal**
- Cash and Card/UPI payment options
- Displays total amount
- Confirm button marks order as paid

**Admin Bar**
- "+ Add Item" button - create new menu items
- "Manage Menu" button - toggle manage mode

**Stats Header**
- Today's sales (only paid orders)
- Pending count
- Total order count

---

## Previous Commits

- `a9f46b1` - Desserts category, seed + `ensure_desserts_category`, UI category sort and Add Item option
- `7d014eb` - Orders API hardening, kitchen ticket UX, README/USAGE refresh
- `b785807` - Manage Menu toggle & Print Bill after Pay implementation
- `07501e1` - Menu item images / QR payment implementation
- `80d154a` - Fixed three UI bugs: missing renderOrder() function, unstyled admin bar, manage mode unavailable products
- `bc088eb` - readme & SPEC.md updated
- `e1c3d03` - Print and pay functionality modal
- `52d2c12` - Initial commit: Cafe POS for Indian cafe