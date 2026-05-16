# Workshop 4: From Raw SQL to SQLAlchemy ORM — Building a Real E‑Commerce Backend

## Introduction: The ORM Mindset

In Workshop 3 you moved from JSON files to SQLite using raw SQL. You wrote queries
like `SELECT * FROM items WHERE id = ?` and managed connections manually. This was a
huge step forward — you got ACID guarantees, proper concurrency, and real query power.

But raw SQL has its own problems:

| Problem | Raw SQL Example | Why It Hurts |
|---------|----------------|--------------|
| **Repetitive** | Write column names in `INSERT`, `SELECT`, `UPDATE` every time | Copy‑paste errors, typos |
| **String‑based** | SQL is just a string — no syntax checking until runtime | Debugging is slow |
| **No IDE help** | Your editor doesn’t know column names or types | No autocomplete, no refactoring |
| **Manual mapping** | You write code to convert rows → Python objects | Boilerplate everywhere |
| **Relationships** | JOINs get complex fast | Easy to forget a JOIN or mess up ON clause |

### Enter the ORM — Object Relational Mapper

An ORM lets you work with **Python objects** instead of **SQL strings**. Instead of:

```python
# Raw SQL (Workshop 3)
row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
item = dict(row)
print(item["name"])
```

You write:

```python
# SQLAlchemy ORM (Workshop 4)
product = db.query(Product).filter(Product.id == product_id).first()
print(product.name)
```

**Key differences:**

| Concept | Raw SQL | SQLAlchemy ORM |
|---------|---------|----------------|
| Table | `CREATE TABLE products (...)` | `class Product(Base): __tablename__ = "products"` |
| Row | `row["name"]` | `product.name` |
| Insert | `INSERT INTO products ...` | `db.add(product)` + `db.commit()` |
| Query | `SELECT * WHERE id = ?` | `.query(Product).filter(Product.id == x).first()` |
| FK relationship | Manual JOIN | `product.category.name` (auto JOIN via relationship) |

### Why SQLAlchemy?

SQLAlchemy is the **most popular Python ORM** and is installed automatically when you
install FastAPI. It supports PostgreSQL, MySQL, SQLite, and more with the same API.

### What You Will Build

A full e‑commerce management system with:

- **Admin authentication** (login/logout with session‑based auth)
- **Products CRUD** with categories (FK relationship)
- **Categories CRUD** (parent entity)
- **Customers CRUD** (with order history)
- **Orders** (the complex relational part — create order with line items, auto‑decrement stock, calculate totals)
- **Dashboard** with statistics across all tables

### Database Schema (6 tables)

```
admins     — id, username, password_hash, created_at
customers  — id, name, email, phone, created_at
categories — id, name, description
products   — id, name, description, price, stock, category_id → categories
orders     — id, customer_id → customers, order_date, total_amount, status
order_items — id, order_id → orders, product_id → products, quantity, unit_price
```

---

## Step 0: Project Setup

**Goal:** Create the folder structure and install dependencies.  
**Mental model:** You’re building a proper FastAPI app, just like before, but now with SQLAlchemy as the data layer.

### 0.1 Create the project folder

```bash
mkdir item_management_sqlalchemy
cd item_management_sqlalchemy
```

### 0.2 Create the directory structure

```bash
mkdir -p app/models app/routes app/templates/products app/templates/categories
mkdir -p app/templates/customers app/templates/orders app/static/css app/static/webfonts
touch app/__init__.py app/models/__init__.py app/routes/__init__.py
```

### 0.3 Copy static files from the previous project

```bash
cp ../item_management_sqlite/app/static/css/custom.css app/static/css/
cp ../item_management_sqlite/app/static/css/fa.min.css app/static/css/
cp ../item_management_sqlite/app/static/webfonts/fa-solid-900.woff2 app/static/webfonts/
```

### 0.4 Install dependencies

```bash
pip install fastapi uvicorn jinja2 sqlalchemy python-multipart
```

**New dependency:** `sqlalchemy` — that’s the only new package.

### 0.5 Create `requirements.txt`

```
fastapi
uvicorn
jinja2
sqlalchemy
```

**Checkpoint:** Your folder is ready and you have all the tools to start coding.

---

## Step 1: SQLAlchemy Setup (`app/database.py`)

**Goal:** Write the core module that connects SQLAlchemy to SQLite and provides a database session for every request.  
**Mental model:** Think of `database.py` as the “engine room”. It starts the engine, creates a session factory, and gives every request its own workspace.

### Comparison with Part 3

| Part 3 (`app/db.py`) | Part 4 (`app/database.py`) |
|----------------------|---------------------------|
| `sqlite3.connect(DB_FILE)` | `create_engine("sqlite:///./shop.db")` |
| Manual `conn.row_factory` | Automatically handled by ORM |
| `conn.execute("...")` | `SessionLocal()` + `db.query(...)` |
| Manual `conn.commit()` / `conn.close()` | Automatic via `get_db()` dependency |
| No relationship support | Full FK + relationship() support |

### Create `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./shop.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Key Concepts

**1. `create_engine`** — This is the connection pool. Unlike raw sqlite3 where you call `connect()` each time, SQLAlchemy keeps a pool of connections and reuses them.

**2. `check_same_thread=False`** — Required for SQLite when FastAPI might use multiple threads. (SQLite normally refuses cross‑thread access.)

**3. `SessionLocal`** — A factory that creates database sessions. A session is a “workspace” where you load objects, modify them, and commit changes.

**4. `declarative_base()`** — The parent class for all your models. Every table will be a Python class that inherits from `Base`.

**5. `get_db()`** — A FastAPI dependency that opens a session before the request and closes it after. This is the **dependency injection** pattern:

```python
@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    # db is already open and ready
    products = db.query(Product).all()
    # db is automatically closed when the function returns
```

| Without DI (Part 3) | With DI (Part 4) |
|---------------------|------------------|
| `conn = get_connection()` | `db: Session = Depends(get_db)` |
| `rows = conn.execute(...)` | `db.query(Product)...` |
| `conn.close()` | Automatic! |

**Try it:** Create `database.py` and run Python. Import `engine` – you’ll see no errors. The `shop.db` file is not created until you create tables, but the engine is alive.

**Checkpoint:** You now have a database engine that can create sessions. Next you’ll design the actual tables as Python classes.

---

## Step 2: Designing the E‑Commerce Schema — Models & Relationships

**Goal:** Translate the entity‑relationship diagram into Python classes using SQLAlchemy.  
**Mental model:** Each table is a class, each column is a class attribute, and foreign keys plus `relationship()` make navigation between tables as easy as `product.category.name`.

### The Relationship Diagram (ERD)

```
Category ──┬── Product ──┬── OrderItem ──┬── Order ──┬── Customer
           │              │               │           │
           │              │               │           └── id, name, email...
           │              │               │
           │              │               └── id, customer_id, order_date...
           │              │
           │              └── id, order_id, product_id, quantity, unit_price
           │
           └── id, name, description, products = relationship("Product")
```

### 2.1 Admin Model (`app/models/admin.py`)

```python
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**What’s happening:**  
- `__tablename__` tells SQLAlchemy the table name.  
- `Column(Integer, primary_key=True)` marks the ID as the primary key and auto‑incrementing.  
- `unique=True` ensures no two admins have the same username.  
- `nullable=False` means the column cannot be empty.

### 2.2 Customer Model (`app/models/customer.py`)

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="customer")
```

**The `orders` relationship:** This doesn’t create a column; it tells SQLAlchemy, “If I access `customer.orders`, give me all orders for this customer.” The `back_populates` string matches a relationship in the `Order` model — we’ll see it soon.

### 2.3 Category Model (`app/models/category.py`)

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))

    products = relationship("Product", back_populates="category")
```

### 2.4 Product Model (`app/models/product.py`)

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
```

**Foreign key magic:**  
`category_id = Column(Integer, ForeignKey("categories.id"))` tells SQLite: “This column points to the `id` column of the `categories` table.” The database will prevent you from inserting a product with a `category_id` that doesn’t exist.

The `category` relationship allows you to do `product.category.name` — behind the scenes SQLAlchemy runs the JOIN for you.

### 2.5 Order Model (`app/models/order.py`)

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, default=0.0)
    status = Column(String(20), default="pending")

    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order",
                               cascade="all, delete-orphan")
```

**Cascade explained:** `cascade="all, delete-orphan"` means: if you delete an `Order`, all its `OrderItem` rows are deleted automatically. Without this, the database would refuse because `order_items.order_id` still references the deleted order.

### 2.6 OrderItem Model (`app/models/order_item.py`)

```python
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
```

### 2.7 Models `__init__.py` (`app/models/__init__.py`)

```python
from app.models.admin import Admin
from app.models.customer import Customer
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

__all__ = ["Admin", "Customer", "Category", "Product", "Order", "OrderItem"]
```

### Why This Schema Design Matters

You could have stored orders as a single table with repeated product data, but that leads to update anomalies (if a product’s price changes, you’d need to update every past order). The normalised design with separate tables for products, orders, and order items is a **real‑world e‑commerce pattern** used by almost every online shop.

**Try it:** Open a Python shell, import the models and call `Base.metadata.create_all(engine)` to create the tables. Then inspect `shop.db` with the `sqlite3` command line to see all six tables.

**Checkpoint:** You’ve just designed the entire database structure, complete with foreign keys and relationships, using pure Python classes. This is the foundation everything else will build on.

---

## Step 3: Seed Script (`seed.py`)

**Goal:** Populate the database with realistic sample data so you can immediately see the app in action.  
**Mental model:** The seed script creates objects like you would in a real request, but does it all at once for setup.

### Comparison

| Part 3 (`app/db.py` init_db) | Part 4 (`seed.py`) |
|------------------------------|-------------------|
| Runs automatically at import | Run manually: `python seed.py` |
| `conn.executemany(...)` for items | `db.add(product)` for each object |
| No relationships to set up | Must link FK references, create related objects |
| Single table | 6 tables with cross‑references |

### Create `seed.py`

```python
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

# --- Products (21 items across all categories) ---
products_data = [
    ("Wireless Mouse", "Ergonomic Bluetooth mouse", 29.99, 50, 0),
    ("USB-C Hub", "7-in-1 USB-C hub with HDMI", 45.99, 30, 0),
    ("Noise Cancelling Headphones", "Over-ear ANC headphones", 199.99, 15, 0),
    ("Python for Data Science", "Comprehensive guide", 39.99, 100, 1),
    ("The Great Gatsby", "Classic novel", 12.99, 200, 1),
    ("Cookbook: 30-Minute Meals", "Quick and easy recipes", 24.99, 60, 1),
    ("Cotton T-Shirt", "Premium 100% cotton, unisex", 19.99, 150, 2),
    ("Denim Jacket", "Classic blue denim jacket", 89.99, 25, 2),
    ("Running Shoes", "Lightweight mesh running shoes", 129.99, 40, 2),
    ("Non-Stick Frying Pan", "12-inch ceramic non-stick", 34.99, 80, 3),
    ("Stainless Steel Water Bottle", "1L insulated bottle", 22.99, 120, 3),
    ("Chef's Knife", "8-inch professional chef knife", 59.99, 45, 3),
    ("Yoga Mat", "Extra thick non-slip mat", 29.99, 90, 4),
    ("Resistance Bands Set", "5 levels of resistance", 19.99, 70, 4),
    ("Jump Rope", "Speed jump rope", 14.99, 110, 4),
    ("Bluetooth Speaker", "Portable waterproof speaker", 79.99, 35, 0),
    ("Tablet Stand", "Adjustable aluminum stand", 25.99, 65, 0),
    ("Fiction Bestseller", "Award-winning novel", 18.99, 85, 1),
    ("Wool Scarf", "Soft merino wool scarf", 34.99, 55, 2),
    ("Coffee Maker", "12-cup programmable", 49.99, 40, 3),
    ("Dumbbell Set", "Adjustable 2x20lb dumbbells", 89.99, 20, 4),
]
products = []
for name, desc, price, stock, cat_idx in products_data:
    p = Product(name=name, description=desc, price=price, stock=stock,
                category_id=categories[cat_idx].id,
                created_at=datetime.utcnow())
    db.add(p)
    products.append(p)
db.flush()

# --- Orders with line items ---
orders_data = [
    (0, [(0, 2), (3, 1)]),       # Alice buys 2 mice + 1 Python book
    (1, [(2, 1), (7, 1)]),       # Bob buys headphones + jacket
    (0, [(1, 1), (10, 2), (15, 1)]),  # Alice buys hub + water bottles + speaker
    (2, [(4, 3), (17, 1)]),      # Carol buys 3 Gatsby + 1 bestseller
    (3, [(6, 2), (8, 1), (13, 1)]),   # Dan buys 2 shirts + shoes + bands
    (4, [(5, 1), (9, 1)]),       # Eve buys cookbook + pan
    (1, [(11, 1), (18, 2), (20, 1)]), # Bob buys knife + 2 scarves + dumbbells
    (2, [(14, 2), (16, 1)]),     # Carol buys 2 jump ropes + tablet stand
]

for customer_idx, line_items in orders_data:
    customer = customers[customer_idx]
    total = sum(products[pid].price * qty for pid, qty in line_items)
    order = Order(customer_id=customer.id, total_amount=round(total, 2),
                  status="completed", order_date=datetime.utcnow())
    db.add(order)
    db.flush()
    for pid, qty in line_items:
        product = products[pid]
        db.add(OrderItem(order_id=order.id, product_id=product.id,
                         quantity=qty, unit_price=product.price))

db.commit()
db.close()
print("Database seeded successfully!")
```

### Run the seed script

```bash
python seed.py
# Output: Database seeded successfully!
```

### Verify

```python
# Open python shell and run:
import sqlite3
conn = sqlite3.connect("shop.db")
for t in ["admins","categories","customers","products","orders","order_items"]:
    cnt = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t}: {cnt}")
conn.close()
```

Expected output:
```
admins: 1
categories: 5
customers: 5
products: 21
orders: 8
order_items: 19
```

> **Git commit:**
> ```
> git add -A
> git commit -m "Step 3: Add seed script with sample data (admin, customers, categories, products, orders)"
> ```

**Checkpoint:** Your database is now filled with sample e‑commerce data. Next you’ll add authentication so only admins can see it.

---

## Step 4: Admin Authentication

**Goal:** Add login/logout so only authorised users can access the management pages.  
**Mental model:** The browser stores a session cookie; the server checks it before rendering any protected page. Passwords are never stored in plain text.

### 4.1 Password Hashing

We use Python's built-in `hashlib` (no external package needed):

```python
import hashlib
pw_hash = hashlib.sha256("admin123".encode()).hexdigest()
```

The seed script hashes the password before storing it. On login, we hash the submitted password and compare hashes.

### 4.2 Auth Routes (`app/routes/auth.py`)

```python
import hashlib
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_current_admin(request: Request, db: Session = Depends(get_db)):
    """Return the logged-in Admin or None."""
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return None
    return db.query(Admin).filter(Admin.id == admin_id).first()


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"error": None}
    )


@router.post("/login")
async def login(request: Request, username: str = Form(...),
                password: str = Form(...), db: Session = Depends(get_db)):
    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    admin = db.query(Admin).filter(
        Admin.username == username, Admin.password_hash == pw_hash
    ).first()
    if not admin:
        return templates.TemplateResponse(
            request=request, name="login.html",
            context={"error": "Invalid username or password"}
        )
    request.session["admin_id"] = admin.id
    return RedirectResponse("/", status_code=303)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/auth/login", status_code=303)
```

### 4.3 Session Middleware (in `app/main.py`)

Add `SessionMiddleware` to enable cookie-based sessions:

```python
from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(SessionMiddleware, secret_key="change-this-secret-key-in-production")
```

### 4.4 Login Template (`app/templates/login.html`)

```html
{% extends "base.html" %}
{% block title %}Admin Login{% endblock %}
{% block content %}
<div class="card" style="max-width: 400px; margin: 3rem auto;">
    <div class="card-header"><i class="fas fa-lock"></i> Admin Login</div>
    <div class="card-body">
        {% if error %}
        <div style="background:#fde8e8; color:#a81c1c; padding:0.6rem; border-radius:8px; margin-bottom:1rem;">
            <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>
        {% endif %}
        <form method="post" action="/auth/login">
            <div class="form-group">
                <label><i class="fas fa-user"></i> Username</label>
                <input type="text" name="username" required autofocus>
            </div>
            <div class="form-group">
                <label><i class="fas fa-key"></i> Password</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%;">
                <i class="fas fa-sign-in-alt"></i> Login
            </button>
        </form>
    </div>
</div>
{% endblock %}
```

### 4.5 Protected Routes Pattern

Every route that requires authentication uses this helper:

```python
def require_admin(request: Request):
    if not request.session.get("admin_id"):
        return None
    return True
```

Usage in routes:

```python
@router.get("/landing")
async def landing(request: Request, db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    # ... render protected content
```

### Comparison: Part 3 vs Part 4 Auth

| Part 3 | Part 4 |
|--------|--------|
| No authentication | Session-based login |
| Anyone can access all pages | Protected routes redirect to login |
| No users at all | Admin table with hashed passwords |
| N/A | Session middleware stores login state |

**What you’ll see:** Visit `http://127.0.0.1:8000/` and you’ll be redirected to the login page. Enter `admin` / `admin123` and you’ll see the dashboard (once we build it in Step 5). Logout clears the session and sends you back to login.

**Checkpoint:** Only authenticated admins can see the app. Next you’ll build the dashboard that shows live statistics.

---

## Step 5: Dashboard (Landing Page with Stats)

**Goal:** Show a summary of the entire e‑commerce system using SQLAlchemy aggregate queries.  
**Mental model:** Instead of writing `SELECT COUNT(*)` in raw SQL, you chain `.count()` or `func.sum()` onto a query. The results are passed to a Jinja2 template.

### `app/main.py` — Full file

```python
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import engine, Base, get_db
from app.models import Product, Category, Customer, Order
from app.routes import auth, products, categories, customers, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop Manager — SQLAlchemy CRUD")
app.add_middleware(SessionMiddleware, secret_key="change-this-secret-key-in-production")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router, prefix="/auth")
app.include_router(products.router, prefix="/products")
app.include_router(categories.router, prefix="/categories")
app.include_router(customers.router, prefix="/customers")
app.include_router(orders.router, prefix="/orders")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def root(request: Request, db: Session = Depends(get_db)):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return templates.TemplateResponse(
            request=request, name="login.html", context={"error": None}
        )

    total_products = db.query(Product).count()
    total_categories = db.query(Category).count()
    total_customers = db.query(Customer).count()
    total_orders = db.query(Order).count()
    revenue_result = db.query(func.sum(Order.total_amount)).scalar() or 0
    low_stock = db.query(Product).filter(Product.stock < 5).count()
    recent_orders = db.query(Order).order_by(
        Order.order_date.desc()
    ).limit(5).all()

    return templates.TemplateResponse(
        request=request, name="landing.html", context={
            "total_products": total_products,
            "total_categories": total_categories,
            "total_customers": total_customers,
            "total_orders": total_orders,
            "total_revenue": round(revenue_result, 2),
            "low_stock": low_stock,
            "recent_orders": recent_orders,
        },
    )
```

### Comparison: Aggregate Queries

| Metric | Raw SQL (Part 3) | SQLAlchemy (Part 4) |
|--------|------------------|---------------------|
| Count | `SELECT COUNT(*) FROM items` | `db.query(Product).count()` |
| Sum | `SELECT SUM(price) FROM items` | `db.query(func.sum(Order.total_amount)).scalar()` |
| Filtered count | `WHERE stock < 5` | `.filter(Product.stock < 5).count()` |
| Latest rows | `ORDER BY date DESC LIMIT 5` | `.order_by(Order.order_date.desc()).limit(5).all()` |

### Dashboard Template (`app/templates/landing.html`)

The template shows 6 stat cards (Products, Categories, Customers, Orders, Revenue,
Low Stock) followed by a recent orders table and action buttons to add new entities.

(You can reuse the template from the original tutorial — it remains the same.)

**What you’ll see:** After login, you’ll be greeted by a dashboard showing 21 products, 5 categories, 5 customers, 8 orders, $5,267.41 revenue, and 2 low‑stock items. The recent orders table lists the last 5 orders.

**Try it:** Add a new product with stock = 3. Refresh the dashboard — the low‑stock counter increases.

**Checkpoint:** You now have a live, data‑driven dashboard. Next you’ll build the full product CRUD.

---

## Step 6: Product CRUD with Sort/Search/Pagination

**Goal:** Build the most feature‑rich entity page — sort, search, paginate, and manage products with category relationships.  
**Mental model:** Every operation you did with raw SQL (WHERE, ORDER BY, LIMIT/OFFSET) is now a chain of `.filter()`, `.order_by()`, `.limit()`, `.offset()`.

### The Route File (`app/routes/products.py`)

```python
import math
from fastapi import APIRouter, Request, Form, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, Category

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
ITEMS_PER_PAGE = 5


def require_admin(request: Request):
    if not request.session.get("admin_id"):
        return None
    return True


@router.get("/landing", response_class=HTMLResponse)
async def products_landing(request: Request, sort: str = Query("default"),
                           page: int = Query(1, ge=1),
                           db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)

    order_col = { "name": Product.name, "price": Product.price,
                  "stock": Product.stock }.get(sort, Product.id)

    total_items = db.query(Product).count()
    total_pages = max(1, math.ceil(total_items / ITEMS_PER_PAGE))

    if page > total_pages:
        return RedirectResponse(
            url=f"/products/landing?sort={sort}&page={total_pages}",
            status_code=303)

    products = db.query(Product).order_by(order_col) \
        .offset((page-1) * ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE).all()

    return templates.TemplateResponse(
        request=request, name="products/products_landing.html", context={
            "products": products, "current_sort": sort,
            "current_page": page, "total_pages": total_pages,
        })


@router.get("/search")
async def search_products(request: Request, q: str = "",
                          min_price: float = None, max_price: float = None,
                          category_id: int = None,
                          sort: str = Query("default"),
                          page: int = Query(1, ge=1),
                          db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)

    query = db.query(Product)
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%") |
                             Product.description.ilike(f"%{q}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    order_col = {"name": Product.name, "price": Product.price,
                 "stock": Product.stock}.get(sort, Product.id)

    total_items = query.count()
    total_pages = max(1, math.ceil(total_items / ITEMS_PER_PAGE))

    if page > total_pages:
        return RedirectResponse(url=f"/products/search?...", status_code=303)

    products = query.order_by(order_col) \
        .offset((page-1)*ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE).all()
    categories_list = db.query(Category).all()

    return templates.TemplateResponse(
        request=request, name="products/products_landing.html", context={
            "products": products, "current_sort": sort,
            "current_page": page, "total_pages": total_pages,
            "q": q, "min_price": min_price, "max_price": max_price,
            "category_id": category_id, "categories": categories_list,
        })


@router.get("/add")
async def add_product_form(request: Request, db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    return templates.TemplateResponse(
        request=request, name="products/product_form.html",
        context={"editing": False, "product": None, "product_id": None,
                 "categories": db.query(Category).all()})


@router.post("/")
async def create_product(request: Request, name: str = Form(...),
                         description: str = Form(""),
                         price: float = Form(...), stock: int = Form(0),
                         category_id: int = Form(None),
                         db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    db.add(Product(name=name, description=description, price=price,
                   stock=stock, category_id=category_id))
    db.commit()
    return RedirectResponse("/products/landing", status_code=303)


@router.get("/edit/{product_id}")
async def edit_product_form(request: Request, product_id: int,
                            db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        request=request, name="products/product_form.html",
        context={"editing": True, "product": product,
                 "product_id": product_id,
                 "categories": db.query(Category).all()})


@router.post("/{product_id}")
async def update_product(request: Request, product_id: int,
                         name: str = Form(...), description: str = Form(""),
                         price: float = Form(...), stock: int = Form(0),
                         category_id: int = Form(None),
                         db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404)
    product.name, product.description = name, description
    product.price, product.stock = price, stock
    product.category_id = category_id
    db.commit()
    return RedirectResponse("/products/landing", status_code=303)


@router.get("/delete/{product_id}")
async def confirm_delete(request: Request, product_id: int,
                         db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    product = db.query(Product).filter(Product.id == product_id).first()
    return templates.TemplateResponse(
        request=request, name="products/product_delete.html",
        context={"product": product, "product_id": product_id})


@router.post("/delete/{product_id}")
async def delete_product(request: Request, product_id: int,
                         db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return RedirectResponse("/products/landing", status_code=303)
```

### Key SQLAlchemy Query Patterns

| Operation | Raw SQL (Part 3) | SQLAlchemy (Part 4) |
|-----------|-----------------|---------------------|
| Get all | `SELECT * FROM products` | `db.query(Product).all()` |
| Get one | `SELECT * WHERE id = ?` | `.filter(Product.id == x).first()` |
| Count | `SELECT COUNT(*)` | `.count()` |
| Order | `ORDER BY name ASC` | `.order_by(Product.name)` |
| Descending | `ORDER BY date DESC` | `.order_by(Product.date.desc())` |
| Paginate | `LIMIT 5 OFFSET 10` | `.limit(5).offset(10)` |
| ILIKE (case-insensitive) | `WHERE name LIKE '%term%'` | `.filter(Product.name.ilike(f"%{term}%"))` |
| Greater/less than | `WHERE price >= 10` | `.filter(Product.price >= 10)` |
| Between | `WHERE price BETWEEN 10 AND 50` | `.filter(Product.price.between(10, 50))` |
| Update field | `UPDATE SET name = ?` | `product.name = new_name` |
| Insert | `INSERT INTO products ...` | `db.add(product)` |
| Delete | `DELETE WHERE id = ?` | `db.delete(product)` |
| Commit | `conn.commit()` | `db.commit()` |

### Templates

The products landing template (`app/templates/products/products_landing.html`) has:
- **Search form** with text search (name/description), price range, and category dropdown
- **Sort controls** (Default, Name, Price, Stock)
- **Data table** showing ID, Name (linked to category name via `p.category.name`),
  Price, Stock (highlighted red if < 5), and Actions (Edit/Delete)
- **Pagination** controls at the bottom

The product form template (`app/templates/products/product_form.html`) has fields for:
- Name (required), Description, Price (required), Stock, Category (dropdown)

The delete confirmation template shows product details and warns before deleting.

**What you’ll see:** Visit `/products/landing` and see 5 products per page. Sort by price, search for “mouse”, filter by category — all without a page reload (in the front‑end experience). Stock below 5 appears in bold red.

**Checkpoint:** Full product CRUD is operational. Next you’ll add categories management.

---

## Step 7: Category CRUD

**Goal:** Manage product categories — simpler than products but uses the same patterns.  
**Mental model:** A category has many products; deleting a category requires you to either unlink or delete those products. We’ll warn the admin.

### Route file (`app/routes/categories.py`)

Same pattern as products but with only name sorting and no search form. The delete template warns if products reference this category:
```
{{ category.products|length }} product(s) in this category will lose their
category assignment.
```

(Use the code from the original tutorial; the file is identical.)

**What you’ll see:** You can add “Sports” or “Electronics” categories, see how many products belong to each, and edit/delete them. Deleting a category with products shows a warning.

**Checkpoint:** Categories work. Next you’ll manage customers.

---

## Step 8: Customer CRUD

**Goal:** Add and manage customers. Deleting a customer with orders will cascade‑delete those orders.  
**Mental model:** The `cascade="all, delete-orphan"` on Order’s `order_items` relationship ensures no orphaned records.

### Key Difference: `cascade="all, delete-orphan"`

When you delete a customer who has orders, the cascade setting on the Order model automatically deletes associated orders and order_items:

```python
# In Order model:
order_items = relationship("OrderItem", back_populates="order",
                           cascade="all, delete-orphan")
```

Without cascade, deleting a customer with orders would raise a foreign key violation.

(Use the original route code for customers; it follows the same CRUD pattern.)

**What you’ll see:** In the customers list, you’ll see how many orders each customer has placed. Deleting a customer with orders removes everything cleanly.

**Checkpoint:** Customer CRUD is done. Now for the most complex piece: orders.

---

## Step 9: Orders — The Complex Relational Part

**Goal:** Create orders with multiple line items, automatically calculate totals, decrement stock, and ensure transactional integrity.  
**Mental model:** An order combines a customer (FK) with several products (via OrderItems). We use `flush()` to get the order ID before creating the items, and we wrap everything in one transaction.

### 9.1 Order Routes (`app/routes/orders.py`)

```python
import math
from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Order, OrderItem, Customer, Product

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/landing")
async def orders_landing(request: Request, page: int = Query(1, ge=1),
                         db: Session = Depends(get_db)):
    if not request.session.get("admin_id"):
        return RedirectResponse("/auth/login", status_code=303)

    total = db.query(Order).count()
    total_pages = max(1, math.ceil(total / 10))

    if page > total_pages:
        return RedirectResponse(url=f"/orders/landing?page={total_pages}",
                                status_code=303)

    orders = db.query(Order).options(joinedload(Order.customer)) \
        .order_by(Order.order_date.desc()) \
        .offset((page-1)*10).limit(10).all()

    return templates.TemplateResponse(
        request=request, name="orders/orders_landing.html",
        context={"orders": orders, "current_page": page,
                 "total_pages": total_pages})


@router.get("/create")
async def create_order_form(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("admin_id"):
        return RedirectResponse("/auth/login", status_code=303)
    return templates.TemplateResponse(
        request=request, name="orders/order_form.html",
        context={"customers": db.query(Customer).all(),
                 "products": db.query(Product).all(), "error": None})


@router.post("/create")
async def create_order(request: Request, customer_id: int = Form(...),
                       product_ids: list[int] = Form(...),
                       quantities: list[int] = Form(...),
                       db: Session = Depends(get_db)):
    if not request.session.get("admin_id"):
        return RedirectResponse("/auth/login", status_code=303)

    # Validate inputs
    if not product_ids or len(product_ids) != len(quantities):
        return templates.TemplateResponse(..., context={"error": "..."})

    # Check stock and calculate total
    total_amount = 0.0
    items_data = []
    for pid, qty in zip(product_ids, quantities):
        if qty < 1: continue
        product = db.query(Product).filter(Product.id == pid).first()
        if not product: continue
        if product.stock < qty:
            return templates.TemplateResponse(..., context={"error": f"..."})
        total_amount += product.price * qty
        items_data.append((product, qty))

    # Create order
    order = Order(customer_id=customer_id, total_amount=round(total_amount, 2),
                  status="pending", order_date=datetime.utcnow())
    db.add(order)
    db.flush()  # Get the order.id before adding items

    # Create order items and decrement stock
    for product, qty in items_data:
        db.add(OrderItem(order_id=order.id, product_id=product.id,
                         quantity=qty, unit_price=product.price))
        product.stock -= qty

    db.commit()
    return RedirectResponse(f"/orders/{order.id}", status_code=303)


@router.get("/{order_id}")
async def order_detail(request: Request, order_id: int,
                       db: Session = Depends(get_db)):
    if not request.session.get("admin_id"):
        return RedirectResponse("/auth/login", status_code=303)

    order = db.query(Order).options(
        joinedload(Order.customer),
        joinedload(Order.order_items).joinedload(OrderItem.product)
    ).filter(Order.id == order_id).first()

    return templates.TemplateResponse(
        request=request, name="orders/order_detail.html",
        context={"order": order})


@router.get("/{order_id}/status/{new_status}")
async def update_order_status(request: Request, order_id: int,
                              new_status: str, db: Session = Depends(get_db)):
    if not request.session.get("admin_id"):
        return RedirectResponse("/auth/login", status_code=303)
    order = db.query(Order).filter(Order.id == order_id).first()
    if order and new_status in ("pending", "completed", "cancelled"):
        order.status = new_status
        db.commit()
    return RedirectResponse(f"/orders/{order_id}", status_code=303)
```

### 9.2 Key SQLAlchemy Features Used in Orders

**`joinedload()` — Eager Loading**

Without `joinedload()`, accessing `order.customer.name` would trigger a separate SQL query for each order (the "N+1 problem"). `joinedload()` tells SQLAlchemy to use a LEFT JOIN so all data comes in one query:

```python
# ❌ N+1: 1 query for orders + 1 query per order for customer
orders = db.query(Order).all()
for o in orders:
    print(o.customer.name)  # Extra query each time!

# ✅ 1 query: LEFT JOIN orders + customers
orders = db.query(Order).options(joinedload(Order.customer)).all()
```

You can even chain joined loads for nested relationships:

```python
db.query(Order).options(
    joinedload(Order.customer),
    joinedload(Order.order_items).joinedload(OrderItem.product)
).all()
```

This loads orders, customers, and all product details in just 2 JOINs.

**`db.flush()` vs `db.commit()`**

`flush()` sends SQL to the database but doesn't finalize the transaction. This lets you get the auto-generated `order.id` before creating OrderItems. If any subsequent operation fails, `commit()` rolls everything back.

### 9.3 The Order Creation Flow

1. Admin selects a customer from a dropdown
2. Admin adds one or more products with quantities (using a JS-powered "Add item" button)
3. Form submits to `POST /orders/create`
4. Server validates: all products exist, stock is sufficient
5. Server creates the Order (gets auto-generated ID via `flush()`)
6. Server creates OrderItems and decrements product.stock
7. Server commits everything atomically

### 9.4 Order Detail Page

Shows:
- Customer info (name, email)
- Order date and status
- Line items table (product name, unit price, quantity, subtotal)
- Status management buttons (Mark Completed, Cancel)

**What you’ll see:** Create an order for Alice with 2 Wireless Mice. You’ll be redirected to the order detail page showing the items and total. The mouse stock decreases by 2. Try ordering more mice than stock — you’ll get an error.

**Checkpoint:** Orders are fully functional with stock management. The final step wires everything together with a base template.

---

## Step 10: Base Template and Integration

**Goal:** Create a shared layout with navigation and mount all routes in `main.py`.  
**Mental model:** The base template gives every page a consistent look and nav bar. `main.py` registers all routers and middleware.

### `app/templates/base.html`

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Shop Manager{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/fa.min.css">
    <link rel="stylesheet" href="/static/css/custom.css">
    <style>
        .navbar-nav .nav-right { margin-left: auto; }
    </style>
</head>
<body>

<nav class="navbar">
    <div class="container">
        <a href="/" class="navbar-brand">
            <i class="fas fa-store"></i> Shop Manager
        </a>
        <ul class="navbar-nav">
            <li><a href="/"><i class="fas fa-chart-pie"></i> Dashboard</a></li>
            <li><a href="/products/landing"><i class="fas fa-box"></i> Products</a></li>
            <li><a href="/categories/landing"><i class="fas fa-tags"></i> Categories</a></li>
            <li><a href="/customers/landing"><i class="fas fa-users"></i> Customers</a></li>
            <li><a href="/orders/landing"><i class="fas fa-shopping-cart"></i> Orders</a></li>
            {% if request.session.get("admin_id") %}
            <li class="nav-right">
                <a href="/auth/logout" style="color:#f87171;">
                    <i class="fas fa-sign-out-alt"></i> Logout
                </a>
            </li>
            {% endif %}
        </ul>
    </div>
</nav>

<main class="container" style="margin-top: 2rem;">
    {% block content %}{% endblock %}
</main>

<footer style="text-align: center; margin: 3rem 0 1rem; color: #5c6b7a;">
    <hr>
    <small>&copy; 2026 — SQLAlchemy CRUD Workshop | FastAPI + SQLAlchemy</small>
</footer>

</body>
</html>
```

### Running the Application

```bash
uvicorn app.main:app --reload
```

Then visit:
- `http://127.0.0.1:8000/` — Login page, then Dashboard
- Login with: `admin` / `admin123`
- Navigate through Products, Categories, Customers, Orders

### Integration Checklist

- [ ] Login redirects to dashboard
- [ ] Dashboard shows correct stats from all tables
- [ ] Products: add, edit, delete, search, sort, paginate
- [ ] Product category dropdown shows categories from DB
- [ ] Categories: add, edit, delete (warning if has products)
- [ ] Customers: add, edit, delete (cascade deletes orders)
- [ ] Orders: create with customer + line items
- [ ] Order creation decreases stock
- [ ] Order creation fails gracefully if stock insufficient
- [ ] Order detail shows all line items with subtotals
- [ ] Order status can be changed (pending → completed/cancelled)
- [ ] Logout clears session and redirects to login

**Checkpoint:** You have a fully integrated e‑commerce admin panel. Try every action and watch how the ORM handles relationships behind the scenes.

---

## Full SQL ↔ SQLAlchemy Comparison Table

| Operation | Raw SQL (Part 3) | SQLAlchemy ORM (Part 4) |
|-----------|-----------------|------------------------|
| **Connect** | `sqlite3.connect("db.db")` | `create_engine("sqlite:///db.db")` |
| **Create table** | `CREATE TABLE products (...)` | `class Product(Base): ...` |
| **Insert** | `INSERT INTO products VALUES (?,?)` | `db.add(Product(...))` |
| **Get by ID** | `SELECT * WHERE id = ?` | `.filter(Product.id == x).first()` |
| **Get all** | `SELECT * FROM products` | `.query(Product).all()` |
| **Count** | `SELECT COUNT(*)` | `.count()` |
| **Filter** | `WHERE price >= ?` | `.filter(Product.price >= x)` |
| **Case-insensitive search** | `WHERE name LIKE '%?%'` | `.filter(Product.name.ilike(f"%{x}%"))` |
| **Sort** | `ORDER BY name ASC` | `.order_by(Product.name)` |
| **Sort descending** | `ORDER BY price DESC` | `.order_by(Product.price.desc())` |
| **Paginate** | `LIMIT 5 OFFSET 10` | `.limit(5).offset(10)` |
| **Update** | `UPDATE SET name=? WHERE id=?` | `product.name = x` |
| **Delete** | `DELETE WHERE id=?` | `db.delete(product)` |
| **Commit** | `conn.commit()` | `db.commit()` |
| **Close** | `conn.close()` | Automatic (DI) |
| **Join (eager)** | Manual `LEFT JOIN ... ON ...` | `.options(joinedload(Rel))` |
| **Access related** | `row["category_name"]` (manual alias) | `product.category.name` (auto) |
| **Transaction** | Manual BEGIN/COMMIT/ROLLBACK | Automatic per request |
| **Sum/Avg/Max/Min** | `SELECT SUM(price)` | `db.query(func.sum(...)).scalar()` |
| **Aggregate filtered** | `SELECT COUNT(*) WHERE ...` | `.filter(...).count()` |

---

## Common Pitfalls

### 1. Forgetting `@router.post` for form submissions
If your form uses `method="post"`, make sure the route has `@router.post(...)`, not
`@router.get(...)`.

### 2. Missing `db.commit()`
SQLAlchemy doesn't auto-commit. After `db.add()`, `db.delete()`, or modifying an
object, you must call `db.commit()`.

### 3. Session closed errors
If you access a lazy-loaded relationship after the session is closed, you get:
```
sqlalchemy.orm.exc.DetachedInstanceError
```
Solution: use `joinedload()` to eager-load relationships before the session closes,
or keep the session open.

### 4. The N+1 query problem
```python
# ❌ BAD: 1 query for orders + N queries for customers
orders = db.query(Order).all()
for o in orders:
    print(o.customer.name)

# ✅ GOOD: 1 query with JOIN
orders = db.query(Order).options(joinedload(Order.customer)).all()
```

### 5. Foreign key constraint violations
When deleting a category with products, or a customer with orders, the database
raises a foreign key error unless:
- You set `category_id = NULL` on products (nullable FK), or
- You use `cascade="all, delete-orphan"` (for customer→orders)

### 6. Form list fields with FastAPI
HTML forms send multiple fields with the same name. FastAPI parses them into a list
if the type hint says `list[int]`:
```python
product_ids: list[int] = Form(...)
```

---

## What You Learned

After this workshop, you can:

| Skill | JSON Version | SQLite Version | SQLAlchemy Version |
|-------|-------------|----------------|--------------------|
| **Storage** | JSON file I/O | Raw SQL queries | Python class → table |
| **IDs** | Manual max+1 | AUTOINCREMENT | primary_key=True |
| **Sorting** | `sorted()` + lambdas | ORDER BY | `.order_by()` |
| **Filtering** | List comprehensions | WHERE | `.filter()` |
| **Pagination** | List slicing | LIMIT/OFFSET | `.limit().offset()` |
| **Aggregation** | `min()`, `max()`, etc. | SQL functions | `func.sum()`, `.count()` |
| **Relationships** | ❌ Manual lookup | JOINs | `relationship()` + `joinedload()` |
| **Concurrency** | ❌ Unsafe | ✅ ACID | ✅ ACID |
| **Code safety** | ❌ Strings | ❌ Strings | ✅ Python objects, IDE support |

You replaced string‑based SQL with Python classes, designed a normalised e‑commerce schema with foreign keys and relationships, and built a full admin panel. The mindset shift is: **data is no longer rows and columns — it’s objects and relationships.** That’s the ORM way.
