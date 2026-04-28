# Manual UI Testing Checklist

**Date:** 2026-04-28  
**Version:** Design-upgrades branch  
**Tester:** _______________

---

## How to Use This Checklist

1. Open browser to http://127.0.0.1:5555
2. Go through each section systematically
3. Check off each item as you verify it works
4. Note any bugs or unexpected behavior in the Issues section

---

## 1. Homepage Load & Header

- [ ] Page loads without errors
- [ ] Title shows "Cafe POS - India"
- [ ] Admin bar visible at top (dark background)
- [ ] Header displays "Cafe POS" with "Live Counter" badge
- [ ] Kitchen Display link visible and clickable
- [ ] Live clock shows current time (updates every second)
- [ ] Stats bar shows: Today's Sales, Pending, Orders
- [ ] Stats update when orders are created

---

## 2. Menu Panel (Left Side)

### Category Tabs
- [ ] "All" tab shows all products
- [ ] "Beverages" tab filters to beverages only
- [ ] "Food" tab filters to food items only
- [ ] "Snacks" tab filters to snacks only
- [ ] "Desserts" tab shows dessert items
- [ ] Active tab has coral/red background

### Search
- [ ] Search box visible above category tabs
- [ ] Typing filters items by name
- [ ] Search works within selected category
- [ ] Clear button (X) appears when typing
- [ ] Clear button removes search text
- [ ] Press `/` focuses search (when not in input)
- [ ] Press `Esc` clears search

### Menu Items
- [ ] Items display emoji icons
- [ ] Items show name and price correctly
- [ ] Prices display in Rs (divided by 100 from paisa)
- [ ] Hover effect shows shadow and border
- [ ] Clicking unavailable items does nothing
- [ ] Unavailable items are grayed out (opacity)

---

## 3. Order Panel (Right Side)

### Adding Items
- [ ] Clicking menu item adds to order
- [ ] Same item increases quantity
- [ ] Order shows item name and unit price
- [ ] Quantity buttons (+/-) visible
- [ ] + increases quantity
- [ ] - decreases quantity
- [ ] Item removed when quantity reaches 0

### Table Number
- [ ] Table number input visible
- [ ] Default value is 1
- [ ] Can change table number
- [ ] Table number sends with order

### Bill Calculation
- [ ] Subtotal updates as items added
- [ ] GST (18%) line visible
- [ ] GST amount calculates correctly
- [ ] Total = Subtotal + GST
- [ ] Clear button removes all items
- [ ] Print/Pay buttons disabled when empty
- [ ] Print/Pay buttons enabled when items exist

---

## 4. Print/Kitchen Flow

### Print Modal
- [ ] Click Print opens modal
- [ ] Modal title: "Kitchen ticket"
- [ ] Bill preview shows items with quantities
- [ ] Bill preview shows subtotal, GST, total
- [ ] Cashier field editable (default: "Counter 1")
- [ ] Paper size selector (58mm/80mm)
- [ ] Changing paper size updates preview
- [ ] Changing cashier updates preview
- [ ] "Send to kitchen" button creates order
- [ ] Order number appears after creation
- [ ] "Print receipt" button triggers print dialog
- [ ] Backdrop click closes modal

---

## 5. Payment Flow

### Payment Modal
- [ ] Click Pay opens modal
- [ ] Bill preview shows in modal
- [ ] Payment options visible: Cash, Card/UPI
- [ ] Clicking option selects it (highlighted border)
- [ ] Can only select one payment method
- [ ] "Confirm & Save" disabled until method selected
- [ ] Confirm creates order with status=paid
- [ ] After payment, receipt modal opens
- [ ] Backdrop click closes modal

---

## 6. Recent Orders Section

- [ ] Recent orders appear below order panel
- [ ] Shows order number, amount, status badge
- [ ] Status colors: Pending=yellow, Prepared=blue, Paid=green
- [ ] Pending orders show "Ready" button
- [ ] Clicking "Ready" changes status to prepared
- [ ] Non-paid orders show "X" (cancel) button
- [ ] Cancel asks for confirmation
- [ ] Cancelled order removed from list

---

## 7. Admin Functions

### Lock/Unlock
- [ ] Admin bar shows "LOCKED" status initially
- [ ] Click "Unlock" prompts for password
- [ ] Password: `admin123`
- [ ] Wrong password shows error
- [ ] Correct password shows "UNLOCKED"
- [ ] Click "Lock" re-locks admin

### Add Item
- [ ] "+ Add Item" button visible in admin bar
- [ ] Clicking requires unlock first
- [ ] Modal opens with form fields
- [ ] Name, Category, Price fields work
- [ ] Emoji picker shows icon options
- [ ] Selecting emoji highlights it
- [ ] Add Item creates product
- [ ] New product appears in menu

### Manage Menu
- [ ] "Manage Menu" button in admin bar
- [ ] Requires unlock to activate
- [ ] Mode indicator appears ("MANAGE MODE")
- [ ] Menu items show toggle switches
- [ ] Toggle shows ON/OFF label
- [ ] Toggling updates availability
- [ ] Changes persist after refresh
- [ ] Exit manage mode to return to normal

---

## 8. Kitchen Display System (KDS)

### Access & Layout
- [ ] Click "Kitchen Display" navigates to KDS
- [ ] Back arrow returns to POS
- [ ] Live clock visible and updating
- [ ] Filter buttons: All, Pending, Prepared
- [ ] Keyboard shortcuts shown ([1], [2], [3], [R])

### Order Display
- [ ] Orders appear as cards
- [ ] Card shows order number, table number
- [ ] Status badge on each card
- [ ] Items listed with quantities
- [ ] Order age shows (e.g., "5m ago")
- [ ] Aged orders (>10 min) have red border
- [ ] Clicking card toggles status
- [ ] New orders trigger audio alert

### Filters
- [ ] "All" shows all orders
- [ ] "Pending" shows pending only
- [ ] "Prepared" shows prepared only
- [ ] Keyboard 1/2/3 switches filters
- [ ] Press R refreshes orders
- [ ] Auto-refresh every 10 seconds

---

## 9. Receipt Printing

### Receipt Content
- [ ] Receipt shows cafe name
- [ ] Address displays
- [ ] GSTIN displays
- [ ] Phone number displays
- [ ] Order number displays
- [ ] Items with quantities
- [ ] Subtotal, GST, Total
- [ ] Payment method shown
- [ ] Cashier name shown
- [ ] Footer note: "Thank you..."

### Print Behavior
- [ ] Print dialog opens
- [ ] Only receipt prints (not full page)
- [ ] 58mm mode formats for thermal
- [ ] 80mm mode formats for wider thermal

---

## 10. Edge Cases & Error Handling

- [ ] Empty cart: Print/Pay disabled
- [ ] Empty cart: Alert if forcing print
- [ ] No table number: Defaults to 1
- [ ] Invalid price: API returns error
- [ ] Network error: Shows error message
- [ ] Modal close: Backdrop click works
- [ ] Rapid clicking: No duplicate orders

---

## Issues Found

| # | Section | Issue Description | Severity |
|---|---------|-------------------|----------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

**Severity:** Low (cosmetic) | Medium (annoying) | High (broken feature)

---

## Summary

- **Total Tests:** ___ / 100+
- **Passed:** ___
- **Failed:** ___
- **Issues Found:** ___

**Overall Status:** Pass / Needs Fixes
