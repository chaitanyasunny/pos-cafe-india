"""
Comprehensive API tests for Cafe POS.
Tests all endpoints: products, orders, stats.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import Product, Order, OrderItem


class TestProductsAPI:
    """Test /api/products endpoints."""

    def test_get_products_empty(self, client, init_database):
        """GET /api/products returns list (auto-seeds defaults on first access)."""
        response = client.get('/api/products')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        # Note: Auto-seeding happens on first access, so we get default products
        assert len(data) >= 27  # Default seed products

    def test_get_products_with_data(self, client_with_db):
        """GET /api/products returns all seeded products."""
        response = client_with_db.get('/api/products')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 20  # Should have 27+ products

    def test_get_product_structure(self, client_with_db):
        """GET /api/products returns products with correct structure."""
        response = client_with_db.get('/api/products')
        data = response.get_json()
        assert len(data) > 0
        product = data[0]
        assert 'id' in product
        assert 'name' in product
        assert 'category' in product
        assert 'price' in product
        assert 'is_available' in product
        assert 'image' in product

    def test_create_product(self, client, init_database):
        """POST /api/products creates a new product."""
        new_product = {
            'name': 'Test Coffee',
            'category': 'Beverages',
            'price': 25000,  # Rs 250 in paisa
            'is_available': True,
            'image': '☕'
        }
        response = client.post('/api/products', json=new_product)
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Test Coffee'
        assert data['category'] == 'Beverages'
        assert data['price'] == 25000
        assert data['is_available'] == True
        assert data['image'] == '☕'
        assert 'id' in data

    def test_create_product_minimal(self, client, init_database):
        """POST /api/products works with minimal fields."""
        new_product = {
            'name': 'Simple Item',
            'category': 'Snacks',
            'price': 10000
        }
        response = client.post('/api/products', json=new_product)
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Simple Item'
        assert data['is_available'] == True  # Default

    def test_update_product_availability(self, client, init_database):
        """PATCH /api/products/:id updates availability."""
        # Create product
        product = {'name': 'Test Item', 'category': 'Food', 'price': 5000}
        create_resp = client.post('/api/products', json=product)
        product_id = create_resp.get_json()['id']

        # Update availability
        response = client.patch(f'/api/products/{product_id}', json={'is_available': False})
        assert response.status_code == 200
        data = response.get_json()
        assert data['is_available'] == False

    def test_update_product_price(self, client, init_database):
        """PATCH /api/products/:id updates price."""
        product = {'name': 'Test Item', 'category': 'Food', 'price': 5000}
        create_resp = client.post('/api/products', json=product)
        product_id = create_resp.get_json()['id']

        response = client.patch(f'/api/products/{product_id}', json={'price': 7500})
        assert response.status_code == 200
        data = response.get_json()
        assert data['price'] == 7500

    def test_update_product_name(self, client, init_database):
        """PATCH /api/products/:id updates name."""
        product = {'name': 'Old Name', 'category': 'Food', 'price': 5000}
        create_resp = client.post('/api/products', json=product)
        product_id = create_resp.get_json()['id']

        response = client.patch(f'/api/products/{product_id}', json={'name': 'New Name'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'New Name'

    def test_update_nonexistent_product(self, client, init_database):
        """PATCH /api/products/:id returns 404 for nonexistent product."""
        response = client.patch('/api/products/99999', json={'name': 'Test'})
        assert response.status_code == 404

    def test_create_product_missing_fields(self, client, init_database):
        """POST /api/products fails without required fields."""
        # Missing price
        response = client.post('/api/products', json={'name': 'Test', 'category': 'Food'})
        assert response.status_code == 400

        # Missing name
        response = client.post('/api/products', json={'category': 'Food', 'price': 1000})
        assert response.status_code == 400

        # Missing category
        response = client.post('/api/products', json={'name': 'Test', 'price': 1000})
        assert response.status_code == 400


class TestOrdersAPI:
    """Test /api/orders endpoints."""

    def test_get_orders_empty(self, client, init_database):
        """GET /api/orders returns empty list when no orders exist."""
        response = client.get('/api/orders')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_create_order_success(self, client, init_database):
        """POST /api/orders creates order with items."""
        # First create a product
        product = {'name': 'Chai', 'category': 'Beverages', 'price': 2000}
        client.post('/api/products', json=product)

        order = {
            'table_number': 5,
            'status': 'pending',
            'items': [{'product_id': 1, 'quantity': 2}]
        }
        response = client.post('/api/orders', json=order)
        assert response.status_code == 200
        data = response.get_json()
        assert 'id' in data
        assert data['table_number'] == 5
        assert data['status'] == 'pending'
        assert len(data['items']) == 1
        assert data['items'][0]['quantity'] == 2

    def test_create_order_paid_status(self, client, init_database):
        """POST /api/orders with status='paid' for immediate payment."""
        product = {'name': 'Coffee', 'category': 'Beverages', 'price': 2500}
        client.post('/api/products', json=product)

        order = {
            'table_number': 3,
            'status': 'paid',
            'items': [{'product_id': 1, 'quantity': 1}]
        }
        response = client.post('/api/orders', json=order)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'paid'

    def test_create_order_empty_items_fails(self, client, init_database):
        """POST /api/orders rejects empty items array."""
        order = {'table_number': 1, 'items': []}
        response = client.post('/api/orders', json=order)
        assert response.status_code == 400

    def test_create_order_missing_items_fails(self, client, init_database):
        """POST /api/orders rejects missing items field."""
        order = {'table_number': 1}
        response = client.post('/api/orders', json=order)
        assert response.status_code == 400

    def test_create_order_invalid_product(self, client, init_database):
        """POST /api/orders with invalid product_id fails."""
        order = {
            'table_number': 1,
            'items': [{'product_id': 99999, 'quantity': 1}]
        }
        response = client.post('/api/orders', json=order)
        assert response.status_code == 400

    def test_create_order_total_calculation(self, client, init_database):
        """POST /api/orders calculates correct total."""
        product = {'name': 'Item', 'category': 'Food', 'price': 5000}
        client.post('/api/products', json=product)

        order = {'items': [{'product_id': 1, 'quantity': 3}]}
        response = client.post('/api/orders', json=order)
        data = response.get_json()
        assert data['total'] == 15000  # 5000 * 3

    def test_update_order_status(self, client, init_database):
        """PATCH /api/orders/:id updates status."""
        # Create product and order
        client.post('/api/products', json={'name': 'Test', 'category': 'Food', 'price': 1000})
        order = {'items': [{'product_id': 1, 'quantity': 1}]}
        create_resp = client.post('/api/orders', json=order)
        order_id = create_resp.get_json()['id']

        # Update status
        response = client.patch(f'/api/orders/{order_id}', json={'status': 'prepared'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'prepared'

    def test_update_order_table_number(self, client, init_database):
        """PATCH /api/orders/:id updates table_number."""
        client.post('/api/products', json={'name': 'Test', 'category': 'Food', 'price': 1000})
        order = {'table_number': 1, 'items': [{'product_id': 1, 'quantity': 1}]}
        create_resp = client.post('/api/orders', json=order)
        order_id = create_resp.get_json()['id']

        response = client.patch(f'/api/orders/{order_id}', json={'table_number': 10})
        assert response.status_code == 200
        data = response.get_json()
        assert data['table_number'] == 10

    def test_delete_order(self, client, init_database):
        """DELETE /api/orders/:id removes order and items."""
        client.post('/api/products', json={'name': 'Test', 'category': 'Food', 'price': 1000})
        order = {'items': [{'product_id': 1, 'quantity': 1}]}
        create_resp = client.post('/api/orders', json=order)
        order_id = create_resp.get_json()['id']

        response = client.delete(f'/api/orders/{order_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True

        # Verify order is gone
        orders_resp = client.get('/api/orders')
        orders = orders_resp.get_json()
        assert len(orders) == 0

    def test_delete_nonexistent_order(self, client, init_database):
        """DELETE /api/orders/:id returns 404 for nonexistent order."""
        response = client.delete('/api/orders/99999')
        assert response.status_code == 404

    def test_get_orders_with_status_filter(self, client, init_database):
        """GET /api/orders?status=pending filters by status."""
        client.post('/api/products', json={'name': 'Test', 'category': 'Food', 'price': 1000})

        # Create orders with different statuses
        client.post('/api/orders', json={'status': 'pending', 'items': [{'product_id': 1, 'quantity': 1}]})
        client.post('/api/orders', json={'status': 'paid', 'items': [{'product_id': 1, 'quantity': 1}]})

        response = client.get('/api/orders?status=pending')
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['status'] == 'pending'

    def test_order_number_format(self, client, init_database):
        """Orders get properly formatted order numbers."""
        client.post('/api/products', json={'name': 'Test', 'category': 'Food', 'price': 1000})
        order = {'items': [{'product_id': 1, 'quantity': 1}]}
        response = client.post('/api/orders', json=order)
        data = response.get_json()
        assert 'order_number' in data
        assert data['order_number'].startswith('ORD-')


class TestStatsAPI:
    """Test /api/stats endpoint."""

    def test_stats_empty(self, client, init_database):
        """GET /api/stats returns zeros when no data."""
        response = client.get('/api/stats')
        assert response.status_code == 200
        data = response.get_json()
        assert data['today_sales'] == 0
        assert data['pending_count'] == 0
        assert data['today_order_count'] == 0

    def test_stats_with_orders(self, client, init_database):
        """GET /api/stats reflects order data."""
        client.post('/api/products', json={'name': 'Test', 'category': 'Food', 'price': 10000})

        # Create a paid order
        paid_order = {
            'status': 'paid',
            'items': [{'product_id': 1, 'quantity': 2}]  # 20000 paisa
        }
        client.post('/api/orders', json=paid_order)

        # Create a pending order
        pending_order = {
            'status': 'pending',
            'items': [{'product_id': 1, 'quantity': 1}]  # 10000 paisa
        }
        client.post('/api/orders', json=pending_order)

        response = client.get('/api/stats')
        data = response.get_json()
        assert data['today_sales'] == 20000  # Only paid orders count
        assert data['pending_count'] == 1
        assert data['today_order_count'] == 2

    def test_stats_prepared_count(self, client, init_database):
        """GET /api/stats includes prepared count."""
        client.post('/api/products', json={'name': 'Test', 'category': 'Food', 'price': 5000})
        client.post('/api/orders', json={'status': 'prepared', 'items': [{'product_id': 1, 'quantity': 1}]})

        response = client.get('/api/stats')
        data = response.get_json()
        assert 'prepared_count' in data
        assert data['prepared_count'] == 1


class TestProductCategories:
    """Test product category functionality."""

    def test_products_by_category(self, client, init_database):
        """Products can be filtered by category in frontend (API returns all)."""
        client.post('/api/products', json={'name': 'Chai', 'category': 'Beverages', 'price': 2000})
        client.post('/api/products', json={'name': 'Samosa', 'category': 'Snacks', 'price': 3000})

        response = client.get('/api/products')
        data = response.get_json()
        assert len(data) == 2

        categories = set(p['category'] for p in data)
        assert 'Beverages' in categories
        assert 'Snacks' in categories

    def test_desserts_category_exists(self, client_with_db):
        """Desserts category is available."""
        response = client_with_db.get('/api/products')
        data = response.get_json()
        categories = set(p['category'] for p in data)
        assert 'Desserts' in categories


class TestDataIntegrity:
    """Test data integrity and edge cases."""

    def test_price_in_paisa(self, client, init_database):
        """Prices are stored in paisa (integer)."""
        product = {'name': 'Test', 'category': 'Food', 'price': 9999}  # Rs 99.99
        response = client.post('/api/products', json=product)
        data = response.get_json()
        assert isinstance(data['price'], int)
        assert data['price'] == 9999

    def test_order_items_snapshot_price(self, client, init_database):
        """Order items store price snapshot at order time."""
        product = {'name': 'Test', 'category': 'Food', 'price': 5000}
        client.post('/api/products', json=product)

        order = {'items': [{'product_id': 1, 'quantity': 1}]}
        response = client.post('/api/orders', json=order)
        data = response.get_json()

        assert len(data['items']) == 1
        assert data['items'][0]['price'] == 5000

    def test_multiple_items_in_order(self, client, init_database):
        """Orders can have multiple different items."""
        client.post('/api/products', json={'name': 'Item1', 'category': 'Food', 'price': 1000})
        client.post('/api/products', json={'name': 'Item2', 'category': 'Food', 'price': 2000})

        order = {
            'items': [
                {'product_id': 1, 'quantity': 1},
                {'product_id': 2, 'quantity': 2}
            ]
        }
        response = client.post('/api/orders', json=order)
        data = response.get_json()
        assert len(data['items']) == 2
        assert data['total'] == 5000  # 1000 + 2000*2
