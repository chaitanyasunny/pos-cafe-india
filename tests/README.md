# Cafe POS API Tests

Automated pytest test suite for the Cafe POS API.

## Setup

### 1. Install dependencies

```bash
/usr/bin/python3 -m pip install pytest pytest-flask
```

### 2. Create test database

```bash
createdb cafe_pos_test
```

## Running Tests

```bash
# Run all tests
/usr/bin/python3 -m pytest tests/ -v

# Run specific test class
/usr/bin/python3 -m pytest tests/test_api.py::TestProductsAPI -v

# Run specific test
/usr/bin/python3 -m pytest tests/test_api.py::TestOrdersAPI::test_create_order_success -v

# Run with coverage (if pytest-cov installed)
/usr/bin/python3 -m pytest tests/ --cov=app
```

## Test Coverage

### Products API (10 tests)
- GET /api/products - list products
- POST /api/products - create product with validation
- PATCH /api/products/:id - update name, price, availability, category, image
- 404 handling for nonexistent products

### Orders API (13 tests)
- GET /api/orders - list orders with optional status filter
- POST /api/orders - create order with items, validation
- PATCH /api/orders/:id - update status and table_number
- DELETE /api/orders/:id - cancel/delete order
- Order number format verification

### Stats API (3 tests)
- GET /api/stats - today's sales, pending count, order count, prepared count
- Correct calculation (only paid orders count for sales)

### Data Integrity (5 tests)
- Price storage in paisa
- Order item price snapshots
- Multiple items per order
- Category handling
- Desserts category availability

## Bugs Found & Fixed

### 1. Missing validation on POST /api/products
**Issue:** API threw 500 KeyError when `price` field was missing  
**Fix:** Added validation to return 400 with error message  
**Test:** `test_create_product_missing_fields`

### 2. SQLAlchemy deprecation warnings
**Issue:** Using legacy `Query.get()` method  
**Fix:** Updated to `db.session.get()`  
**Test:** All update/delete tests

## Test Database

Tests use an isolated `cafe_pos_test` database:
- Each test gets fresh tables (drop/create)
- Some tests use auto-seeded default products (27+ items)
- Test data never touches development database

## CI/CD Integration

Add to your CI pipeline:

```bash
# Ensure test DB exists
createdb cafe_pos_test 2>/dev/null || true

# Run tests
/usr/bin/python3 -m pytest tests/ -v --tb=short
```
