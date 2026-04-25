import os
import secrets
from collections import defaultdict
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://localhost/cafe_pos')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)  # in paisa
    is_available = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(255), nullable=True)  # emoji or icon identifier
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'is_available': self.is_available,
            'image': self.image
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), nullable=False)
    table_number = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, prepared, paid
    total = db.Column(db.Integer, default=0)  # in paisa
    created_at = db.Column(db.DateTime, default=datetime.now)

    items = db.relationship('OrderItem', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'table_number': self.table_number,
            'status': self.status,
            'total': self.total,
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer, nullable=False)  # snapshot at order time

    product = db.relationship('Product')

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else '',
            'quantity': self.quantity,
            'price': self.price
        }


IST = pytz.timezone('Asia/Kolkata')

def get_ist_now():
    """Get current time in Indian Standard Time."""
    return datetime.now(IST)


# (name, price_paisa, emoji) — single source for seed + DB upgrades
_DESSERT_SEED = (
    ('Gulab Jamun (2 pcs)', 4500, '🟤'),
    ('Ras Malai', 5500, '🥛'),
    ('Kheer (Cup)', 5000, '🍚'),
    ('Jalebi (Portion)', 4000, '🌀'),
    ('Ice Cream (2 Scoops)', 5000, '🍨'),
    ('Brownie with Ice Cream', 6500, '🍫'),
    ('Cheesecake Slice', 7000, '🍰'),
    ('Fruit Custard', 4500, '🍮'),
)


def default_dessert_products():
    return [Product(name=n, category='Desserts', price=p, image=i) for n, p, i in _DESSERT_SEED]


def seed_products():
    """Seed default menu items if database is empty."""
    if Product.query.first() is None:
        items = [
            # Beverages
            Product(name='Masala Chai', category='Beverages', price=2000, image='☕'),
            Product(name='Filter Coffee', category='Beverages', price=2500, image='🥤'),
            Product(name='Cold Coffee', category='Beverages', price=4500, image='🧊'),
            Product(name='Masala Lemon Soda', category='Beverages', price=3500, image='🍋'),
            Product(name='Green Tea', category='Beverages', price=3000, image='🍵'),
            Product(name='Hot Chocolate', category='Beverages', price=5000, image='🍫'),
            Product(name='Iced Tea', category='Beverages', price=4000, image='🧃'),
            Product(name='Lassi (Sweet)', category='Beverages', price=3500, image='🥛'),
            # Food
            Product(name='Veg Sandwich', category='Food', price=6000, image='🥪'),
            Product(name='Grilled Cheese Sandwich', category='Food', price=7500, image='🧀'),
            Product(name='Poha', category='Food', price=5000, image='🍚'),
            Product(name='Upma', category='Food', price=5000, image='🥘'),
            Product(name='Idli Sambar (2 pcs)', category='Food', price=5500, image='🍛'),
            Product(name='Medu Vada (2 pcs)', category='Food', price=5500, image='🫘'),
            Product(name='Pav Bhaji', category='Food', price=7000, image='🍛'),
            Product(name='Misal Pav', category='Food', price=6500, image='🌶️'),
            Product(name='Dosa (Masala)', category='Food', price=7000, image='🥞'),
            Product(name='Uttapam', category='Food', price=6500, image='🥞'),
            # Snacks
            Product(name='Samosa (2 pcs)', category='Snacks', price=3000, image='🥟'),
            Product(name='Vada Pav', category='Snacks', price=3500, image='🍞'),
            Product(name='Bread Pakora', category='Snacks', price=3000, image='🍳'),
            Product(name='Kachori', category='Snacks', price=3000, image='🟤'),
            Product(name='Dhokla', category='Snacks', price=4000, image='🟡'),
            Product(name='Pakode (Platter)', category='Snacks', price=4500, image='🫛'),
            Product(name='Biscuits & Cheese', category='Snacks', price=5000, image='🍪'),
            Product(name='Cookie (Choco Chip)', category='Snacks', price=2500, image='🍫'),
            *default_dessert_products(),
        ]
        db.session.add_all(items)
        db.session.commit()


def ensure_desserts_category():
    """Add default desserts if the DB was seeded before that category existed."""
    if Product.query.filter_by(category='Desserts').first() is not None:
        return
    db.session.add_all(default_dessert_products())
    db.session.commit()


def merge_duplicate_products():
    """For identical (category, name), keep the lowest id; re-point order lines and remove extras."""
    groups = defaultdict(list)
    for p in Product.query.order_by(Product.id).all():
        key = (p.category.strip().lower(), p.name.strip().lower())
        groups[key].append(p)
    changed = False
    for plist in groups.values():
        if len(plist) <= 1:
            continue
        keeper = plist[0]
        for dup in plist[1:]:
            for oi in OrderItem.query.filter_by(product_id=dup.id).all():
                oi.product_id = keeper.id
            db.session.delete(dup)
            changed = True
    if changed:
        db.session.commit()


@app.before_request
def before_first():
    if not hasattr(app, '_seeded'):
        with app.app_context():
            db.create_all()
            seed_products()
            ensure_desserts_category()
            merge_duplicate_products()
        app._seeded = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@app.route('/api/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json

    if 'is_available' in data:
        product.is_available = data['is_available']
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'category' in data:
        product.category = data['category']
    if 'image' in data:
        product.image = data['image']

    db.session.commit()
    return jsonify(product.to_dict())


@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    product = Product(
        name=data['name'],
        category=data['category'],
        price=data['price'],
        is_available=data.get('is_available', True),
        image=data.get('image')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict())


@app.route('/api/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        data = request.json or {}
        items = data.get('items') or []
        if not items:
            return jsonify({'error': 'Order must include at least one line item'}), 400

        status = data.get('status') or 'pending'
        if status not in ('pending', 'prepared', 'paid'):
            status = 'pending'

        order_num = f"ORD-{datetime.now().strftime('%H%M%S')}-{secrets.randbelow(900) + 100}"

        order = Order(
            order_number=order_num,
            table_number=data.get('table_number'),
            status=status,
            total=0,
            created_at=get_ist_now()
        )
        db.session.add(order)
        db.session.flush()

        total = 0
        for item in items:
            product = Product.query.get(item['product_id'])
            if product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item.get('quantity', 1),
                    price=product.price
                )
                db.session.add(order_item)
                total += product.price * item.get('quantity', 1)

        if total == 0:
            db.session.rollback()
            return jsonify({'error': 'No valid products in order'}), 400

        order.total = total
        db.session.commit()
        return jsonify(order.to_dict())

    # GET
    date_str = request.args.get('date')
    query = Order.query

    if date_str:
        try:
            filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Order.created_at) == filter_date)
        except ValueError:
            pass

    orders = query.order_by(Order.created_at.desc()).limit(50).all()
    return jsonify([o.to_dict() for o in orders])


@app.route('/api/orders/<int:order_id>', methods=['PATCH', 'DELETE'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)

    if request.method == 'DELETE':
        OrderItem.query.filter_by(order_id=order.id).delete(synchronize_session=False)
        db.session.delete(order)
        db.session.commit()
        return jsonify({'success': True})

    data = request.json

    if 'status' in data:
        order.status = data['status']
    if 'table_number' in data:
        order.table_number = data['table_number']

    db.session.commit()
    return jsonify(order.to_dict())


@app.route('/api/stats', methods=['GET'])
def stats():
    now_ist = get_ist_now()
    today_ist = now_ist.date()

    today_orders = Order.query.filter(
        db.func.date(Order.created_at) == today_ist
    ).all()

    total_sales = sum(o.total for o in today_orders if o.status == 'paid')
    pending_count = sum(1 for o in today_orders if o.status == 'pending')
    prepared_count = sum(1 for o in today_orders if o.status == 'prepared')

    return jsonify({
        'today_sales': total_sales,
        'today_order_count': len(today_orders),
        'pending_count': pending_count,
        'prepared_count': prepared_count
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
