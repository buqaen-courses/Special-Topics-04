"""Seed script — populates the database with sample data."""
import hashlib
from datetime import datetime
from app.database import SessionLocal, engine, Base
from app.models import Admin, Customer, Category, Product, Order, OrderItem

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Only seed if no admins exist
if db.query(Admin).count() > 0:
    print("Database already seeded. Skipping.")
    db.close()
    exit(0)

# --- Admin ---
admin = Admin(
    username="admin",
    password_hash=hashlib.sha256("admin123".encode()).hexdigest(),
    created_at=datetime.utcnow(),
)
db.add(admin)

# --- Customers ---
customers_data = [
    ("Alice Johnson", "alice@example.com", "+1-555-0101"),
    ("Bob Smith", "bob@example.com", "+1-555-0102"),
    ("Carol White", "carol@example.com", "+1-555-0103"),
    ("Dan Brown", "dan@example.com", "+1-555-0104"),
    ("Eve Davis", "eve@example.com", "+1-555-0105"),
]
customers = []
for name, email, phone in customers_data:
    c = Customer(name=name, email=email, phone=phone, created_at=datetime.utcnow())
    db.add(c)
    customers.append(c)
db.flush()

# --- Categories ---
categories_data = [
    ("Electronics", "Gadgets, devices, and tech accessories"),
    ("Books", "Fiction, non-fiction, and educational"),
    ("Clothing", "Apparel and fashion accessories"),
    ("Home & Kitchen", "Household items and cookware"),
    ("Sports", "Sports equipment and activewear"),
]
categories = []
for name, desc in categories_data:
    cat = Category(name=name, description=desc)
    db.add(cat)
    categories.append(cat)
db.flush()

# --- Products ---
products_data = [
    ("Wireless Mouse", "Ergonomic Bluetooth mouse", 29.99, 50, categories[0].id),
    ("USB-C Hub", "7-in-1 USB-C hub with HDMI", 45.99, 30, categories[0].id),
    ("Noise Cancelling Headphones", "Over-ear ANC headphones", 199.99, 15, categories[0].id),
    ("Python for Data Science", "Comprehensive guide", 39.99, 100, categories[1].id),
    ("The Great Gatsby", "Classic novel by F. Scott Fitzgerald", 12.99, 200, categories[1].id),
    ("Cookbook: 30-Minute Meals", "Quick and easy recipes", 24.99, 60, categories[1].id),
    ("Cotton T-Shirt", "Premium 100% cotton, unisex", 19.99, 150, categories[2].id),
    ("Denim Jacket", "Classic blue denim jacket", 89.99, 25, categories[2].id),
    ("Running Shoes", "Lightweight mesh running shoes", 129.99, 40, categories[2].id),
    ("Non-Stick Frying Pan", "12-inch ceramic non-stick", 34.99, 80, categories[3].id),
    ("Stainless Steel Water Bottle", "1L insulated bottle", 22.99, 120, categories[3].id),
    ("Chef's Knife", "8-inch professional chef knife", 59.99, 45, categories[3].id),
    ("Yoga Mat", "Extra thick non-slip mat", 29.99, 90, categories[4].id),
    ("Resistance Bands Set", "5 levels of resistance", 19.99, 70, categories[4].id),
    ("Jump Rope", "Speed jump rope with ball bearings", 14.99, 110, categories[4].id),
    ("Bluetooth Speaker", "Portable waterproof speaker", 79.99, 35, categories[0].id),
    ("Tablet Stand", "Adjustable aluminum stand", 25.99, 65, categories[0].id),
    ("Fiction Bestseller", "Award-winning novel", 18.99, 85, categories[1].id),
    ("Wool Scarf", "Soft merino wool scarf", 34.99, 55, categories[2].id),
    ("Coffee Maker", "12-cup programmable coffee maker", 49.99, 40, categories[3].id),
    ("Dumbbell Set", "Adjustable 2x20lb dumbbells", 89.99, 20, categories[4].id),
]
products = []
for name, desc, price, stock, cat_id in products_data:
    p = Product(
        name=name,
        description=desc,
        price=price,
        stock=stock,
        category_id=cat_id,
        created_at=datetime.utcnow(),
    )
    db.add(p)
    products.append(p)
db.flush()

# --- Orders ---
orders_data = [
    (customers[0], [(products[0], 2), (products[3], 1)]),
    (customers[1], [(products[2], 1), (products[7], 1)]),
    (customers[0], [(products[1], 1), (products[10], 2), (products[15], 1)]),
    (customers[2], [(products[4], 3), (products[17], 1)]),
    (customers[3], [(products[6], 2), (products[8], 1), (products[13], 1)]),
    (customers[4], [(products[5], 1), (products[9], 1)]),
    (customers[1], [(products[11], 1), (products[18], 2), (products[20], 1)]),
    (customers[2], [(products[14], 2), (products[16], 1)]),
]

for customer, line_items in orders_data:
    total = sum(qty * products[products.index(p)].price for p, qty in line_items)
    order = Order(
        customer_id=customer.id,
        order_date=datetime.utcnow(),
        total_amount=round(total, 2),
        status="completed",
    )
    db.add(order)
    db.flush()

    for product, qty in line_items:
        oi = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=qty,
            unit_price=product.price,
        )
        db.add(oi)

db.commit()
db.close()
print("Database seeded successfully!")
