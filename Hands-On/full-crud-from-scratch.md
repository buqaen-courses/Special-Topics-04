# Building a CRUD Web Application from Scratch with FastAPI
## A Step-by-Step Tutorial (No JavaScript, Pure HTML/CSS + Jinja2)

---

## Part 0: Understanding the API Design (MUST READ FIRST!)

**⚠️ CRITICAL: Read this entire section before writing any code!**

Most beginners fail at CRUD applications because they start coding without understanding the complete architecture. This section teaches you to think like a backend developer: design first, code second.

### What You'll Learn in This Section:
1. What endpoints your API needs
2. What HTML pages you need to create
3. How forms connect to API endpoints
4. How to avoid the most common bugs

---

### Table 1: Complete API Endpoint Design

This table shows **every route** your FastAPI application must handle. Study it carefully.

| Method | Path | Purpose | Request Data | Response | Notes |
|--------|------|---------|--------------|----------|-------|
| GET | `/` | Landing page | None | HTML: landing.html | Entry point of app |
| GET | `/items/` | List all items | None | HTML: items_list.html | Shows all items from database |
| GET | `/items/new` | Show create form | None | HTML: item_form.html (editing=False) | Empty form for new item |
| POST | `/items/` | Create new item | Form: name, price, is_offer | Redirect to `/items/` | Processes form submission |
| GET | `/items/edit/{item_id}` | Show edit form | URL param: item_id | HTML: item_form.html (editing=True) | Pre-filled form with existing data |
| POST | `/items/{item_id}` | Update existing item | URL param: item_id<br>Form: name, price, is_offer | Redirect to `/items/` | **Different path than GET edit!** |
| POST | `/items/delete/{item_id}` | Delete item | URL param: item_id | Redirect to `/items/` | POST for safety (not GET) |

**🔑 Key Insights:**

1. **Creating an item requires TWO routes:**
   - `GET /items/new` → Shows empty form
   - `POST /items/` → Receives form data and creates item

2. **Editing an item requires TWO routes with DIFFERENT paths:**
   - `GET /items/edit/{item_id}` → Shows pre-filled form
   - `POST /items/{item_id}` → Receives form data and updates item
   - ⚠️ **Common mistake:** Students often POST to `/items/edit/{item_id}` (wrong!)

3. **Why different paths for edit?**
   - `GET /items/edit/5` is a "UI route" (shows the edit page)
   - `POST /items/5` is a "resource route" (modifies item #5)
   - This follows RESTful conventions where `/items/5` represents the item resource

4. **Delete uses POST, not GET:**
   - GET requests should never modify data (security principle)
   - HTML forms only support GET and POST (not DELETE method)

---

### Table 2: HTML Pages and Their Requirements

This table shows what **each HTML template** needs to work correctly.

| Page File | Served at URL(s) | Variables Passed from FastAPI | Forms on Page | Links on Page |
|-----------|------------------|-------------------------------|---------------|---------------|
| **landing.html** | `/` | • `request` (required by Jinja2) | None | • `<a href="/items/">` to view items |
| **items_list.html** | `/items/` | • `request`<br>• `items` (list of dicts) | **Delete form** (one per item):<br>• `action="/items/delete/{{ item.id }}"`<br>• `method="post"`<br>• Submit button | • `<a href="/items/new">` to create<br>• `<a href="/items/edit/{{ item.id }}">` per item to edit |
| **item_form.html** | `/items/new`<br>`/items/edit/{item_id}` | • `request`<br>• `editing` (bool)<br>**If editing=True:**<br>• `item_id` (int)<br>• `name` (str)<br>• `price` (float)<br>• `is_offer` (bool) | **One form** with dynamic action:<br>• `action="{% if editing %}/items/{{ item_id }}{% else %}/items/{% endif %}"`<br>• `method="post"`<br>• Fields: name, price, is_offer<br>• Submit button | • `<a href="/items/">` to cancel |

**🔑 Key Insights:**

1. **item_form.html is reused for both create and edit:**
   - When `editing=False`: form is empty, POSTs to `/items/`
   - When `editing=True`: form is pre-filled, POSTs to `/items/{item_id}`
   - The form's `action` URL changes based on the `editing` variable

2. **Critical: Form action ≠ Page URL**
   - When you visit `GET /items/edit/5`, you see the edit form
   - But that form POSTs to `/items/5` (not `/items/edit/5`)
   - The page URL and form action are **different**!

3. **Delete button is actually a form:**
   - Can't use `<a href="/items/delete/5">` (that's a GET request)
   - Must use `<form action="/items/delete/5" method="post">`
   - This prevents accidental deletion from web crawlers

---

### Table 3: Form-to-Endpoint Mapping (The Most Important Table!)

This table shows **where each form sends its data**. This is where most bugs happen!

| Form Location (Page URL) | Form Action (Where Data Goes) | HTTP Method | Form Fields | What Happens After Submit |
|---------------------------|--------------------------------|-------------|-------------|---------------------------|
| `/items/new` | `/items/` | POST | name, price, is_offer | Creates new item → Redirects to `/items/` |
| `/items/edit/5` | `/items/5` | POST | name, price, is_offer | Updates item #5 → Redirects to `/items/` |
| `/items/` (delete button) | `/items/delete/5` | POST | (none, just item_id in URL) | Deletes item #5 → Redirects to `/items/` |

**🔑 The Golden Rule:**

> **The URL you see in your browser (page URL) is NOT always the same as the URL where the form sends data (form action)!**

**Example:**
- You visit: `http://localhost:8000/items/edit/5`
- The form on that page has: `<form action="/items/5" method="post">`
- When you click submit, data goes to: `http://localhost:8000/items/5`

This is **by design** and follows REST principles!

---

### Table 4: Data Flow for Each Operation

This table shows the **complete journey** of each CRUD operation.

| Operation | Step 1: User Action | Step 2: Browser Request | Step 3: FastAPI Route | Step 4: FastAPI Response | Step 5: Browser Action |
|-----------|---------------------|-------------------------|------------------------|--------------------------|------------------------|
| **View List** | Clicks "View Items" link | `GET /items/` | `@router.get("/")` loads items from JSON | Returns `items_list.html` with items data | Displays list page |
| **Create - Show Form** | Clicks "Add New Item" | `GET /items/new` | `@router.get("/new")` | Returns `item_form.html` with `editing=False` | Displays empty form |
| **Create - Submit** | Fills form, clicks "Create" | `POST /items/`<br>Body: name, price, is_offer | `@router.post("/")` creates item, saves to JSON | Returns redirect to `/items/` | Browser requests `GET /items/` |
| **Edit - Show Form** | Clicks "Edit" on item #5 | `GET /items/edit/5` | `@router.get("/edit/{item_id}")` loads item #5 | Returns `item_form.html` with `editing=True` and item data | Displays pre-filled form |
| **Edit - Submit** | Changes form, clicks "Update" | `POST /items/5`<br>Body: name, price, is_offer | `@router.post("/{item_id}")` updates item #5, saves to JSON | Returns redirect to `/items/` | Browser requests `GET /items/` |
| **Delete** | Clicks "Delete" on item #5 | `POST /items/delete/5` | `@router.post("/delete/{item_id}")` removes item #5, saves to JSON | Returns redirect to `/items/` | Browser requests `GET /items/` |

**🔑 Key Insights:**

1. **Every form submission ends with a redirect:**
   - Never return HTML directly after POST
   - Always redirect to prevent duplicate submissions (if user refreshes)
   - This is called the "Post/Redirect/Get" (PRG) pattern

2. **GET requests show pages, POST requests modify data:**
   - GET: Safe, can be bookmarked, can be refreshed
   - POST: Modifies data, should redirect after success

3. **The browser makes TWO requests for create/edit/delete:**
   - First: POST with form data
   - Second: GET to the redirected URL (to show updated list)

---

### Table 5: Variable Requirements for Each Template

This table shows **exactly what data** each template expects from FastAPI.

| Template | Required Variables | Optional Variables | Variable Types | Example Values |
|----------|-------------------|-------------------|----------------|----------------|
| **landing.html** | • `request` | None | • `request`: Request object | N/A |
| **items_list.html** | • `request`<br>• `items` | None | • `request`: Request object<br>• `items`: list[dict] | `items = [{"id": 0, "name": "Laptop", "price": 999.99, "is_offer": False}]` |
| **item_form.html** (create mode) | • `request`<br>• `editing` | None | • `request`: Request object<br>• `editing`: bool | `editing = False` |
| **item_form.html** (edit mode) | • `request`<br>• `editing`<br>• `item_id`<br>• `name`<br>• `price`<br>• `is_offer` | None | • `request`: Request object<br>• `editing`: bool<br>• `item_id`: int<br>• `name`: str<br>• `price`: float<br>• `is_offer`: bool | `editing = True`<br>`item_id = 5`<br>`name = "Laptop"`<br>`price = 999.99`<br>`is_offer = False` |

**🔑 Key Insights:**

1. **`request` is always required:**
   - Jinja2 needs it for context
   - Always pass it: `{"request": request, ...}`

2. **item_form.html has two modes:**
   - Create mode: Only needs `editing=False`
   - Edit mode: Needs `editing=True` plus all item data

3. **Variable names must match exactly:**
   - If template uses `{{ items }}`, FastAPI must pass `items`
   - If template uses `{{ item_id }}`, FastAPI must pass `item_id`

---

### Table 6: Common Bugs and How to Avoid Them

| Bug | Symptom | Cause | Solution | Prevention |
|-----|---------|-------|----------|------------|
| **405 Method Not Allowed** | Clicking "Update" gives 405 error | Form POSTs to `/items/edit/5` but no route exists | Change form action to `/items/{{ item_id }}` | Always check Table 3 for correct form actions |
| **422 Unprocessable Entity** | Form submission fails with 422 | Missing `python-multipart` package | Run `pip install python-multipart` | Install all dependencies before coding |
| **Checkbox always False** | `is_offer` never becomes True | HTML checkboxes don't send data when unchecked | Use `is_offer: bool = Form(False)` as default | Always provide defaults for optional form fields |
| **Template not found** | `TemplateNotFound: item_form.html` | Wrong templates directory path | Check `Jinja2Templates(directory="app/templates")` | Verify directory structure matches code |
| **Static files 404** | CSS doesn't load | Static files not mounted | Add `app.mount("/static", StaticFiles(...))` | Mount static files before defining routes |
| **Data not saving** | Changes disappear after restart | Not calling `save_items()` | Call `save_items(items)` after modifications | Always save after create/update/delete |
| **Wrong item edited** | Editing item #5 changes item #3 | Using list index instead of item ID | Use `item["id"]` not list position | Always identify items by ID, not index |

---

### Quiz: Test Your Understanding

Before moving to Part 1, answer these questions:

1. **Q:** If you visit `/items/edit/7`, where does the form send its data?
   **A:** To `/items/7` (not `/items/edit/7`)

2. **Q:** How many routes are needed to create a new item?
   **A:** Two routes: `GET /items/new` (show form) and `POST /items/` (process form)

3. **Q:** Why do we use POST for delete instead of a simple link?
   **A:** GET requests should never modify data (security principle)

4. **Q:** What variables must you pass to `item_form.html` when editing item #5?
   **A:** `request`, `editing=True`, `item_id=5`, `name`, `price`, `is_offer`

5. **Q:** After successfully creating an item, should you return HTML or redirect?
   **A:** Redirect to `/items/` (Post/Redirect/Get pattern)

If you can answer all these correctly, you're ready to start coding!

---

## Part 1: Project Setup

### Step 1.1: Create Project Structure
```bash
mkdir my_crud_app
cd my_crud_app
mkdir -p app/templates app/static/css app/data
touch app/__init__.py app/main.py app/items.py app/data/items.json
```
**What each directory does:**
- `app/`: Main application package
- `app/templates/`: HTML templates (Jinja2)
- `app/static/css/`: CSS stylesheets
- `app/data/`: JSON file for data storage

### Step 1.2: Install Dependencies

```bash
pip install fastapi uvicorn jinja2 python-multipart
```
**Why these packages?**
- `fastapi`: Web framework
- `uvicorn`: ASGI server to run FastAPI
- `jinja2`: Template engine for HTML
- `python-multipart`: Required for form data parsing (prevents 422 errors)

---

## Part 2: Basic FastAPI Setup

### Step 2.1: Create Main Application (`app/main.py`)

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.items import router as items_router

app = FastAPI()

# Mount static files (CSS, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include items router
app.include_router(items_router)

@app.get("/")
async def landing(request: Request):
return templates.TemplateResponse("landing.html", {"request": request})
```
**Code explanation:**
- `app.mount("/static", ...)`: Makes `/static/css/style.css` accessible
- `templates = Jinja2Templates(...)`: Tells FastAPI where HTML files are
- `app.include_router(items_router)`: Adds all `/items/*` routes
- `@app.get("/")`: Handles the landing page (see Table 1)

### Step 2.2: Initialize Data File (`app/data/items.json`)

```json
[
  {"id": 0, "name": "Laptop", "price": 999.99, "is_offer": false},
  {"id": 1, "name": "Mouse", "price": 25.50, "is_offer": true},
  {"id": 2, "name": "Keyboard", "price": 75.00, "is_offer": false}
]
```
**Data structure:**
- Each item is a dictionary with 4 fields
- `id`: Unique identifier (integer)
- `name`: Item name (string)
- `price`: Item price (float)
- `is_offer`: Special offer flag (boolean)

---

## Part 3: Create Base Template

### Step 3.1: Base HTML Template (`app/templates/base.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% block title %}CRUD App{% endblock %}</title>
<link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
<header>
<h1>My CRUD Application</h1>
<nav>
<a href="/">Home</a>
<a href="/items/">Items</a>
</nav>
</header>
<main>
{% block content %}{% endblock %}
</main>
<footer>
<p>&copy; 2024 CRUD Tutorial</p>
</footer>
</body>
</html>
```
**Template inheritance:**
- Other templates will `{% extends "base.html" %}`
- They override `{% block title %}` and `{% block content %}`
- Navigation links match Table 2 requirements

### Step 3.2: Basic CSS (`app/static/css/style.css`)

```css
* {
margin: 0;
padding: 0;
box-sizing: border-box;
}

body {
font-family: Arial, sans-serif;
line-height: 1.6;
background-color: #f4f4f4;
}

header {
background: #333;
color: #fff;
padding: 1rem;
text-align: center;
}

nav a {
color: #fff;
margin: 0 1rem;
text-decoration: none;
}

nav a:hover {
text-decoration: underline;
}

main {
max-width: 800px;
margin: 2rem auto;
padding: 2rem;
background: #fff;
border-radius: 8px;
box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

footer {
text-align: center;
padding: 1rem;
margin-top: 2rem;
color: #666;
}

.btn {
display: inline-block;
padding: 0.5rem 1rem;
margin: 0.5rem 0.25rem;
background: #007bff;
color: #fff;
text-decoration: none;
border: none;
border-radius: 4px;
cursor: pointer;
}

.btn:hover {
background: #0056b3;
}

.btn-danger {
background: #dc3545;
}

.btn-danger:hover {
background: #c82333;
}

.item-card {
border: 1px solid #ddd;
padding: 1rem;
margin: 1rem 0;
border-radius: 4px;
}

.item-card h3 {
margin-bottom: 0.5rem;
}

.offer-badge {
background: #28a745;
color: #fff;
padding: 0.25rem 0.5rem;
border-radius: 3px;
font-size: 0.8rem;
}

form {
display: flex;
flex-direction: column;
gap: 1rem;
}

label {
font-weight: bold;
}

input[type="text"],
input[type="number"] {
padding: 0.5rem;
border: 1px solid #ddd;
border-radius: 4px;
font-size: 1rem;
}

input[type="checkbox"] {
width: 20px;
height: 20px;
}
```
---

## Part 4: Create Templates

### Step 4.1: Landing Page (`app/templates/landing.html`)

```html
{% extends "base.html" %}

{% block title %}Home - CRUD App{% endblock %}

{% block content %}
<h2>Welcome to the CRUD Tutorial</h2>
<p>This is a simple CRUD application built with FastAPI, Jinja2, and pure HTML/CSS.</p>
<a href="/items/" class="btn">View Items</a>
{% endblock %}
```
**Matches Table 2:**
- Requires: `request` (passed by FastAPI)
- Links: `<a href="/items/">` to view items ✓

### Step 4.2: Items List Page (`app/templates/items_list.html`)

```html
{% extends "base.html" %}

{% block title %}Items List{% endblock %}

{% block content %}
<h2>Items List</h2>
<a href="/items/new" class="btn">Add New Item</a>

{% for item in items %}
<div class="item-card">
<h3>{{ item.name }}</h3>
<p>Price: ${{ "%.2f"|format(item.price) }}</p>
{% if item.is_offer %}
<span class="offer-badge">Special Offer!</span>
{% endif %}
<div>
<a href="/items/edit/{{ item.id }}" class="btn">Edit</a>
<form action="/items/delete/{{ item.id }}" method="post" style="display: inline;">
<button type="submit" class="btn btn-danger" onclick="return confirm('Are you sure?')">Delete</button>
</form>
</div>
</div>
{% endfor %}
{% endblock %}
```
**Matches Table 2:**
- Requires: `request`, `items` ✓
- Forms: Delete form with `action="/items/delete/{{ item.id }}"` and `method="post"` ✓
- Links: `<a href="/items/new">` and `<a href="/items/edit/{{ item.id }}">` ✓

**Important details:**
- Delete is a `<form>`, not a link (prevents accidental GET requests)
- `onclick="return confirm(...)"` asks for confirmation
- `style="display: inline;"` makes form appear next to Edit button

### Step 4.3: Item Form Page (`app/templates/item_form.html`)

```html
{% extends "base.html" %}

{% block title %}{% if editing %}Edit{% else %}Create{% endif %} Item{% endblock %}

{% block content %}
<h2>{% if editing %}Edit{% else %}Create New{% endif %} Item</h2>

<form action="{% if editing %}/items/{{ item_id }}{% else %}/items/{% endif %}" method="post">
<div>
<label for="name">Name:</label>
<input type="text" id="name" name="name" value="{{ name if editing else '' }}" required>
</div>

<div>
<label for="price">Price:</label>
<input type="number" id="price" name="price" step="0.01" value="{{ price if editing else '' }}" required>
</div>

<div>
<label for="is_offer">
<input type="checkbox" id="is_offer" name="is_offer" {% if editing and is_offer %}checked{% endif %}>
Special Offer
</label>
</div>

<div>
<button type="submit" class="btn">{% if editing %}Update{% else %}Create{% endif %}</button>
<a href="/items/" class="btn" style="background: #6c757d;">Cancel</a>
</div>
</form>
{% endblock %}
```
**Matches Table 2:**
- Requires: `request`, `editing`, and if editing: `item_id`, `name`, `price`, `is_offer` ✓
- Form action: `{% if editing %}/items/{{ item_id }}{% else %}/items/{% endif %}` ✓
- Form method: `post` ✓
- Links: `<a href="/items/">` to cancel ✓

**Critical details:**
- **Form action changes based on mode** (see Table 3):
  - Create mode: `action="/items/"`
  - Edit mode: `action="/items/{{ item_id }}"`
- Input values are pre-filled only when editing
- Checkbox is checked only when `editing and is_offer`
- `step="0.01"` allows decimal prices like $99.99

---
## Part 5: Implement CRUD Routes

### Step 5.1: Items Router Setup (`app/items.py`)
```python
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json
from pathlib import Path

router = APIRouter(prefix="/items", tags=["items"])
templates = Jinja2Templates(directory="app/templates")

DATA_FILE = Path("app/data/items.json")

def load_items():
"""Load items from JSON file"""
with open(DATA_FILE, "r") as f:
return json.load(f)

def save_items(items):
"""Save items to JSON file"""
with open(DATA_FILE, "w") as f:
json.dump(items, f, indent=2)
```
**Code explanation:**
- `APIRouter(prefix="/items")`: All routes start with `/items`
- `load_items()`: Reads JSON file and returns list of items
- `save_items(items)`: Writes list of items to JSON file
- `Path("app/data/items.json")`: Cross-platform file path

### Step 5.2: READ - List All Items

```python
@router.get("/")
async def list_items(request: Request):
items = load_items()
return templates.TemplateResponse("items_list.html", {
"request": request,
"items": items
})
```
**Matches Table 1:**
- Method: GET ✓
- Path: `/items/` (prefix + `/`) ✓
- Response: HTML with items data ✓

**Matches Table 5:**
- Passes `request` and `items` to template ✓

### Step 5.3: CREATE - Show Form and Handle Submission

```python
@router.get("/new")
async def new_item_form(request: Request):
return templates.TemplateResponse("item_form.html", {
"request": request,
"editing": False
})

@router.post("/")
async def create_item(
name: str = Form(...),
price: float = Form(...),
is_offer: bool = Form(False)
):
items = load_items()

# Generate new ID
new_id = max([item["id"] for item in items], default=-1) + 1

# Create new item
new_item = {
"id": new_id,
"name": name,
"price": price,
"is_offer": is_offer
}

items.append(new_item)
save_items(items)

return RedirectResponse(url="/items/", status_code=303)
```
**Matches Table 1:**
- `GET /items/new`: Shows form ✓
- `POST /items/`: Creates item ✓

**Matches Table 3:**
- Form at `/items/new` POSTs to `/items/` ✓

**Code details:**
- `Form(...)`: Required field (raises error if missing)
- `Form(False)`: Optional field with default value (fixes checkbox bug)
- `new_id = max(...) + 1`: Generates next available ID
- `status_code=303`: "See Other" redirect (best practice after POST)

### Step 5.4: UPDATE - Show Form and Handle Submission

**⚠️ CRITICAL: Note the different paths for GET and POST!**

```python
@router.get("/edit/{item_id}")
async def edit_item_form(request: Request, item_id: int):
items = load_items()

# Find item by ID
item = next((item for item in items if item["id"] == item_id), None)

if not item:
return RedirectResponse(url="/items/", status_code=303)

return templates.TemplateResponse("item_form.html", {
"request": request,
"editing": True,
"item_id": item["id"],
"name": item["name"],
"price": item["price"],
"is_offer": item["is_offer"]
})

@router.post("/{item_id}")
async def update_item(
item_id: int,
name: str = Form(...),
price: float = Form(...),
is_offer: bool = Form(False)
):
items = load_items()

# Find item index
item_index = next((i for i, item in enumerate(items) if item["id"] == item_id), None)

if item_index is None:
return RedirectResponse(url="/items/", status_code=303)

# Update item
items[item_index] = {
"id": item_id,
"name": name,
"price": price,
"is_offer": is_offer
}

save_items(items)

return RedirectResponse(url="/items/", status_code=303)
```
**Matches Table 1:**
- `GET /items/edit/{item_id}`: Shows pre-filled form ✓
- `POST /items/{item_id}`: Updates item ✓

**Matches Table 3:**
- Form at `/items/edit/5` POSTs to `/items/5` ✓

**Why Two Different Paths?**
- `GET /items/edit/{item_id}` - Shows the edit form (you see this in your browser)
- `POST /items/{item_id}` - Receives the form submission (RESTful convention)
- This follows REST principles where `/items/{item_id}` represents the item resource
- The form's `action` attribute must point to `POST /items/{item_id}`, not the edit URL

**Code details:**
- `next((item for item in items if ...), None)`: Finds item by ID
- `enumerate(items)`: Gets both index and item (needed to update list)
- If item not found, redirects to list

### Step 5.5: DELETE - Handle Deletion

```python
@router.post("/delete/{item_id}")
async def delete_item(item_id: int):
items = load_items()

# Remove item with matching ID
items = [item for item in items if item["id"] != item_id]

save_items(items)

return RedirectResponse(url="/items/", status_code=303)
```
**Matches Table 1:**
- `POST /items/delete/{item_id}`: Deletes item ✓

**Matches Table 3:**
- Delete form POSTs to `/items/delete/{item_id}` ✓

**Code details:**
- List comprehension filters out the item to delete
- Creates a new list without the matching item
- Always saves after modification

### Step 5.6: Complete `app/items.py` File

Here's the complete file for reference:

```python
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json
from pathlib import Path

router = APIRouter(prefix="/items", tags=["items"])
templates = Jinja2Templates(directory="app/templates")

DATA_FILE = Path("app/data/items.json")

def load_items():
"""Load items from JSON file"""
with open(DATA_FILE, "r") as f:
return json.load(f)

def save_items(items):
"""Save items to JSON file"""
with open(DATA_FILE, "w") as f:
json.dump(items, f, indent=2)

@router.get("/")
async def list_items(request: Request):
"""Display all items"""
items = load_items()
return templates.TemplateResponse("items_list.html", {
"request": request,
"items": items
})

@router.get("/new")
async def new_item_form(request: Request):
"""Show form to create new item"""
return templates.TemplateResponse("item_form.html", {
"request": request,
"editing": False
})

@router.post("/")
async def create_item(
name: str = Form(...),
price: float = Form(...),
is_offer: bool = Form(False)
):
"""Create a new item"""
items = load_items()

# Generate new ID
new_id = max([item["id"] for item in items], default=-1) + 1

# Create new item
new_item = {
"id": new_id,
"name": name,
"price": price,
"is_offer": is_offer
}

items.append(new_item)
save_items(items)

return RedirectResponse(url="/items/", status_code=303)

@router.get("/edit/{item_id}")
async def edit_item_form(request: Request, item_id: int):
"""Show form to edit existing item"""
items = load_items()

# Find item by ID
item = next((item for item in items if item["id"] == item_id), None)

if not item:
return RedirectResponse(url="/items/", status_code=303)

return templates.TemplateResponse("item_form.html", {
"request": request,
"editing": True,
"item_id": item["id"],
"name": item["name"],
"price": item["price"],
"is_offer": item["is_offer"]
})

@router.post("/{item_id}")
async def update_item(
item_id: int,
name: str = Form(...),
price: float = Form(...),
is_offer: bool = Form(False)
):
"""Update an existing item"""
items = load_items()

# Find item index
item_index = next((i for i, item in enumerate(items) if item["id"] == item_id), None)

if item_index is None:
return RedirectResponse(url="/items/", status_code=303)

# Update item
items[item_index] = {
"id": item_id,
"name": name,
"price": price,
"is_offer": is_offer
}

save_items(items)

return RedirectResponse(url="/items/", status_code=303)

@router.post("/delete/{item_id}")
async def delete_item(item_id: int):
"""Delete an item"""
items = load_items()

# Remove item with matching ID
items = [item for item in items if item["id"] != item_id]

save_items(items)

return RedirectResponse(url="/items/", status_code=303)
```
---

## Part 6: Run the Application

### Step 6.1: Start the Server

```bash
uvicorn app.main:app --reload
```
**What this does:**
- `app.main:app`: Loads the `app` object from `app/main.py`
- `--reload`: Auto-restarts server when code changes
- Server runs on `http://localhost:8000`

### Step 6.2: Open Browser

Visit:

```text
http://localhost:8000
```
You should see the landing page.

---

## Part 7: Test Every CRUD Operation

### ✅ Test 1: View Items
1. Open homepage at `http://localhost:8000`
2. Click "View Items" button
3. Verify you see the 3 default items (Laptop, Mouse, Keyboard)

**Expected URL:** `http://localhost:8000/items/`

### ✅ Test 2: Create Item
1. Click "Add New Item" button
2. Fill in the form:
   - Name: `Monitor`
   - Price: `299.99`
   - Check "Special Offer" if desired
3. Click "Create" button
4. Verify you're redirected to items list
5. Verify new item appears at the bottom

**URLs involved:**
- Form page: `http://localhost:8000/items/new`
- Form submits to: `POST http://localhost:8000/items/`
- Redirects to: `http://localhost:8000/items/`

### ✅ Test 3: Edit Item
1. Click "Edit" button on any item (e.g., Laptop)
2. Verify form is pre-filled with existing values
3. Change some values:
   - Name: `Gaming Laptop`
   - Price: `1299.99`
   - Toggle "Special Offer"
4. Click "Update" button
5. Verify you're redirected to items list
6. Verify changes appear in the list

**URLs involved:**
- Form page: `http://localhost:8000/items/edit/0` (browser shows this)
- Form submits to: `POST http://localhost:8000/items/0` (different!)
- Redirects to: `http://localhost:8000/items/`

**Important:**
- Browser URL while editing: `/items/edit/0`
- Form submission target: `/items/0`
- These are intentionally different (see Table 3)

### ✅ Test 4: Delete Item
1. Click "Delete" button on any item
2. Confirm the popup dialog
3. Verify you're redirected to items list
4. Verify item no longer appears

**URLs involved:**
- Form submits to: `POST http://localhost:8000/items/delete/0`
- Redirects to: `http://localhost:8000/items/`

### ✅ Test 5: Data Persistence
1. Create/edit/delete some items
2. Stop the server (Ctrl+C)
3. Check `app/data/items.json` - changes should be saved
4. Restart the server
5. Verify changes persisted

---

## Final Project Structure

```text
my_crud_app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── items.py
│   │
│   ├── data/
│   │   └── items.json
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── landing.html
│   │   ├── items_list.html
│   │   └── item_form.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
└── requirements.txt (optional)
```
---

## Key Lessons Learned

### 1. Design Before Coding
You designed:
- All endpoints (Table 1)
- All pages (Table 2)
- All form actions (Table 3)
- All data flow (Table 4)

before writing implementation code.

### 2. GET vs POST
- **GET** → Show pages/data (safe, idempotent)
- **POST** → Modify data (not safe, not idempotent)

### 3. Form Action vs Page URL
These are often different:

| Page URL | Form Action | Why Different? |
|----------|-------------|----------------|
| `/items/new` | `/items/` | "new" is UI route, "/" is resource collection |
| `/items/edit/5` | `/items/5` | "edit" is UI route, "/5" is resource identifier |

This distinction prevents the 405 error and follows REST conventions.

### 4. Post/Redirect/Get Pattern
After every POST:
1. Modify data
2. Save to storage
3. Redirect to GET endpoint

This prevents duplicate submissions when user refreshes the page.

### 5. Reusable Templates
One `item_form.html` handles both:
- Create mode (`editing=False`)
- Edit mode (`editing=True`)

The template adapts using Jinja2 conditionals.

### 6. Checkbox Handling
HTML checkboxes:
- Send value when checked
- Send nothing when unchecked

Solution: `is_offer: bool = Form(False)` provides default value.

---

## Common Debugging Checklist

When something breaks, check these:

### 405 Method Not Allowed
**Symptoms:** Form submission fails with 405 error

**Check:**
- Does the route exist in `items.py`?
- Is the HTTP method correct (GET vs POST)?
- Does form `action` attribute match the route path exactly?

**Example fix:**
```html
<!-- Wrong -->
<form action="/items/edit/{{ item_id }}" method="post">

<!-- Correct -->
<form action="/items/{{ item_id }}" method="post">
```
### 422 Unprocessable Entity
**Symptoms:** Form submission fails with 422 error

**Check:**
- Is `python-multipart` installed? (`pip install python-multipart`)
- Do form field `name` attributes match FastAPI `Form()` parameters?
- Are required fields marked with `Form(...)` not `Form(default)`?

### Template Not Found
**Symptoms:** `TemplateNotFound: item_form.html`

**Check:**
- Is template path correct in `Jinja2Templates(directory="...")`?
- Does the file exist in the templates folder?
- Is the filename spelled correctly (case-sensitive)?

### CSS Not Loading
**Symptoms:** Page has no styling

**Check:**
- Is static folder mounted? (`app.mount("/static", ...)`)
- Is CSS path correct in HTML? (`/static/css/style.css`)
- Check browser console for 404 errors

### Data Not Saving
**Symptoms:** Changes disappear after restart

**Check:**
- Are you calling `save_items(items)` after modifications?
- Does the `app/data/` directory exist?
- Check file permissions on `items.json`

### Wrong Item Edited/Deleted
**Symptoms:** Editing item #5 changes item #3

**Check:**
- Are you using `item["id"]` not list index?
- Is ID generation correct? (`max([item["id"] ...]) + 1`)

---

## Next Improvements

After mastering this tutorial, you can add:

### Beginner Level:
- Flash messages for success/error feedback
- Form validation (min/max price, name length)
- Sorting items by name or price
- Search/filter functionality

### Intermediate Level:
- SQLite database instead of JSON
- SQLAlchemy ORM
- Pagination (show 10 items per page)
- User authentication and sessions
- File uploads for item images

### Advanced Level:
- PostgreSQL database
- Async database operations
- Docker containerization
- API documentation with Swagger
- HTMX for dynamic updates (still no JavaScript!)
- Deployment to cloud (Heroku, Railway, etc.)

---

## Conclusion

You built a complete CRUD web application using:

- **FastAPI** - Modern Python web framework
- **Jinja2** - Server-side templating
- **HTML/CSS** - Pure frontend (no JavaScript)
- **JSON** - Simple data storage
- **RESTful routing** - Industry-standard API design
- **Server-side rendering** - Traditional web architecture

Most importantly, you learned:
- **API-first thinking** - Design endpoints before coding
- **Form-to-endpoint mapping** - Understanding HTTP methods
- **REST conventions** - Resource-based URL design
- **Proper CRUD architecture** - Separation of concerns

These concepts apply to **all backend frameworks**, not just FastAPI. Whether you move to Django, Flask, Express.js, Spring Boot, or Rails, these principles remain the same.

**Congratulations!** You now understand the fundamentals of web application development.
