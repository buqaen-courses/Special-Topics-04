# Workshop 4 — SQLAlchemy ORM + E-Commerce Schema

Teaches SQLAlchemy ORM with 6 related tables (admins, customers, categories, products, orders, order_items) and session-based admin authentication.

## How to run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed the database (admin, 5 categories, 5 customers, 21 products, 8 orders)
cd item_management_sqlalchemy
python seed.py

# 3. Start the server
uvicorn app.main:app --reload

# 4. Open in browser
#    http://127.0.0.1:8000
#    Login: admin / admin123
```

## What's inside

| Layer | Files | Purpose |
|-------|-------|---------|
| **Models** | `app/models/*.py` | 6 SQLAlchemy models with `relationship()` and `ForeignKey` |
| **Routes** | `app/routes/*.py` | HTML-rendered CRUD for products, categories, customers, orders |
| **Auth** | `app/routes/auth.py` | Session-based login/logout with `SessionMiddleware` |
| **Templates** | `app/templates/**/*.html` | Green-theme Jinja2 templates (12 files across 4 entity folders) |

## Reference

Full walkthrough: `full-crud-from-scratch-part4.md` (in the parent directory)
