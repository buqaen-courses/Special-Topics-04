# Workshop 3 — SQLite CRUD (raw sqlite3)

Teaches converting JSON file storage to SQLite with raw SQL queries.

## How to run

```bash
# 1. Install dependencies
pip install fastapi uvicorn jinja2 python-multipart

# 2. Start the server (auto-creates + seeds the database)
cd item_management_sqlite
uvicorn app.main:app --reload

# 3. Open in browser
#    http://127.0.0.1:8000          → Dashboard
#    http://127.0.0.1:8000/items/landing  → Items CRUD
```

No seed script needed — `app/db.py` calls `init_db()` on import.

## What's inside

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app, dashboard with SQL aggregate stats |
| `app/routes/items.py` | Full CRUD + sort/search/pagination using `WHERE` / `ORDER BY` / `LIMIT/OFFSET` |
| `app/db.py` | SQLite connection, `init_db()`, `dict_from_row()` helper |
| `app/templates/` | Jinja2 templates (green theme) |

## Reference

Full walkthrough: `full-crud-from-scratch-part3.md` (in the parent directory)
