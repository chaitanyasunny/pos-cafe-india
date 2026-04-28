"""
Pytest configuration and fixtures for Cafe POS API tests.
"""
import pytest
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Product, Order, OrderItem, IST


@pytest.fixture
def app_config():
    """Configure app for testing with test database."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cafe_pos_test'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


@pytest.fixture
def client(app_config):
    """Create test client."""
    with app_config.test_client() as client:
        yield client


@pytest.fixture
def init_database(app_config):
    """Initialize database with fresh tables for each test."""
    with app_config.app_context():
        # Drop all tables and recreate (fresh state per test)
        db.drop_all()
        db.create_all()
        yield db
        # Cleanup after test
        db.session.remove()
        db.drop_all()


@pytest.fixture
def seeded_database(init_database):
    """Database with default products seeded."""
    from app import seed_products, ensure_desserts_category
    seed_products()
    ensure_desserts_category()
    yield init_database


@pytest.fixture
def client_with_db(app_config, seeded_database):
    """Test client with seeded database."""
    with app_config.test_client() as client:
        yield client
