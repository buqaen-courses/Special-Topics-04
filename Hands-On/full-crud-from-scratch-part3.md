# Workshop 3: From JSON to SQLite — The Database Mindset

## Introduction: The True Mindset Shift

In Workshops 1 and 2 you stored your data in a **JSON file**. Every time you needed an
item, you loaded the entire file into memory, searched through a Python list, modified
it in RAM, and wrote the whole thing back to disk.

This works fine for a single user on a laptop. But ask yourself:

> **What happens when two people try to delete different items at the same instant?**

With JSON:
1. User A loads the file (sees 5 items)
2. User B loads the file (sees 5 items)
3. User A deletes item #3 and saves (4 items remain)
4. User B deletes item #2 and saves — **but User B still has the old list of 5!**
5. User B's save **overwrites** User A's change. Item #3 is back from the dead.

This is called a **race condition**, and it's just one of many problems with file‑based
storage.

### Why Databases Exist

A database is not just "a better way to store data". It is a **concurrent, queryable,
transactional system** that guarantees:

| Property | What It Means | JSON File | SQLite |
|----------|---------------|-----------|--------|
| **Atomicity** | Operations succeed completely or not at all | ❌ Partial writes corrupt the file | ✅ Transactions |
| **Consistency** | Data always follows rules (e.g. no negative prices) | ❌ Your code must enforce everything | ✅ Constraints + types |
| **Isolation** | Concurrent users don't interfere | ❌ Last‑write‑wins destroys data | ✅ WAL mode, row‑level locking |
| **Durability** | Committed data survives crashes | ❌ File can be half‑written | ✅ Write‑ahead log |

### Why SQLite?

SQLite is the **most deployed database engine in the world**. Every phone, browser, and
many embedded devices use it. For this workshop:

- **Zero configuration** — no server to install, no passwords, no ports
- **Single file** — your whole database is one `items.db` file
- **Built into Python** — `import sqlite3`, zero dependencies
- **SQL** — you learn the language that every database speaks (PostgreSQL, MySQL, etc.)

### What You Will Learn

By converting your JSON‑based CRUD app to SQLite, you will:

1. ✅ Replace `load_items()` / `save_items()` with **SQL queries**
2. ✅ Replace Python list sorting with **`ORDER BY`**
3. ✅ Replace Python filtering with **`WHERE` clauses**
4. ✅ Replace Python slicing with **`LIMIT` / `OFFSET`**
5. ✅ Replace hand‑rolled ID generation with **`AUTOINCREMENT`**
6. ✅ Replace `items[item_id]` index tricks with **`WHERE id = ?` lookups**
7. ✅ See **exactly what a database does for you** that you were doing manually

---

## Step 0: Create the SQLite Project

**Goal:** Set up a fresh copy of your JSON‑based project so you can safely migrate it to SQLite.  
**Mental model:** You're not starting from scratch — you're swapping out the data layer while keeping the web layer (FastAPI routes and Jinja2 templates) exactly the same.

### 0.1 Copy the JSON‑based project

```bash
# From your workspace root
cp -r item_management item_management_sqlite
cd item_management_sqlite
```

### 0.2 Remove the JSON data file

```bash
rm items.json
```

The database will replace it.

### 0.3 Install dependencies (if not already done)

```bash
pip install fastapi uvicorn jinja2 python-multipart
```

**No new package needed!** `sqlite3` is part of Python's standard library.

**What you'll see:** Your `item_management_sqlite` folder is identical to the previous project except that `items.json` is gone. The templates and routes are still there, waiting to be upgraded.

**Checkpoint:** You have a clean project ready for the database layer.

---

## Step 1: Create the Database Module (`app/db.py`)

**Goal:** Write a single module that handles all database connectivity — creating the file, defining the table, seeding sample data, and providing connections to every route.  
**Mental model:** This module is the "engine room". Routes will import `get_connection()` to talk to SQLite and `init_db()` will be called once when the server starts to ensure the table exists and has data.

### The Complete `app/db.py`

```python
import sqlite3
import os

DB_FILE = "items.db"


def get_connection():
    """Get a database connection with row factory for named column access."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row      # ← lets you write row["name"] instead of row[0]
    conn.execute("PRAGMA journal_mode=WAL")  # ← better concurrent performance
    return conn


def init_db():
    """Create the items table if it doesn't exist and seed with sample data."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            is_offer INTEGER DEFAULT 0,
            tax REAL DEFAULT 0.0
        )
    """)

    # Seed data if table is empty
    count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    if count == 0:
        sample = [
            ("Laptop", 999.99, 1, 99.99),
            ("Mouse", 25.50, 0, 2.55),
            ("Keyboard", 75.00, 1, 7.50),
            ("Monitor", 299.99, 0, 29.99),
            # … 22 items total (same as the original seed)
        ]
        conn.executemany(
            "INSERT INTO items (name, price, is_offer, tax) VALUES (?, ?, ?, ?)",
            sample,
        )

    conn.commit()
    conn.close()


def dict_from_row(row):
    """Convert a sqlite3.Row to a plain dict."""
    if row is None:
        return None
    return dict(row)
```

### Key Concepts Explained

**1. `sqlite3.Row` as row_factory**

Without this, columns are accessed by index: `row[0]` for id, `row[1]` for name, etc.
With `sqlite3.Row`, you access by name: `row["name"]`, `row["price"]`. We then wrap
with `dict(row)` to get a regular Python dict that templates can iterate.

Compare:

| JSON approach | SQLite approach |
|---------------|-----------------|
| `item["name"]` | `row["name"]` (same!) |
| `item["price"]` | `row["price"]` (same!) |

The templates don't change because both produce dicts with the same keys.

**2. `INTEGER PRIMARY KEY AUTOINCREMENT`**

In the JSON version, you manually generated IDs:
```python
new_id = max([item["id"] for item in items], default=-1) + 1
```

With SQLite, the database does this automatically. Every inserted row gets a unique,
ever‑increasing ID. No collisions, no race conditions, no manual work.

**3. `INTEGER` instead of `BOOL` for `is_offer`**

SQLite has no native boolean type. You store `is_offer` as an integer:
- `1` = True (on offer)
- `0` = False (not on offer)

**4. `?` placeholders**

Never insert values directly into SQL strings (SQL injection risk). Always use `?`
placeholders:

```python
# ❌ DANGEROUS — never do this
conn.execute(f"SELECT * FROM items WHERE name = '{user_input}'")

# ✅ SAFE — parameterised query
conn.execute("SELECT * FROM items WHERE name = ?", (user_input,))
```

**Try it:** Create `app/db.py` and then open a Python shell. Run:

```python
from app.db import init_db
init_db()
```

Then check your folder — `items.db` has appeared. Open it with the `sqlite3` command to see the table:

```bash
sqlite3 items.db ".tables"
sqlite3 items.db "SELECT COUNT(*) FROM items;"
```

You'll see the `items` table and 22 rows. This proves your database is alive.

**Checkpoint:** The database module is ready. Next you'll rewire the dashboard to ask SQLite instead of reading JSON.

---

## Step 2: Rewrite the Landing Page (`app/main.py`)

**Goal:** Replace the JSON‑based dashboard with live SQL aggregate queries.  
**Mental model:** Instead of loading every item into Python and computing stats with `min()`, `max()`, and `len()`, you ask the database to do that work with one‑liner SQL functions. You get the numbers instantly without pulling all rows into memory.

### BEFORE (JSON version)

```python
@app.get("/")
async def root(request: Request):
    items = load_items()
    total = len(items)
    offers = [i for i in items if i.get("is_offer", False)]
    offers_count = len(offers)
    prices = [i["price"] for i in items if "price" in i]
    total_value = sum(prices) if prices else 0
    avg_price = total_value / total if total > 0 else 0
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    ...
```

**Problems with this approach:**
- Loads **every item** from disk just to compute aggregates
- Does min/max/avg in Python — the database could do it faster
- No data integrity — JSON files can have missing fields

### AFTER (SQLite version — full `app/main.py`)

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db import init_db, get_connection, dict_from_row
from app.routes import items

# Create the table and seed it on first run
init_db()

app = FastAPI(title="Shop Manager — SQLite Edition")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(items.router, prefix="/items")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def root(request: Request):
    conn = get_connection()

    total = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    offers_count = conn.execute(
        "SELECT COUNT(*) FROM items WHERE is_offer = 1"
    ).fetchone()[0]
    regular_count = total - offers_count

    stats = conn.execute(
        "SELECT MIN(price) as min_price, MAX(price) as max_price, "
        "AVG(price) as avg_price, SUM(price) as total_value FROM items"
    ).fetchone()

    conn.close()

    min_price = stats["min_price"] or 0
    max_price = stats["max_price"] or 0
    avg_price = stats["avg_price"] or 0
    total_value = stats["total_value"] or 0
    offers_pct = offers_count / total * 100
    
    return templates.TemplateResponse(
        request=request, name="landing.html", context={
            "total_items": total,
            "offers_count": offers_count,
            "regular_count": regular_count,
            "min_price": round(min_price, 2),
            "max_price": round(max_price, 2),
            "avg_price": round(avg_price, 2),
            "total_value": round(total_value, 2),
            "offers_pct" : offers_pct
        },
    )
```

### What Changed

| JSON Version | SQLite Version | Why Better |
|--------------|----------------|------------|
| `len(items)` | `SELECT COUNT(*)` | Database returns one number instead of all rows |
| List comprehension for offers | `SELECT COUNT(*) WHERE is_offer = 1` | Filtered at source |
| `min()`, `max()`, `sum()` in Python | `SELECT MIN/MAX/AVG/SUM(...)` | Database does aggregation internally |
| `load_items()` called every request | `get_connection()` / `close()` | Connection pool, no file I/O |

**Try it:** Start the server with `uvicorn app.main:app --reload`. Open `http://localhost:8000/`. You'll see the same dashboard as before, but now the numbers come directly from SQLite. Check the terminal — there's no `load_items()` log because the database handles everything.

**Checkpoint:** The dashboard is now powered by SQL. Next you'll convert the core CRUD routes.

---

## Step 3: Rewrite the Items Routes (`app/routes/items.py`)

**Goal:** Transform every list‑based operation (create, read, update, delete, search) into SQL queries.  
**Mental model:** The database is now your single source of truth. You never load all items unless absolutely necessary; instead, you ask precise questions with `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.

### 3.1 The Old `load_items()` / `save_items()` Pattern

**JSON version:**
```python
def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# No save_items existed — each route wrote directly to file
```

**SQLite version:** There is no `load_items()` anymore. Each route opens a connection, runs a query, and closes. The database manages persistence.

The old `load_items()` is kept in `items.py` only as a convenience for routes that truly need all items (though you'll see we replace even those with SQL).

### 3.2 LIST — `GET /items/landing`

**JSON version** (old):
```python
items = load_items()          # load ALL items from JSON
if sort == "name":
    items = sorted(items, key=lambda x: x["name"].lower())  # sort in Python
# ... count, slice in Python ...
paginated_items = items[start:end]
```

**SQLite version** (new):
```python
conn = get_connection()

# Build ORDER BY dynamically
order = "ORDER BY id ASC"
if sort == "name":
    order = "ORDER BY name COLLATE NOCASE ASC"

# Count WITHOUT loading all data
total_items = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]

# Paginate WITH the database
offset = (page - 1) * ITEMS_PER_PAGE
rows = conn.execute(
    f"SELECT * FROM items {order} LIMIT ? OFFSET ?",
    (ITEMS_PER_PAGE, offset),
).fetchall()
conn.close()

paginated_items = [dict_from_row(r) for r in rows]
```

**Key differences:**

| Operation | JSON (Python) | SQLite (SQL) |
|-----------|---------------|--------------|
| Count | `len(items)` — loads everything | `SELECT COUNT(*)` — one number |
| Sort by name | `sorted(items, key=lambda x: x["name"].lower())` | `ORDER BY name COLLATE NOCASE ASC` |
| Sort by price | `sorted(items, key=lambda x: x["price"])` | `ORDER BY price ASC` |
| Paginate | `items[start:end]` (slicing) | `LIMIT 5 OFFSET 0` |
| Case‑insensitive | `.lower()` on every compare | `COLLATE NOCASE` (built‑in) |

**Why `COLLATE NOCASE`?** SQLite can compare strings case‑insensitively without
you having to call `.lower()` on every item. It's faster and cleaner.

### 3.3 CREATE — `POST /items/`

**JSON version:**
```python
items = load_items()
new_item = {"name": name, "price": price, "is_offer": is_offer, "tax": price * 0.1}
items.append(new_item)
with open(DATA_FILE, "w") as f:
    json.dump(items, f, indent=4)
```

**SQLite version:**
```python
conn = get_connection()
conn.execute(
    "INSERT INTO items (name, price, is_offer, tax) VALUES (?, ?, ?, ?)",
    (name, price, int(is_offer), round(price * 0.1, 2)),
)
conn.commit()
conn.close()
```

**What's better:**
- No ID generation — `AUTOINCREMENT` handles it
- No file read/write — just an INSERT
- No loading the entire dataset to add one item
- `int(is_offer)` — converts Python `bool` to SQLite `INTEGER`

### 3.4 READ one item (for edit form) — `GET /items/edit/{item_id}`

**JSON version:**
```python
items = load_items()
if item_id < 0 or item_id >= len(items):
    raise HTTPException(status_code=404, detail="Item not found")
item = items[item_id]    # ← Using item_id as a LIST INDEX!
```

**This is a bug in the JSON version!** It treats `item_id` as an array index, not
as a real identifier. If you delete item #2, item #3 becomes index 2, and the URL
`/items/edit/3` now edits the wrong item.

**SQLite version:**
```python
conn = get_connection()
row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
conn.close()

if row is None:
    raise HTTPException(status_code=404, detail="Item not found")

item = dict_from_row(row)
```

**Why this is correct:**
- `WHERE id = ?` finds the row by its actual primary key
- IDs are stable — deleting a row doesn't change other IDs
- No "off‑by‑one" bugs after deletion

### 3.5 UPDATE — `POST /items/{item_id}`

**JSON version:**
```python
items = load_items()
if item_id < 0 or item_id >= len(items):
    raise HTTPException(...)
items[item_id] = {"id": item_id, "name": name, "price": price, ...}
with open(DATA_FILE, "w") as f:
    json.dump(items, f, indent=4)
```

**SQLite version:**
```python
conn = get_connection()
row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
if row is None:
    conn.close()
    raise HTTPException(status_code=404, detail="Item not found")

conn.execute(
    "UPDATE items SET name = ?, price = ?, is_offer = ?, tax = ? WHERE id = ?",
    (name, price, int(is_offer), round(price * 0.1, 2), item_id),
)
conn.commit()
conn.close()
```

### 3.6 DELETE — `POST /items/delete/{item_id}`

**JSON version:**
```python
items = load_items()
if item_id < 0 or item_id >= len(items):
    raise HTTPException(...)
items.pop(item_id)
with open(DATA_FILE, "w") as f:
    json.dump(items, f, indent=4)
```

**SQLite version:**
```python
conn = get_connection()
conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
conn.commit()
conn.close()
```

**That's it.** No loading, no searching, no writing the whole file. One query.

### 3.7 SEARCH — `GET /items/search`

**JSON version:**
```python
items = load_items()
filtered = []
for item in items:
    if min_price is not None and item["price"] < min_price: continue
    if max_price is not None and item["price"] > max_price: continue
    filtered.append(item)
# then sort in Python, slice in Python, count in Python...
```

**SQLite version:**
```python
conditions = []
params = []
if min_price is not None:
    conditions.append("price >= ?")
    params.append(min_price)
if max_price is not None:
    conditions.append("price <= ?")
    params.append(max_price)

where = " AND ".join(conditions) if conditions else "1=1"

# Count
total_items = conn.execute(
    f"SELECT COUNT(*) FROM items WHERE {where}", params
).fetchone()[0]

# Paginated results
rows = conn.execute(
    f"SELECT * FROM items WHERE {where} {order} LIMIT ? OFFSET ?",
    params + [ITEMS_PER_PAGE, offset],
).fetchall()
```

**Key insight:** The `WHERE` clause is built dynamically. If only `min_price` is set,
the query becomes `WHERE price >= 10`. If both are set:
`WHERE price >= 10 AND price <= 100`. If neither: `WHERE 1=1` (always true).

**Try it:** After updating the routes, restart the server. Visit `/items/landing?sort=price` and see the table sorted by price. Add a new item — the ID is auto‑generated. Edit and delete items by ID; you'll notice that deleting an item never causes the wrong item to be edited.

**Checkpoint:** Every CRUD operation now runs directly on the database. The templates still receive the same variable names, so no template changes are needed.

---

## Step 4: Templates — What Changes?

**Goal:** Confirm that the front‑end stays exactly the same.  
**Mental model:** The database returns rows that we convert to dicts, which look identical to the JSON‑based dicts. The Jinja2 templates don't care where the data came from.

### Spoiler: Almost Nothing!

The templates receive the same variable names as before:

| Context Variable | JSON Version | SQLite Version |
|-----------------|--------------|----------------|
| `products` | List of dicts | List of dicts (from `dict_from_row()`) |
| `item.id` | Integer from JSON | Integer from `AUTOINCREMENT` |
| `item.name` | String | String |
| `item.price` | Float | Float |
| `item.is_offer` | Python `bool` | Python `bool` (converted from `int`) |

**One subtle change:** In the JSON version, `is_offer` was a Python `bool`. In SQLite,
it's stored as `INTEGER` (0 or 1). But `dict()` on a `sqlite3.Row` gives you `0` or `1`
as integers. In Python, `0` is falsy and `1` is truthy, so `{% if item.is_offer %}` in
Jinja2 works exactly the same.

**No template changes needed!** The templates from Workshops 1 and 2 work unchanged.

**Checkpoint:** You've replaced the entire data layer without touching a single HTML file. That's the power of separating data from presentation.

---

## Step 5: Complete the Conversion Checklist

**Goal:** Ensure every file has been migrated and the project structure is correct.

### ✅ All Changes at a Glance

| File | JSON Version | SQLite Version |
|------|-------------|----------------|
| `app/db.py` | ❌ Does not exist | **NEW** — connection, init, seed data |
| `app/main.py` | `load_items()` → Python stats | `SELECT COUNT/MIN/MAX/AVG/SUM` → SQL stats |
| `app/routes/items.py` | `load_items()` → list ops → `json.dump()` | `INSERT/SELECT/UPDATE/DELETE` → SQL |
| `items.json` | Data file | ❌ **Deleted** — replaced by `items.db` |
| `items.db` | ❌ Does not exist | **NEW** — auto‑created by `init_db()` |
| `app/templates/*.html` | Jinja2 templates | **Unchanged** — same variable names |

### ✅ Verify Your Project Structure

Your final `item_management_sqlite` folder should look like this:

```
item_management_sqlite/
├── app/
│   ├── __init__.py
│   ├── db.py                ← NEW: database module
│   ├── main.py              ← MODIFIED: SQL queries, init_db()
│   ├── models.py            ← unchanged
│   ├── routes/
│   │   ├── __init__.py
│   │   └── items.py         ← MODIFIED: SQL everywhere
│   ├── static/
│   │   ├── css/
│   │   │   ├── custom.css
│   │   │   └── fa.min.css
│   │   └── webfonts/
│   └── templates/
│       ├── base.html
│       ├── landing.html
│       ├── delete_confirm.html
│       ├── item_form.html
│       └── items/
│           └── items_landing.html
├── items.json               ← DELETED
└── items.db                 ← AUTO‑GENERATED on first run
```

**Checkpoint:** You've finished the migration. Time to test everything.

---

## Step 6: Run and Test

**Goal:** Confirm that every feature works identically to the JSON version, but now with a real database underneath.

### 6.1 Start the server

```bash
uvicorn app.main:app --reload
```

Watch the terminal output. On first run, `init_db()` will:
1. Create `items.db`
2. Create the `items` table
3. Insert 22 sample items

### 6.2 Test every operation

| Test | URL | What to check |
|------|-----|---------------|
| Dashboard | `http://localhost:8000/` | Stats load from SQLite |
| List items | `/items/landing` | Items shown, pagination works |
| Sort by name | `/items/landing?sort=name` | ORDER BY name |
| Sort by price | `/items/landing?sort=price` | ORDER BY price |
| Search by price | `/items/search?min_price=10&max_price=50` | WHERE price BETWEEN |
| Add item | `/items/add` → submit | INSERT works |
| Edit item | `/items/edit/1` → change name | UPDATE by id |
| Delete item | `/items/delete/1` → confirm | DELETE by id |
| Invalid page | `/items/landing?page=999` | Redirects to last page |
| Data persistence | Stop server, restart | Data still in `items.db` |

### 6.3 Peer into the database (bonus)

Run this in the terminal while the server is running:

```bash
sqlite3 items.db
```

Try these commands:
```sql
.tables
SELECT * FROM items;
SELECT COUNT(*) FROM items WHERE is_offer = 1;
SELECT name, price FROM items ORDER BY price DESC LIMIT 3;
.exit
```

This is the same SQL your Python code uses. You can inspect, debug, and even manually modify data without restarting the server.

**Checkpoint:** The app works exactly like before, but now it's backed by a concurrent, crash‑safe database. You've leveled up from file storage to real data management.

---

## Step 7: Commit Your Work

**Goal:** Save your progress with Git.

```bash
git init
git add -A
git commit -m "Step 3: Migrated from JSON to SQLite — full CRUD with SQL queries"
```

Add `items.db` to `.gitignore` (it's a binary file that gets regenerated):

```bash
echo "items.db" >> .gitignore
git add .gitignore
git commit -m "Add items.db to .gitignore"
```

---

## Reference: SQL ↔ JSON Cheat Sheet

Keep this table handy as you work:

| What You Want | JSON (Python) | SQLite (SQL) |
|---------------|---------------|--------------|
| **All items** | `load_items()` | `SELECT * FROM items` |
| **Count** | `len(items)` | `SELECT COUNT(*) FROM items` |
| **One item by ID** | `items[id]` (buggy index) | `SELECT * FROM items WHERE id = ?` |
| **Create item** | `items.append()` + `json.dump()` | `INSERT INTO items VALUES (?, ?, ...)` |
| **Update item** | `items[index] = new` + `json.dump()` | `UPDATE items SET ... WHERE id = ?` |
| **Delete item** | `items.pop(index)` + `json.dump()` | `DELETE FROM items WHERE id = ?` |
| **Sort ascending** | `sorted(items, key=...)` | `ORDER BY name ASC` |
| **Case‑insensitive sort** | `sorted(items, key=lambda x: x.lower())` | `ORDER BY name COLLATE NOCASE ASC` |
| **Filter by range** | `[i for i in items if min <= i["price"] <= max]` | `WHERE price BETWEEN ? AND ?` |
| **Paginate (page 2, 5 per page)** | `items[5:10]` | `LIMIT 5 OFFSET 5` |
| **Count after filter** | `len(filtered_list)` | `SELECT COUNT(*) FROM items WHERE ...` |
| **Min/Max/Avg** | `min()`, `max()`, `sum()/len()` | `SELECT MIN(), MAX(), AVG() FROM items` |
| **Auto‑increment ID** | `max(ids) + 1` (race condition!) | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| **Booleans** | `True` / `False` | `1` / `0` (INTEGER) |
| **Save** | `json.dump(items, f)` (writes entire file) | `COMMIT` (logs only the change) |
| **Concurrency** | ❌ Last‑write‑wins | ✅ WAL mode, row‑level locking |

**Try this yourself:** Pick any JSON operation from the left column and convert it to the SQL version using the cheat sheet. You'll quickly build intuition.

---

## Common Pitfalls

### 1. "I forgot to call `conn.commit()`"

This is the #1 SQLite mistake. Without `commit()`, your INSERT/UPDATE/DELETE runs in
a transaction that is **rolled back** when the connection closes.

```python
# ❌ Changes disappear!
conn.execute("INSERT INTO items ...")
conn.close()

# ✅ Changes persist
conn.execute("INSERT INTO items ...")
conn.commit()
conn.close()
```

### 2. "I forgot to close the connection"

SQLite has a limited number of concurrent connections (default 1024). In a dev server
this is rarely a problem, but it's good practice:

```python
conn = get_connection()
try:
    result = conn.execute(...)
finally:
    conn.close()
```

Or use Python's `contextlib`:
```python
from contextlib import closing

with closing(get_connection()) as conn:
    result = conn.execute(...)
```

### 3. "My `is_offer` values are `0` and `1`, not `True` and `False`"

This is normal. SQLite has no boolean type. The integer `0` is falsy and `1` is truthy
in both Python and Jinja2, so `{% if item.is_offer %}` works correctly.

### 4. "I deleted an item and now IDs have gaps"

This is **by design**. If your IDs are 1, 2, 3, 4, 5 and you delete item 3, you get
1, 2, 4, 5. SQLite will **never** reuse ID 3. This is correct behaviour — it prevents
confusion when someone has bookmarked `/items/edit/3`.

### 5. "My search stopped working"

Check dynamic WHERE clause building. Common mistakes:
- Forgetting `1=1` when no filters are active
- Using Python string formatting (`f"...{value}..."`) instead of `?` placeholders
- Not converting `None` checks correctly (`min_price is not None` vs `min_price`)

---

## What You Learned

After this workshop, you can:

| Skill | JSON Version | SQLite Version |
|-------|-------------|----------------|
| **Data storage** | File I/O with `json.load/dump` | SQL queries with `sqlite3` |
| **ID management** | Manual via `max(ids) + 1` | Auto via `AUTOINCREMENT` |
| **Sorting** | Python `sorted()` with lambdas | SQL `ORDER BY` with `COLLATE NOCASE` |
| **Filtering** | Python list comprehensions | SQL `WHERE` clauses |
| **Pagination** | Python list slicing `[start:end]` | SQL `LIMIT/OFFSET` |
| **Aggregation** | `min()`, `max()`, `sum()`, `len()` | SQL `MIN()`, `MAX()`, `AVG()`, `SUM()`, `COUNT()` |
| **Concurrency** | ❌ Unsafe (last‑write‑wins) | ✅ Safe (WAL mode, transactions) |
| **Data integrity** | ❌ No constraints | ✅ NOT NULL, types, PRIMARY KEY |
| **Portability** | JSON file | Single `.db` file, zero config |

And most importantly, you now understand **why databases exist** — they handle the hard
parts (concurrency, integrity, querying) so you don't have to.

---

## Next Steps

After mastering SQLite, you can:

1. **Add a `categories` table** with a foreign key from items → categories
2. **Use SQLAlchemy** — an ORM that generates SQL for you
3. **Switch to PostgreSQL** — same SQL, different connection string
4. **Add indexes** — make searches faster on large datasets
5. **Use migrations** — Alembic for schema changes over time
6. **Deploy** — SQLite works on Railway, Fly.io, etc.

Every database you ever use (PostgreSQL, MySQL, MariaDB, Oracle, SQL Server) speaks
the same SQL you just learned. The only thing that changes is the connection string.

---

You've done much more than swap a file format. You've adopted the database mindset: **the database is your partner, not just a storage bucket**. From here on, every query you write, every table you design, will be driven by the question "What can the database do for me?" That's the foundation of every real‑world application.