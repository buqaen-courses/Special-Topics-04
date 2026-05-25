# Step‑by‑Step Workshop: Build a CRUD App with FastAPI + Pure HTML/CSS

**Goal:** Create a complete item management web application **from scratch**, learning one piece at a time.  
**No Bootstrap, no JavaScript** – only FastAPI, HTML forms, Jinja2 templates, and a minimal custom CSS with FontAwesome icons.

Each step adds a new feature. After each step you will **test** the feature in the browser.  
By the end you will understand:

- How to serve HTML pages with FastAPI
- How to read and write a JSON file as a database
- How to use Jinja2 templates (loops, conditions, inheritance)
- How to handle GET and POST requests
- What are path parameters and query parameters
- The Post/Redirect/Get pattern
- Basic HTTP status codes (200, 303, 404)

---

## Before You Start – Setup

Create a new folder for the project, then inside it:

```bash
mkdir my_crud_app
cd my_crud_app
```

Create the following subdirectories:

```bash
mkdir app
mkdir app/static
mkdir app/static/css
mkdir app/templates
mkdir app/routes
```

Install the required packages:

```bash
pip install fastapi uvicorn jinja2
```

We will create the files one by one. Let's begin!

---

## Step 0 – Project Skeleton and Initial Files

We need a few files that won't change much. Create them now.

### `app/__init__.py`
Empty file, marks `app` as a Python package.

```python
# This file can be empty
```

### `app/routes/__init__.py`
Empty file.

```python
# This file can be empty
```

### `app/models.py`
We define a Pydantic model for an Item. We'll use it later for validation.

```python
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False
    tax: Optional[float] = None
```

### `items.json` (sample data)
Create this file in the project root (same level as `app` folder). We put a few items so the landing page is not empty.

```json
[
  {
    "name": "Laptop",
    "price": 999.99,
    "is_offer": false,
    "tax": 99.999
  },
  {
    "name": "Smartphone",
    "price": 499.50,
    "is_offer": true,
    "tax": 49.95
  },
  {
    "name": "Headphones",
    "price": 79.99,
    "is_offer": false,
    "tax": 7.999
  }
]
```

---

## Step 1 – Minimal Custom CSS (with comments)

Create `app/static/css/custom.css`. This CSS will style everything without any framework.

```css
/* ============================================================
   custom.css – Minimal styling for our CRUD app
   No frameworks, only essential rules.
   ============================================================ */

/* ---------- RESET & GLOBAL ---------- */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Roboto, system-ui, sans-serif;
    background: #f0f4f8;
    color: #1e2a3e;
    line-height: 1.5;
}

.container {
    max-width: 1300px;
    margin: 0 auto;
    padding: 0 20px;
}

/* ---------- NAVIGATION BAR ---------- */
.navbar {
    background: #0b3b5f;
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}
.navbar-brand {
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
    color: white;
}
.navbar-nav {
    display: flex;
    gap: 1.5rem;
    list-style: none;
}
.navbar-nav a {
    color: #e0f2fe;
    text-decoration: none;
    font-weight: 500;
}
.navbar-nav a:hover {
    color: white;
    text-decoration: underline;
}

/* ---------- CARD COMPONENT ---------- */
.card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
    overflow: hidden;
}
.card-header {
    background: #2c7da0;
    color: white;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    font-size: 1.2rem;
}
.card-body {
    padding: 1.5rem;
}

/* ---------- FORM STYLES ---------- */
.form-group {
    margin-bottom: 1.2rem;
}
label {
    display: block;
    margin-bottom: 0.4rem;
    font-weight: 600;
    color: #0b3b5f;
}
input, select {
    width: 100%;
    padding: 0.6rem 0.8rem;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 1rem;
}
input:focus {
    outline: none;
    border-color: #2c7da0;
    box-shadow: 0 0 0 3px rgba(44,125,160,0.2);
}
.checkbox-group {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.checkbox-group input {
    width: auto;
}

/* ---------- BUTTONS ---------- */
.btn {
    display: inline-block;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    border: none;
    cursor: pointer;
    font-size: 0.95rem;
    transition: background 0.2s;
}
.btn-primary {
    background: #2c7da0;
    color: white;
}
.btn-primary:hover {
    background: #1f5e7a;
}
.btn-danger {
    background: #d62828;
    color: white;
}
.btn-danger:hover {
    background: #a81c1c;
}
.btn-warning {
    background: #e9c46a;
    color: #2d2d2d;
}
.btn-warning:hover {
    background: #d4a832;
}
.btn-secondary {
    background: #8d99ae;
    color: white;
}
.btn-secondary:hover {
    background: #6c757d;
}
.btn-sm {
    padding: 0.3rem 0.8rem;
    font-size: 0.85rem;
}

/* ---------- TABLE STYLES ---------- */
.table {
    width: 100%;
    border-collapse: collapse;
}
.table th, .table td {
    border-bottom: 1px solid #e2e8f0;
    padding: 0.75rem;
    text-align: left;
}
.table th {
    background: #f1f5f9;
    font-weight: 700;
}
.table tr:hover {
    background: #f8fafc;
}
.badge {
    background: #2c7da0;
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.8rem;
}
.badge-secondary {
    background: #94a3b8;
}

/* ---------- UTILITIES ---------- */
.text-center { text-align: center; }
.mt-3 { margin-top: 1rem; }
.mb-4 { margin-bottom: 1.5rem; }
.gap-2 { gap: 0.5rem; }
.d-flex { display: flex; }
.justify-between { justify-content: space-between; }
```

---

## Step 2 – Base Template (Jinja2)

Create `app/templates/base.html`. This is the skeleton that all pages will extend.

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Items CRUD{% endblock %}</title>
    <!-- FontAwesome CDN (free icons) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Our custom CSS -->
    <link rel="stylesheet" href="/static/css/custom.css">
</head>
<body>

<nav class="navbar">
    <div class="container">
        <a href="/items/landing" class="navbar-brand">
            <i class="fas fa-boxes"></i> Items Manager
        </a>
        <ul class="navbar-nav">
            <li><a href="/items/landing"><i class="fas fa-table-list"></i> Items</a></li>
            <li><a href="/items/add"><i class="fas fa-plus-circle"></i> Add Item</a></li>
        </ul>
    </div>
</nav>

<main class="container" style="margin-top: 2rem;">
    {% block content %}
    <!-- Child templates will insert their content here -->
    {% endblock %}
</main>

<footer style="text-align: center; margin: 3rem 0 1rem; color: #5c6b7a;">
    <hr>
    <small>© 2026 — CRUD Workshop | Pure HTML/CSS + FastAPI</small>
</footer>

</body>
</html>
```

---

## Step 3 – Landing Page (Show All Items)

**What we learn:**  
- A `GET` request to show data.  
- Jinja2 loop (`{% for %}`) to display a list.  
- How to serve a template with context.

### 3.1 Backend: add the route to show the landing page

Create `app/routes/items.py` – we will add routes step by step. Initially only the landing page.

```python
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
DATA_FILE = "items.json"

def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

@router.get("/landing", response_class=HTMLResponse)
async def landing_page(request: Request):
    items = load_items()
    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={"items": items}
    )
```

### 3.2 Frontend: create `landing.html`

Create `app/templates/landing.html`. This template extends `base.html` and shows the items in a table.

```html
{% extends "base.html" %}

{% block title %}All Items{% endblock %}

{% block content %}
<h2><i class="fas fa-cubes"></i> Items Management</h2>

<!-- ADD BUTTON -->
<div style="margin: 1.5rem 0;">
    <a href="/items/add" class="btn btn-primary">
        <i class="fas fa-plus"></i> Add New Item
    </a>
</div>

<!-- ITEMS TABLE -->
<div class="card">
    <div class="card-header">
        <i class="fas fa-table"></i> Current items
    </div>
    <div class="card-body" style="padding: 0;">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Offer</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% if items and items|length > 0 %}
                    {% for item in items %}
                    <tr>
                        <td>{{ loop.index0 }}</td>
                        <td>{{ item.name }}</td>
                        <td>${{ "%.2f"|format(item.price) }}</td>
                        <td>
                            {% if item.is_offer %}
                                <span class="badge">Yes</span>
                            {% else %}
                                <span class="badge badge-secondary">No</span>
                            {% endif %}
                        </td>
                        <td>
                            <a href="/items/edit/{{ loop.index0 }}" class="btn btn-warning btn-sm">
                                <i class="fas fa-edit"></i>
                            </a>
                            <a href="/items/delete/{{ loop.index0 }}" class="btn btn-danger btn-sm">
                                <i class="fas fa-trash-alt"></i>
                            </a>
                        </td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr><td colspan="5" class="text-center">No items found. Add one!</td></tr>
                {% endif %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

### 3.3 Main FastAPI app

Create `app/main.py` to mount static files and include the router.

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import items

app = FastAPI(title="Items CRUD - Step by Step")

# Serve static files (CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include the items router (all routes under /items)
app.include_router(items.router, prefix="/items")

@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/items/landing")
```

### 3.4 Test Step 3

Run the server:

```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000`. You should see the landing page with the three sample items. The table shows ID, Name, Price, Offer status, and action buttons (Edit/Delete). The buttons don’t work yet – we will add those routes in the next steps.

**Concepts checked:**  
- `GET /items/landing` → returns HTML (status 200).  
- Jinja2 renders the table using a `for` loop.  
- `{{ loop.index0 }}` gives the zero‑based index (used as item ID).

---

## Step 4 – Add New Item (HTML Form + POST)

**What we learn:**  
- HTML form with `method="post"`.  
- Reading form data with `Form(...)` in FastAPI.  
- Redirect after POST (status code 303).  
- Saving data to JSON file.

### 4.1 Add the route to show the “Add Item” form

Add this function to `app/routes/items.py` (put it after the `load_items` function).

```python
@router.get("/add", response_class=HTMLResponse)
async def add_item_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="item_form.html",
        context={"editing": False, "item": None, "item_id": None}
    )
```

### 4.2 Add the route to process the form submission (create item)

Add this function to `app/routes/items.py`.

```python
from fastapi import Form, status
from fastapi.responses import RedirectResponse

@router.post("/")
async def create_item(
    name: str = Form(...),
    price: float = Form(...),
    is_offer: bool = Form(False)
):
    items = load_items()
    new_item = {
        "name": name,
        "price": price,
        "is_offer": is_offer,
        "tax": price * 0.1
    }
    items.append(new_item)
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)
    return RedirectResponse("/items/landing", status_code=status.HTTP_303_SEE_OTHER)
```

### 4.3 Create the template `item_form.html`

This template will be used for both **add** and **edit**. For now we only use it for add.

Create `app/templates/item_form.html`:

```html
{% extends "base.html" %}

{% block title %}{{ 'Edit' if editing else 'Add' }} Item{% endblock %}

{% block content %}
<div class="card" style="max-width: 600px; margin: 0 auto;">
    <div class="card-header">
        <i class="fas {{ 'fa-pen' if editing else 'fa-plus' }}"></i>
        {{ 'Edit Item' if editing else 'Create New Item' }}
    </div>
    <div class="card-body">
        <form method="post" action="{% if editing %}/items/{{ item_id }}{% else %}/items/{% endif %}">
            <div class="form-group">
                <label><i class="fas fa-tag"></i> Name</label>
                <input type="text" name="name" required
                       value="{{ item.name if editing else '' }}">
            </div>
            <div class="form-group">
                <label><i class="fas fa-dollar-sign"></i> Price</label>
                <input type="number" name="price" step="0.01" required
                       value="{{ item.price if editing else '' }}">
            </div>
            <div class="form-group checkbox-group">
                <input type="checkbox" name="is_offer" id="offer"
                       {% if editing and item.is_offer %}checked{% endif %}>
                <label for="offer" style="margin:0;">This item is on offer</label>
            </div>

            {% if editing and item.tax is defined %}
                <div style="background:#e6f4ea; padding:0.6rem; border-radius:8px; margin-bottom:1rem;">
                    <i class="fas fa-calculator"></i> Auto-calculated tax: ${{ "%.2f"|format(item.tax) }}
                </div>
            {% endif %}

            <div class="d-flex gap-2" style="margin-top: 1.5rem;">
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-save"></i> {{ 'Update' if editing else 'Create' }}
                </button>
                <a href="/items/landing" class="btn btn-secondary">Cancel</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

### 4.4 Test Step 4

- Click “Add New Item” on the landing page. You should see the form.
- Fill in: Name = “Tablet”, Price = 299.99, check “offer” checkbox.
- Submit the form.
- You are redirected to the landing page and the new item appears in the table.

**Check your `items.json`** – it should now contain 4 items.

---

## Step 5 – Edit Item (Pre‑filled Form + Update)

**What we learn:**  
- Path parameters (`{item_id}`).  
- Pre‑populating an HTML form.  
- Handling POST to update an existing item.

### 5.1 Add the route to show the edit form (GET)

Add to `app/routes/items.py`:

```python
from fastapi import HTTPException

@router.get("/edit/{item_id}", response_class=HTMLResponse)
async def edit_item_form(request: Request, item_id: int):
    items = load_items()
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse(
        request=request,
        name="item_form.html",
        context={"editing": True, "item": items[item_id], "item_id": item_id}
    )
```

### 5.2 Add the route to update the item (POST)

Add to `app/routes/items.py`:

```python
@router.post("/{item_id}")
async def update_item(
    item_id: int,
    name: str = Form(...),
    price: float = Form(...),
    is_offer: bool = Form(False)
):
    items = load_items()
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = {
        "name": name,
        "price": price,
        "is_offer": is_offer,
        "tax": price * 0.1
    }
    items[item_id] = updated_item
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)
    return RedirectResponse("/items/landing", status_code=status.HTTP_303_SEE_OTHER)
```

### 5.3 Test Step 5

- On the landing page, click the **Edit** button (yellow pencil) for any item.
- You should see the form pre‑filled with that item’s data.
- Change the name or price, then submit.
- The landing page updates with the changed data.

---

## Step 6 – Delete Item (Confirmation Page + POST)

**What we learn:**  
- Using a confirmation page to prevent accidental deletion.  
- A `GET` to show confirmation, then a `POST` to perform the deletion.  
- Removing an item from the list by index.

### 6.1 Add route to show confirmation page (GET)

Add to `app/routes/items.py`:

```python
@router.get("/delete/{item_id}", response_class=HTMLResponse)
async def confirm_delete(request: Request, item_id: int):
    items = load_items()
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse(
        request=request,
        name="delete_confirm.html",
        context={"item": items[item_id], "item_id": item_id}
    )
```

### 6.2 Add route to actually delete (POST)

Add to `app/routes/items.py`:

```python
@router.post("/delete/{item_id}")
async def delete_item(item_id: int):
    items = load_items()
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    items.pop(item_id)
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)
    return RedirectResponse("/items/landing", status_code=status.HTTP_303_SEE_OTHER)
```

### 6.3 Create the `delete_confirm.html` template

Create `app/templates/delete_confirm.html`:

```html
{% extends "base.html" %}

{% block title %}Confirm Deletion{% endblock %}

{% block content %}
<div class="card" style="max-width: 500px; margin: 2rem auto; text-align: center;">
    <div class="card-header" style="background: #d62828;">
        <i class="fas fa-exclamation-triangle"></i> Confirm Delete
    </div>
    <div class="card-body">
        {% if item %}
            <p>Are you sure you want to delete <strong>"{{ item.name }}"</strong>?</p>
            <p>Price: ${{ "%.2f"|format(item.price) }}</p>
            <form method="post" action="/items/delete/{{ item_id }}">
                <button type="submit" class="btn btn-danger">
                    <i class="fas fa-trash-alt"></i> Yes, delete
                </button>
                <a href="/items/landing" class="btn btn-secondary">Cancel</a>
            </form>
        {% else %}
            <p>Item not found.</p>
            <a href="/items/landing" class="btn btn-primary">Back to list</a>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### 6.4 Test Step 6

- Click the **Delete** button (red trash can) for any item.
- You see a confirmation page asking “Are you sure?”
- Click “Yes, delete”. The item disappears from the landing page.

---

## Step 7 – Search / Filter by Price (Query Parameters)

**What we learn:**  
- Query parameters (`?min_price=10&max_price=50`).  
- Filtering a list in Python.  
- Keeping filter values in the input fields after submit.

### 7.1 Add the search route to `app/routes/items.py`

Add this function **before** the landing page route, or reorder as you like. The route is `/items/search`.

```python
@router.get("/search")
async def search_items(
    request: Request,
    min_price: float = None,
    max_price: float = None
):
    items = load_items()
    filtered = []
    for item in items:
        price = item["price"]
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue
        filtered.append(item)
    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={
            "items": filtered,
            "min_price": min_price,
            "max_price": max_price
        }
    )
```

### 7.2 Update `landing.html` – add the filter form

Replace the content of `landing.html` with the following (adds a filter card above the table):

```html
{% extends "base.html" %}

{% block title %}All Items{% endblock %}

{% block content %}
<h2><i class="fas fa-cubes"></i> Items Management</h2>

<!-- FILTER CARD -->
<div class="card">
    <div class="card-header">
        <i class="fas fa-filter"></i> Filter by price
    </div>
    <div class="card-body">
        <form method="GET" action="/items/search">
            <div class="d-flex gap-2" style="flex-wrap: wrap;">
                <div style="flex: 1;">
                    <label>Min price ($)</label>
                    <input type="number" name="min_price" step="0.01"
                           value="{{ min_price if min_price is defined else '' }}">
                </div>
                <div style="flex: 1;">
                    <label>Max price ($)</label>
                    <input type="number" name="max_price" step="0.01"
                           value="{{ max_price if max_price is defined else '' }}">
                </div>
                <div style="align-self: flex-end;">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-search"></i> Search
                    </button>
                    <a href="/items/landing" class="btn btn-secondary">
                        <i class="fas fa-undo-alt"></i> Reset
                    </a>
                </div>
            </div>
        </form>
    </div>
</div>

<!-- ADD BUTTON -->
<div style="margin: 1.5rem 0;">
    <a href="/items/add" class="btn btn-primary">
        <i class="fas fa-plus"></i> Add New Item
    </a>
</div>

<!-- ITEMS TABLE (same as before) -->
<div class="card">
    <div class="card-header">
        <i class="fas fa-table"></i> Current items
    </div>
    <div class="card-body" style="padding: 0;">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Offer</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% if items and items|length > 0 %}
                    {% for item in items %}
                    <tr>
                        <td>{{ loop.index0 }}</td>
                        <td>{{ item.name }}</td>
                        <td>${{ "%.2f"|format(item.price) }}</td>
                        <td>
                            {% if item.is_offer %}
                                <span class="badge">Yes</span>
                            {% else %}
                                <span class="badge badge-secondary">No</span>
                            {% endif %}
                        </td>
                        <td>
                            <a href="/items/edit/{{ loop.index0 }}" class="btn btn-warning btn-sm">
                                <i class="fas fa-edit"></i>
                            </a>
                            <a href="/items/delete/{{ loop.index0 }}" class="btn btn-danger btn-sm">
                                <i class="fas fa-trash-alt"></i>
                            </a>
                        </td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr><td colspan="5" class="text-center">No items found. Add one!</td></tr>
                {% endif %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

### 7.3 Test Step 7

- On the landing page, enter min price = 100, max price = 600.
- Click Search → only items with price between 100 and 600 appear (e.g., Laptop 999.99? That's above 600, so it might be excluded; adjust values to see filtering).
- Use the Reset button to go back to the full list.

**Note:** The filter works with the original `items.json` data. You can add more items to test different ranges.

---

## Step 8 – Final Review and Bonus (JSON API)

You now have a complete CRUD application with:

- **Create** (POST `/items/`)
- **Read** (GET `/items/landing` and `/items/search`)
- **Update** (POST `/items/{item_id}`)
- **Delete** (POST `/items/delete/{item_id}`)

### Bonus: Add JSON API endpoints (optional)

If you want to also offer a REST API, add these routes to `app/routes/items.py`. They use the same `load_items` / `save_items` functions.

```python
from app.models import Item

api_router = APIRouter(prefix="/api/items", tags=["api"])

@api_router.get("/")
async def api_read_items():
    items = load_items()
    return {"items": items, "count": len(items)}

@api_router.post("/")
async def api_create_item(item: Item):
    items = load_items()
    item.tax = item.price * 0.1
    items.append(item.model_dump())
    save_items(items)
    return {"message": "Item created", "item": item}

@api_router.put("/{item_id}")
async def api_update_item(item_id: int, item: Item):
    items = load_items()
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    item.tax = item.price * 0.1
    items[item_id] = item.model_dump()
    save_items(items)
    return {"message": "Item updated", "item": item}

@api_router.delete("/{item_id}")
async def api_delete_item(item_id: int):
    items = load_items()
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    deleted = items.pop(item_id)
    save_items(items)
    return {"message": "Item deleted", "deleted": deleted}
```

Then in `app/main.py`, include this router as well:

```python
app.include_router(items.api_router)
```

Now you can test with `curl` or a tool like Postman.

---

## Summary of HTTP Concepts Learned

| Concept | Example in our app |
|---------|--------------------|
| **GET** | Loading `/items/landing`, the search form. |
| **POST** | Creating, updating, and deleting items. |
| **Path parameter** | `/items/edit/1` – the `1` is the item ID. |
| **Query parameter** | `/items/search?min_price=10` |
| **Status 200** | Page loads successfully. |
| **Status 303** | Redirect after POST (e.g., after create/update/delete). |
| **Status 404** | Trying to edit a non‑existent item. |
| **HTML forms** | `method="post"`, `action="/items/"` |
| **Jinja2** | Loops (`for`), conditions (`if`), filters (`|format`), inheritance (`extends`). |

---

## Final Project Structure

```
my_crud_app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── items.py
│   ├── static/
│   │   └── css/
│   │       └── custom.css
│   └── templates/
│       ├── base.html
│       ├── landing.html
│       ├── item_form.html
│       └── delete_confirm.html
├── items.json
└── pyproject.toml (optional)
```

---

## What’s Next?

- Add more fields (e.g., `description`, `stock`).  
- Sort the table by clicking on column headers (would require JavaScript, but you can also make it a server‑side sort with query params).  
- Replace the JSON file with a real database (SQLite, PostgreSQL).  
- Add user authentication.

You have built a solid foundation. Congratulations!