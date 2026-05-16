# Workshop 4.5: Client‑Side Rendering with Vue.js  
## The Bridge Between Server‑Rendered HTML and Modern SPAs

**Time:** ~60 minutes  
**What you need:** Your Part 4 backend running, a modern browser, and curiosity.

---

## Introduction: The Paradigm Shift

### How Part 4 Works (Server‑Side Rendering)

In Part 4, your FastAPI backend does **all the work**:

```
Browser → GET /products/landing → Backend
  │                                │
  │                                ├── Queries SQLite
  │                                ├── Takes the data
  │                                ├── Stuffs it into a Jinja2 template
  │                                └── Sends back a complete HTML page
  │                               
  └── The browser just displays it 
```

Every click — sort, search, paginate, add, delete — triggers a **full page reload**.  
The screen flickers. State is lost. It feels like 2005.

### How Vue.js Works (Client‑Side Rendering)

With Vue.js, the browser does the rendering work:

```
Browser                        Backend
  │                               │
  │  fetch('/api/products')       │
  │ ──────────────────────────►   │
  │                               ├── Queries SQLite
  │                               └── Returns JSON (raw data, no HTML)
  │  ◄──────────────────────────  │
  │                               │
  ├── Vue.js takes the JSON      │
  ├── Builds the HTML            │
  └── Displays it                │
  │                               │
  │  User clicks "Sort by Price"  │
  │                               │
  │  fetch('/api/products?sort=price')
  │ ──────────────────────────►   │
  │  ◄──────────────────────────  │
  │                               │
  ├── Vue.js updates ONLY        │
  │   the table rows             │
  └── No page reload!            │
```

The server **stops caring about HTML**. It just returns JSON — the same data you already query with SQLAlchemy. Vue.js takes that data and builds the HTML dynamically.

### The Analogy

| | Jinja2 (Parts 1–4) | Vue.js (Part 4.5→5) |
|---|---|---|
| **Server sends** | Fully plated meal (HTML) | Raw ingredients (JSON) |
| **Browser does** | Just eats it | Cooks it into a meal |
| **Change request** | Send plate back, wait for new one | Grab different ingredients, re‑cook only what changed |
| **Flicker?** | Yes — full reload every time | No — only data updates |

### Why This Matters

1. **Faster UX** – No page reloads. Click sort and the table re‑sorts instantly.  
2. **Less server load** – JSON is lighter than HTML.  
3. **Separation of concerns** – Backend developers focus on data/APIs, frontend developers focus on UI.  
4. **Mobile‑ready** – The same JSON API powers your web app, mobile app, and third‑party integrations.

### What You’ll Build

A **product viewer** that:
- Logs into your Part 4 backend
- Fetches the same 21 products from the database
- Renders them in a sortable, paginated table
- Does **zero page reloads**

All in a single HTML file, with Vue.js loaded from a CDN.

---

## Step 0: Setup – Extend Part 4 with JSON Endpoints

**Goal:** Give the frontend a way to talk to the backend with JSON (not HTML).  
**Mental model:** The server becomes a *data provider*; the frontend becomes the *renderer*.

### 0.1 Prerequisites

Your Part 4 backend must be set up and seeded:

```bash
cd item_management_sqlalchemy_v4
python seed.py                     # (first time only)
```

### 0.2 Create the API Directory

Create a new folder for JSON API routes:

```bash
mkdir app\api
```

Create `app/api/__init__.py` (empty file).

### 0.3 Create the Auth API

Create `app/api/auth_api.py`:

```python
import hashlib
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin

router = APIRouter(prefix="/api/auth", tags=["Auth API"])


@router.post("/login")
async def api_login(request: Request, db: Session = Depends(get_db)):
    """JSON login endpoint. Accepts {username, password}, returns session cookie."""
    body = await request.json()
    pw_hash = hashlib.sha256(body["password"].encode()).hexdigest()
    admin = db.query(Admin).filter(
        Admin.username == body["username"],
        Admin.password_hash == pw_hash,
    ).first()
    if not admin:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Invalid credentials"},
        )
    request.session["admin_id"] = admin.id
    return {"success": True, "admin_id": admin.id}
```

### 0.4 Create the Products API

Create `app/api/products_api.py`:

```python
from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product

router = APIRouter(prefix="/api/products", tags=["Products API"])


@router.get("")
async def list_products_api(
    request: Request,
    sort: str = Query("name"),
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """JSON product list with sort and pagination. Requires auth."""
    if not request.session.get("admin_id"):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    order_map = {"name": Product.name, "price": Product.price, "stock": Product.stock}
    order_col = order_map.get(sort, Product.id)

    query = db.query(Product).order_by(order_col)
    total = query.count()
    products = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "stock": p.stock,
                "category_name": p.category.name if p.category else None,
            }
            for p in products
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": max(1, (total + per_page - 1) // per_page),
    }
```

### 0.5 Register the API Routes in `main.py`

Edit `app/main.py`. Add two new imports at the top:

```python
from fastapi.responses import HTMLResponse      # ← new
from app.api import auth_api, products_api       # ← new
```

Add two `app.include_router()` calls after the existing ones:

```python
app.include_router(orders.router, prefix="/orders")

# JSON API routes (new in Part 4.5)
app.include_router(auth_api.router)
app.include_router(products_api.router)
```

Add a route to serve our Vue HTML file at the end of the file (after the `root()` route):

```python
@app.get("/viewer", include_in_schema=False)
async def product_viewer():
    """Serves the Vue.js product viewer HTML file."""
    with open("product-viewer.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())
```

### 0.6 Test the API Endpoints

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000/docs` and verify you see:
- The new `Auth API` section with `POST /api/auth/login`
- The new `Products API` section with `GET /api/products`

Test the login manually:

1. In the docs, expand `POST /api/auth/login` and click “Try it out”.
2. Use `{ "username": "admin", "password": "admin123" }` (the credentials from your seed script).
3. Execute. You should see a `200` response with `{"success": true, "admin_id": 1}`.

Test products (you’ll be automatically logged in because the docs share the session):

1. Expand `GET /api/products` and click “Try it out”.
2. Set `per_page` to `3` and execute.
3. You should see a JSON array with 3 products and `"total": 21`.

**What you just did:** You proved the server now speaks pure JSON. This is the “data API” our Vue frontend will consume.

### 0.7 Create the Vue HTML Starter File

Create `product-viewer.html` in the **same directory** as `seed.py` (the project root) with this template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Product Viewer</title>
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body>
  <div id="app">
    <!-- We'll fill this in step by step -->
  </div>
  <script>
    const { createApp } = Vue

    createApp({
      data() {
        return {}
      },
      methods: {},
      created() {}
    }).mount('#app')
  </script>
</body>
</html>
```

### 0.8 Open the Viewer

Navigate to `http://localhost:8000/viewer`. You’ll see a blank page — that’s perfect. We’ll add content from the next step.

> **Why `/viewer`?** The backend serves the HTML from the same domain (`localhost:8000`). That means our `fetch()` calls can be relative (`/api/products`), and the browser will automatically send session cookies. No CORS headaches, no cross‑origin issues.

**Checkpoint:** Your backend now exposes JSON APIs, and you have an empty Vue page ready to be painted.

---

## Step 1: Hello Vue – Reactive Data Binding

**Goal:** Make Vue display dynamic text that updates automatically.  
**Mental model:** Vue watches JavaScript variables and rewrites parts of the DOM when they change.

### 1.1 Add the Template

Inside `<div id="app">`, replace the placeholder comment with:

```html
<h1>Product Viewer</h1>
<p>Welcome, {{ username }}!</p>
<p>You have <strong>{{ productCount }}</strong> products in the database.</p>
```

### 1.2 Add Reactive Data

In the `data()` function, replace the empty `return {}` with:

```javascript
data() {
  return {
    username: 'Admin',
    productCount: 0
  }
},
```

### 1.3 Save and Refresh

Reload `http://localhost:8000/viewer`. You should see:

```
Product Viewer
Welcome, Admin!
You have 0 products in the database.
```

### 1.4 What Just Happened?

| Code | What it does |
|------|-------------|
| `createApp({...})` | Creates a Vue application attached to `#app` |
| `data() { return { username: 'Admin' } }` | Declares a **reactive variable** `username` |
| `{{ username }}` | Vue replaces it with `'Admin'` and **watches it** for changes |
| `{{ productCount }}` | Vue replaces it with `0` and watches it too |

### 1.5 Prove Reactivity in Real Time

In your `<script>` block, temporarily change the last line from:

```javascript
}).mount('#app')
```

to:

```javascript
window.app = createApp({...}).mount('#app')
```

Now save, refresh, and open the browser console (F12). Type:

```javascript
app.username = "Glitch"
```

The page instantly updates to **“Welcome, Glitch!”** — no reload, no extra code.  
Remove the `window.app =` wrapper afterwards; you won’t need it again.

### 1.6 Jinja2 vs Vue

| | Jinja2 (Parts 1–4) | Vue.js (Part 4.5) |
|---|---|---|
| **Where it runs** | Server (Python) | Browser (JavaScript) |
| **When it renders** | On HTTP request | When data changes |
| **`{{ username }}`** | Replaced once, sent as HTML | Watched continuously, updates live |
| **To change value** | Reload the page | Just update the variable |

**Checkpoint:** You’ve seen that Vue variables are alive — change them and the page follows. Next you’ll control one from an input field.

---

## Step 2: Two‑Way Binding with `v-model`

**Goal:** Let the user type something and see it echoed immediately, without any event‑handling code.  
**Mental model:** `v-model` creates a live wire between an `<input>` and a data variable.

### 2.1 Add the Search Input

Inside `<div id="app">`, after the two `<p>` tags, paste:

```html
<div style="margin: 1rem 0;">
  <input v-model="search" placeholder="Type to search..." style="width: 100%; padding: 0.5rem;" />
  <p><em>You typed: <strong>{{ search }}</strong></em></p>
</div>
```

### 2.2 Add the Data Variable

Add `search` to `data()`:

```javascript
data() {
  return {
    username: 'Admin',
    productCount: 0,
    search: ''          // ← add this
  }
},
```

### 2.3 Save and Refresh

Type “laptop” into the input field. You’ll see “You typed: **laptop**” update with every keystroke. No extra JavaScript required.

### 2.4 How `v-model` Works

```
┌─────────────────────────────────┐
│      v-model="search"           │
│                                 │
│  User types "laptop"            │
│       │                        │
│       ▼                        │
│  search = "laptop" (data)       │
│       │                        │
│       ▼                        │
│  {{ search }} → "laptop"        │
│  (template updates)             │
│       │                        │
│  You type more → search updates │
│  → template re‑renders          │
└─────────────────────────────────┘
```

`v-model` is **two‑way binding**: input changes update the data, data changes update the input.

### 2.5 Compare with Vanilla JavaScript

Without Vue, you’d have to write:

```javascript
document.querySelector('input').addEventListener('input', function(e) {
  document.querySelector('p strong').textContent = e.target.value
})
```

With Vue, it’s just `<input v-model="search">` and `{{ search }}`.

**Checkpoint:** You now have a live search field that reflects its content in real time. Next you’ll render a list of items.

---

## Step 3: Display a List with `v-for`

**Goal:** Show a table of hardcoded products. We’ll replace them with real data later.  
**Mental model:** `v-for` is like a Jinja2 `for` loop, but it lives in the browser and updates whenever the array changes.

### 3.1 Add the Table Template

After the search `<div>`, paste:

```html
<h2>Products</h2>

<table border="1" style="width: 100%; border-collapse: collapse; margin-top: 0.5rem;">
  <thead>
    <tr>
      <th>ID</th>
      <th>Name</th>
      <th>Price</th>
      <th>Stock</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="p in products" :key="p.id">
      <td>{{ p.id }}</td>
      <td>{{ p.name }}</td>
      <td>${{ p.price.toFixed(2) }}</td>
      <td>{{ p.stock }}</td>
    </tr>
  </tbody>
</table>

<p v-if="products.length === 0">No products to show yet.</p>
```

### 3.2 Add Hardcoded Products

Add a `products` array to `data()`:

```javascript
data() {
  return {
    username: 'Admin',
    productCount: 0,
    search: '',
    products: [
      { id: 1, name: 'Laptop', price: 999.99, stock: 10 },
      { id: 2, name: 'Mouse', price: 25.50, stock: 50 },
      { id: 3, name: 'Keyboard', price: 75.00, stock: 30 },
    ]
  }
},
```

### 3.3 Save and Refresh

You should see a table with 3 rows: Laptop, Mouse, Keyboard. The prices are formatted with `toFixed(2)`.

### 3.4 How `v-for` Works

```
<tr v-for="p in products" :key="p.id">
  │
  ├── Iteration 1: p = { id:1, name:'Laptop',  price:999.99, stock:10 }
  ├── Iteration 2: p = { id:2, name:'Mouse',   price:25.50,  stock:50 }
  └── Iteration 3: p = { id:3, name:'Keyboard', price:75.00,  stock:30 }
```

- `v-for="p in products"` — loop over the array; each item becomes `p`.
- `:key="p.id"` — unique identifier. Always include it to help Vue track elements.
- `{{ p.name }}` — access properties just like in Jinja2.

**Checkpoint:** You can render lists dynamically. The empty state message (`v-if`) appears if the array is empty. Next you’ll ditch the hardcoded data and connect to a real API.

---

## Step 4: Connect to the Real API

**Goal:** Replace hardcoded products with live data from your Part 4 backend.  
**Mental model:** `fetch()` asks the server for JSON; Vue then displays it. The browser stays on the same page.

### 4.1 Clean Up the Data

First, remove the hardcoded `products` array from `data()`. Replace it with an empty array:

```javascript
products: [],
```

Also remove `productCount: 0` — we’ll use `products.length` directly in the template.

### 4.2 Add Login and Data‑Loading Methods

Replace the `methods: {}` object with:

```javascript
methods: {
  async login() {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'admin', password: 'admin123' })
    })
    if (!res.ok) throw new Error('Login failed')
  },
  async loadProducts() {
    this.loading = true
    try {
      const params = new URLSearchParams({
        sort: 'name',
        page: 1,
        per_page: 100
      })
      const res = await fetch(`/api/products?${params}`)
      if (!res.ok) throw new Error('Failed to load products')
      const data = await res.json()
      this.products = data.products
    } catch (e) {
      console.error('Failed to load products', e)
      this.products = []
    } finally {
      this.loading = false
    }
  }
},
```

> **`JSON.stringify(obj)`** converts a JS object into a JSON string.  
> **`URLSearchParams({...})`** builds a query string (`sort=name&page=1&per_page=100`).  
> **`async/await`** makes asynchronous code read like synchronous code.

### 4.3 Trigger the Workflow When the App Starts

Replace `created() {}` with:

```javascript
async created() {
  await this.login()       // Login once — cookie stored by browser
  await this.loadProducts()  // Then load products
},
```

### 4.4 Update the Template

Change the product count line from:

```html
<p>You have <strong>{{ productCount }}</strong> products in the database.</p>
```

to:

```html
<p>You have <strong>{{ products.length }}</strong> products in the database.</p>
```

### 4.5 Save and Refresh

You should now see a table with **21 products** loaded directly from the database, all without a page reload!

### 4.6 What Just Happened: The Full Request‑Response Cycle

1. **Page loads** → Vue’s `created()` runs.
2. `login()` sends `POST /api/auth/login` with credentials.
3. Backend validates, sets a session cookie. The browser stores it automatically.
4. `loadProducts()` sends `GET /api/products?sort=name&per_page=100`. Because the request is to the same origin (`localhost:8000`), the cookie is sent automatically.
5. Backend checks auth, queries SQLite, returns JSON with 21 products.
6. `this.products = data.products` — Vue notices the change and re‑renders the table.
7. The page now shows 21 products, instantly.

### 4.7 Why We Login Only Once

The browser remembers the session cookie. All subsequent requests include it automatically. No need to log in again.

> **Same‑origin advantage:** Our HTML is served from `http://localhost:8000/viewer` and the API from `http://localhost:8000/api/...`. That’s the same origin, so cookies flow freely. In Part 5, when frontend and backend run on different ports, we’ll use `credentials: 'include'`.

### 4.8 Inspect the Magic

Open the browser’s Developer Tools (F12) → Network tab. Reload the page. You’ll see:
- `viewer` (the HTML file)
- `login` (a POST to `/api/auth/login`)
- `products?sort=name&page=1&per_page=100` (a GET with JSON response)

Click on the products request and look at the “Response” tab. You’ll see the raw JSON your frontend received.

**Checkpoint:** You’ve replaced static data with a live API call. The browser fetches JSON, not HTML, and Vue builds the UI. Next you’ll add loading states and empty‑state handling.

---

## Step 5: Loading and Empty States with `v-if`

**Goal:** Provide visual feedback while data loads and when no products exist.  
**Mental model:** `v-if` toggles entire DOM elements; Vue doesn’t even render them if the condition is false.

### 5.1 Add a Loading Flag

In `data()`, add:

```javascript
loading: false
```

### 5.2 Use It in `loadProducts()`

We already set `this.loading = true` at the start and `this.loading = false` in `finally`. So the method from Step 4 already handles it.

### 5.3 Replace the Old `v-if` with Loading/Empty States

Find this line:

```html
<p v-if="products.length === 0">No products to show yet.</p>
```

Replace it with:

```html
<div v-if="loading" style="padding: 2rem; text-align: center; color: #666;">
  <em>Loading products...</em>
</div>

<div v-else-if="products.length === 0" style="padding: 2rem; text-align: center; color: #999;">
  No products found.
</div>
```

And add `v-else` to the `<table>` tag:

```html
<table v-else border="1" style="width: 100%; border-collapse: collapse; margin-top: 0.5rem;">
```

### 5.4 Save and Refresh

You’ll briefly see “Loading products…” before the table appears. If you temporarily block the API request (e.g., by stopping the backend), you’ll see “No products found.”

### 5.5 How `v-if` / `v-else-if` / `v-else` Work

Only **one** of these branches is rendered at any time:

```
v-if="loading"          →  "Loading products..."
v-else-if="empty"       →  "No products found."
v-else                  →  The table
```

| Directive | Behavior | Use case |
|-----------|----------|----------|
| `v-if` | Removes/adds elements from the DOM | Rarely toggled states (loading, auth) |
| `v-show` | Always in DOM, toggles `display:none` | Frequently toggled (tooltips, menus) |

**Checkpoint:** Your app now communicates what’s happening. Users never stare at a blank screen.

---

## Step 6: Sort Controls with `@click` and `:class`

**Goal:** Add sort buttons that change the order of products and highlight the active button.  
**Mental model:** Click events update a reactive variable; the UI reflects it instantly. The server re‑sorts the data.

### 6.1 Add the Sort Variable

In `data()`, add:

```javascript
sortBy: 'name'
```

### 6.2 Update `loadProducts()` to Use `sortBy`

In `loadProducts()`, change the `params` to:

```javascript
const params = new URLSearchParams({
  sort: this.sortBy,    // ← now dynamic
  page: 1,
  per_page: 5           // ← reduce to 5 to see pagination later
})
```

### 6.3 Add Sort Buttons to the Template

Place this block between the search `<div>` and the `<h2>Products</h2>` heading:

```html
<div style="margin: 1rem 0; display: flex; gap: 0.5rem; align-items: center;">
  <span style="font-weight: bold;">Sort by:</span>
  <button @click="sortBy = 'name'; loadProducts()"
          :class="{ active: sortBy === 'name' }">Name</button>
  <button @click="sortBy = 'price'; loadProducts()"
          :class="{ active: sortBy === 'price' }">Price</button>
  <button @click="sortBy = 'stock'; loadProducts()"
          :class="{ active: sortBy === 'stock' }">Stock</button>
</div>
```

### 6.4 Add Styling

Inside `<head>`, add a `<style>` block (if not already present):

```html
<style>
  body { font-family: sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; }
  .active { background: #2b9348; color: white; font-weight: bold; border: none; border-radius: 4px; }
  button { border: 1px solid #ccc; border-radius: 4px; padding: 0.3rem 0.8rem; cursor: pointer; background: #f5f5f5; }
  button:hover { background: #e0e0e0; }
</style>
```

### 6.5 Save and Refresh

Click “Price” — the table re‑sorts by price. The “Price” button turns green. No page reload. Click “Name” to revert. Everything updates in under a second.

### 6.6 What’s Happening?

- `@click="sortBy = 'name'; loadProducts()"` — two actions: change `sortBy`, then fetch fresh data.
- `:class="{ active: sortBy === 'name' }"` — Vue adds the `active` CSS class when the condition is true.

### 6.7 The Shorthand `:`

| Shorthand | Full directive | Purpose |
|-----------|----------------|---------|
| `:class` | `v-bind:class` | Dynamically bind CSS classes |
| `:key` | `v-bind:key` | Unique identifier for list elements |
| `:disabled` | `v-bind:disabled` | Enable/disable a button |

Any HTML attribute can be dynamic with `:`.

**Checkpoint:** You can now sort products on the fly. Next you’ll add pagination so users can browse all 21 products.

---

## Step 7: Pagination

**Goal:** Let users navigate through pages of products.  
**Mental model:** The backend does the heavy lifting (LIMIT/OFFSET); the frontend just changes a page number and re‑fetches.

### 7.1 Add Pagination State

Add to `data()`:

```javascript
currentPage: 1,
totalPages: 1
```

### 7.2 Update `loadProducts()` to Use and Capture Pagination

Change the `params` and store the total pages:

```javascript
const params = new URLSearchParams({
  sort: this.sortBy,
  page: this.currentPage,   // now dynamic
  per_page: 5
})
```

After `const data = await res.json();`, add:

```javascript
this.totalPages = data.total_pages
```

### 7.3 Add Pagination Controls

After the closing `</table>` tag, paste:

```html
<div v-if="totalPages > 1" style="margin-top: 1rem; display: flex; gap: 0.3rem; justify-content: center; align-items: center;">
  <button @click="currentPage--; loadProducts()"
          :disabled="currentPage <= 1">← Previous</button>

  <span v-for="n in totalPages" :key="n"
        @click="currentPage = n; loadProducts()"
        :class="{ active: n === currentPage }"
        style="padding: 0.3rem 0.8rem; cursor: pointer; border: 1px solid #ccc; border-radius: 4px;">
    {{ n }}
  </span>

  <button @click="currentPage++; loadProducts()"
          :disabled="currentPage >= totalPages">Next →</button>
</div>

<p style="text-align: center; color: #666; margin-top: 0.5rem;">
  Page {{ currentPage }} of {{ totalPages }} ({{ products.length }} products on this page)
</p>
```

### 7.4 Add Disabled Button Styling

In the `<style>` block, add:

```css
button:disabled { opacity: 0.5; cursor: not-allowed; }
```

### 7.5 Save and Refresh

You now have 5 products per page. Click page numbers or Previous/Next. The URL doesn’t change, the page doesn’t reload — only the table data updates.

**Checkpoint:** Full pagination works. You’ve completed the core features.

---

## Step 8: The Complete File

If you ever get lost, here’s the entire working `product-viewer.html`. Compare it with yours to spot differences.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Product Viewer</title>
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
  <style>
    body { font-family: sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; }
    table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
    th, td { padding: 0.5rem; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #f5f5f5; }
    .active { background: #2b9348; color: white; font-weight: bold; border: none; border-radius: 4px; }
    button { border: 1px solid #ccc; border-radius: 4px; padding: 0.3rem 0.8rem; cursor: pointer; background: #f5f5f5; }
    button:hover { background: #e0e0e0; }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    .low-stock { color: #d62828; font-weight: bold; }
  </style>
</head>
<body>
<div id="app">
  <h1>Product Viewer</h1>
  <p>Welcome, {{ username }}!</p>
  <p>You have <strong>{{ products.length }}</strong> products in the database.</p>

  <div style="margin: 1rem 0;">
    <input v-model="search" placeholder="Type to search..." style="width:100%; padding:0.5rem;" />
    <p><em>You typed: <strong>{{ search }}</strong></em></p>
  </div>

  <div style="margin: 1rem 0; display: flex; gap: 0.5rem; align-items: center;">
    <span style="font-weight: bold;">Sort by:</span>
    <button @click="sortBy='name'; loadProducts()" :class="{ active: sortBy==='name' }">Name</button>
    <button @click="sortBy='price'; loadProducts()" :class="{ active: sortBy==='price' }">Price</button>
    <button @click="sortBy='stock'; loadProducts()" :class="{ active: sortBy==='stock' }">Stock</button>
  </div>

  <div v-if="loading" class="loading"><em>Loading products...</em></div>

  <div v-else-if="products.length === 0" class="empty">No products found.</div>

  <table v-else>
    <thead>
      <tr><th>ID</th><th>Name</th><th>Price</th><th>Stock</th></tr>
    </thead>
    <tbody>
      <tr v-for="p in products" :key="p.id">
        <td>{{ p.id }}</td>
        <td>{{ p.name }}</td>
        <td>${{ p.price.toFixed(2) }}</td>
        <td :class="{ 'low-stock': p.stock < 5 }">{{ p.stock }}</td>
      </tr>
    </tbody>
  </table>

  <div v-if="totalPages > 1" style="margin-top:1rem; display:flex; gap:0.3rem; justify-content:center; align-items:center;">
    <button @click="currentPage--; loadProducts()" :disabled="currentPage <= 1">← Previous</button>
    <span v-for="n in totalPages" :key="n" @click="currentPage=n; loadProducts()"
          :class="{ active: n===currentPage }" style="padding:0.3rem 0.8rem; border:1px solid #ccc; border-radius:4px; cursor:pointer;">
      {{ n }}
    </span>
    <button @click="currentPage++; loadProducts()" :disabled="currentPage >= totalPages">Next →</button>
  </div>

  <p style="text-align:center; color:#666; margin-top:0.5rem;">
    Page {{ currentPage }} of {{ totalPages }} ({{ products.length }} products on this page)
  </p>
</div>

<script>
  const { createApp } = Vue

  createApp({
    data() {
      return {
        username: 'Admin',
        search: '',
        products: [],
        loading: false,
        sortBy: 'name',
        currentPage: 1,
        totalPages: 1,
      }
    },
    async created() {
      await this.login()
      await this.loadProducts()
    },
    methods: {
      async login() {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: 'admin', password: 'admin123' }),
        })
        if (!res.ok) throw new Error('Login failed')
      },
      async loadProducts() {
        this.loading = true
        try {
          const params = new URLSearchParams({
            sort: this.sortBy,
            page: this.currentPage,
            per_page: 5,
          })
          const res = await fetch(`/api/products?${params}`)
          if (!res.ok) throw new Error('Failed to load products')
          const data = await res.json()
          this.products = data.products
          this.totalPages = data.total_pages
        } catch (e) {
          console.error('Failed to load products', e)
          this.products = []
        } finally {
          this.loading = false
        }
      },
    }
  }).mount('#app')
</script>
</body>
</html>
```

**Checkpoint:** You now have a complete, working product viewer. The rest of the workshop reinforces what you’ve built and adds challenges.

---

## Step 9: What You’ve Learned

### Vue Concepts, Step by Step

| Step | Concept | You Added | You Saw |
|------|---------|-----------|---------|
| 1 | `{{ }}` + `data()` | Hello text | “Welcome, Admin!” |
| 2 | `v-model` | Search input | Text updates as you type |
| 3 | `v-for` | Hardcoded table | 3 products in a table |
| 4 | `fetch()` + `created()` + `async/await` | Real API call | 21 products from DB |
| 5 | `v-if/v-else` | Loading/empty states | “Loading...” or table |
| 6 | `@click` + `:class` | Sort buttons | Click to re‑sort |
| 7 | Pagination logic | Page buttons | Navigate through pages |

### Architecture: The Full Data Flow

```
User clicks "Sort by Price"
    │
    ▼
@click sets this.sortBy = 'price'
    │
    ▼
:class recalculates (Price button turns green)
    │
    ▼
loadProducts() calls fetch('/api/products?sort=price&page=1')
    │
    ▼
Backend queries SQLite, returns JSON
    │
    ▼
this.products = data.products
this.totalPages = data.total_pages
    │
    ▼
Vue detects changes → re‑renders the table
    │
    ▼
You see products sorted by price — no page reload
```

---

## Step 10: Bridge to Part 5

In Part 5, you’ll transform this single‑file prototype into a production‑grade SPA.

| This tutorial | Part 5 |
|---------------|--------|
| Single `product-viewer.html` file | Multiple `.vue` files in `src/views/` |
| Vue from CDN (`<script>` tag) | Vue from npm (`import` statements) |
| API routes added to Part 4 backend | Separate `backend/` + `frontend/` folders |
| Login called once in `created()` | Auth guard in Vue Router |
| Backend serves JSON (manual parsing) | Pydantic schemas for validation |
| Same origin (`localhost:8000`) | CORS proxy: `localhost:5173` → `localhost:8000` |

### The Single‑File Component (SFC) Preview

Here’s how our product viewer will look as a `.vue` component in Part 5:

```vue
<template>
  <div>
    <h1>Product Viewer</h1>
    <div v-if="loading">Loading...</div>
    <table v-else>
      <tr v-for="p in products" :key="p.id">
        <td>{{ p.name }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  data() { return { products: [], loading: true } },
  async created() { await this.loadProducts() },
  methods: {
    async loadProducts() {
      const res = await fetch('/api/products')
      this.products = (await res.json()).products
      this.loading = false
    }
  }
}
</script>

<style scoped>
  h1 { color: #333; }
</style>
```

The concepts (`data`, `created`, `methods`, `v-for`, `{{ }}`) are identical.

---

## Step 11: Challenges (Try It Yourself)

These are optional but highly recommended to solidify your understanding.

### Challenge 1: Highlight Low‑Stock Items in Red

**Task:** Make stock numbers turn red when stock < 5.

**Hint:** In the final complete file above, we’ve already included the `low-stock` class in the `<style>` block. Add `:class="{ 'low-stock': p.stock < 5 }"` to the `<td>` that shows stock:

```html
<td :class="{ 'low-stock': p.stock < 5 }">{{ p.stock }}</td>
```

After adding, your table will show low‑stock items in bold red. (The complete file already contains this; try removing it and adding it back to see the effect.)

### Challenge 2: Add a Delete Button

**Task:** Add a delete column. Clicking “Delete” should remove the product and refresh the list.

**Backend preparation** – add to `app/api/products_api.py`:

```python
@router.delete("/{product_id}")
async def delete_product_api(request: Request, product_id: int, db: Session = Depends(get_db)):
    if not request.session.get("admin_id"):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
```

**Frontend** – add a new `<th>Actions</th>` column and a delete button inside the `<tr>`:

```html
<td><button @click="deleteProduct(p.id)">Delete</button></td>
```

Add the method:

```javascript
async deleteProduct(id) {
  if (!confirm('Delete this product?')) return
  await fetch(`/api/products/${id}`, { method: 'DELETE' })
  this.loadProducts()  // refresh the list
}
```

Now you can delete products from the UI — the list updates instantly.

### Challenge 3: Implement Real‑Time Search

**Task:** Use the `search` text to filter the products shown on the current page. You can either filter on the frontend (using a computed property) or send the search term to a new API parameter. Try the frontend approach first: create a `computed` property that filters `this.products` by the search string.

---

## Debugging & Common Pitfalls

- **“Not authenticated” error in console:** Ensure your backend is running, the login route is registered, and you’re using the correct credentials (`admin` / `admin123`). Check that cookies aren’t blocked (browser settings).
- **Blank table with no errors:** Open the Network tab. Does the `/api/products` request return 200? If it shows 401, your login might have failed silently. Add `console.log('Logged in')` after `await this.login()` to trace.
- **Vue not updating:** Make sure you’re using `this.products = ...` inside methods, not `products = ...`. Vue needs the `this` context to detect changes.
- **Styles not applied:** Verify that your `<style>` block is inside `<head>` and that class names match exactly.

---

## Summary

### What Changed?

| Before (Part 4) | After (Part 4.5) |
|---|---|
| Server renders HTML with Jinja2 | JSON API + Vue.js renders HTML in browser |
| Full page reload on every click | Instant UI updates, no reload |
| Login via HTML form submission | Login via `fetch()` + JSON |
| State lives on the server | State lives in Vue’s `data()` |
| Templates in `app/templates/` | Templates in `{{ }}` and directives in HTML |

### Key Takeaways

1. **Vue.js is just JavaScript** – it runs in the browser. The server is a data provider.  
2. **`data()` defines reactive state** – change it, and the DOM updates automatically.  
3. **Directives (`v-for`, `v-if`, `v-model`, `@click`, `:class`)** extend HTML with logic.  
4. **`fetch()` is the bridge** between browser and server.  
5. **No page reloads = better UX** – the browser never navigates away.

### Next: Part 5

Open `full-crud-from-scratch-part5.md`. You’ll:
- Move to a proper Vue project with build tools
- Add Vue Router for multi‑page navigation
- Add Pydantic schemas for request/response validation
- Build a full CRUD SPA: Products, Categories, Customers, Orders

Every Vue concept you learned here (`{{ }}`, `v-for`, `v-if`, `v-model`, `@click`, `:class`, `created()`, `methods`) works exactly the same way in Part 5. Only the project structure changes.

