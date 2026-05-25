# Workshop 5: Full‑Stack Apps — REST API + Vue.js Frontend

## Introduction: The Full‑Stack Architecture

In Workshops 1–4 you built a **monolithic** application where the backend rendered HTML
templates directly. The server did everything: query the database, generate HTML, and
send it to the browser.

In the real world, modern applications split into **two separate projects**:

```
┌─────────────────────┐         HTTP/JSON         ┌─────────────────────┐
│                     │ ◄──────────────────────►  │                     │
│   Vue.js Frontend   │      REST API calls        │   FastAPI Backend   │
│   (port 5173)       │                            │   (port 8000)       │
│                     │     GET /api/products      │                     │
│   Pure JavaScript   │     POST /api/orders       │   Python + SQLAlch  │
│   No page reloads   │     DELETE /api/products   │   Returns JSON      │
│                     │     PATCH /api/...          │   No HTML rendered  │
└─────────────────────┘                            └─────────────────────┘
```

### Why Separate Frontend and Backend?

| Reason | Monolith (Part 4) | Full‑Stack (Part 5) |
|--------|-------------------|---------------------|
| **Rendering** | Server renders HTML templates | Browser renders Vue components |
| **Data format** | HTML mixed with Jinja2 | Pure JSON over HTTP |
| **Navigation** | Full page reloads on every click | Instant navigation (SPA) |
| **State** | Server stores session | Browser stores state in Vue |
| **Reusability** | Backend tied to HTML | Backend serves any client (web, mobile, CLI) |
| **Deployment** | One server to deploy | Backend + static files (or CDN) |
| **Team split** | Full‑stack dev needed | Frontend + Backend teams can work independently |

### What Changed from Part 4?

The **backend** now has a single type of route:

1. **JSON API routes** — return JSON data: `/api/products`

The HTML template routes from Part 4 have been removed — the backend is a pure API server.
The root `/` now redirects to the password‑protected Swagger UI at `/docs`.

The **frontend** is a brand‑new Vue.js SPA that talks only to the JSON API.

### REST API — The Language of the Web

REST (Representational State Transfer) uses standard HTTP methods as verbs:

| HTTP Method | Meaning | Example |
|-------------|---------|---------|
| `GET` | Read/retrieve | `GET /api/products` |
| `POST` | Create | `POST /api/products` (send JSON body) |
| `PUT` | Replace (full update) | `PUT /api/products/1` (send all fields) |
| `PATCH` | Partial update | `PATCH /api/products/1` (send only changed fields) |
| `DELETE` | Remove | `DELETE /api/products/1` |

Each endpoint returns JSON with appropriate HTTP status codes:
- `200 OK` — success
- `201 Created` — resource created
- `400 Bad Request` — invalid input
- `401 Unauthorized` — not logged in
- `404 Not Found` — resource doesn't exist

### What You Will Build

1. **RESTful API** with all CRUD endpoints for Products, Categories, Customers, Orders
2. **Pydantic schemas** for request validation and response serialization
3. **Vue.js 3 SPA** with Vue Router and no page reloads
4. **Proxy setup** so frontend and backend communicate seamlessly
5. **Full‑stack workflow** — two terminals, two servers, one application

---

## Step 0: Project Structure

**Goal:** Set up the two‑folder layout that separates backend and frontend.  
**Mental model:** The backend folder is a pure data server; the frontend folder is a separate app that speaks to it.

### 0.1 Create the Full‑Stack Folder

```
item_management_fullstack/
├── backend/                    # FastAPI + SQLAlchemy (copied from Part 4)
│   ├── app/
│   │   ├── api/                # NEW: JSON API routes
│   │   │   ├── auth_api.py
│   │   │   ├── dashboard_api.py
│   │   │   ├── products_api.py
│   │   │   ├── categories_api.py
│   │   │   ├── customers_api.py
│   │   │   └── orders_api.py
│   │   ├── schemas/            # NEW: Pydantic request/response models
│   │   │   ├── auth.py
│   │   │   ├── product.py
│   │   │   ├── category.py
│   │   │   ├── customer.py
│   │   │   └── order.py
│   │   ├── models/             # SQLAlchemy models (from Part 4)
│   │   ├── static/             # CSS, fonts
│   │   ├── database.py         # SQLAlchemy setup
│   │   └── main.py             # CORS + all routers
│   ├── seed.py
│   └── requirements.txt
├── frontend/                   # NEW: Vue.js 3 SPA
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── style.css
│       ├── api.js              # API client (fetch wrapper)
│       ├── router.js           # Vue Router config
│       └── views/
│           ├── Login.vue
│           ├── Dashboard.vue
│           ├── Products.vue
│           ├── ProductForm.vue
│           ├── Categories.vue
│           ├── CategoryForm.vue
│           ├── Customers.vue
│           ├── CustomerForm.vue
│           ├── Orders.vue
│           ├── OrderDetail.vue
│           └── OrderCreate.vue
└── full-crud-from-scratch-part5.md
```

### 0.2 Set Up the Backend

Copy your entire `item_management_sqlalchemy` folder into `backend/`:

```bash
cp -r item_management_sqlalchemy item_management_fullstack/backend
cd item_management_fullstack/backend
```

Add the new `app/api/` and `app/schemas/` directories:

```bash
mkdir -p app/api app/schemas
touch app/api/__init__.py app/schemas/__init__.py
```

Remove the HTML template routes that are no longer needed — the backend will serve
only JSON API endpoints:

```bash
rm -rf app/routes app/templates
```

### 0.3 Create the Frontend

```bash
cd ../frontend
npm init -y
npm install vue@3 vue-router@4
npm install -D vite@5 @vitejs/plugin-vue@5
```

**Checkpoint:** You now have two completely separate codebases that will talk over HTTP.

---

## Step 1: Pydantic Schemas — The Contract Layer

**Goal:** Define exactly what data the API expects and returns, with automatic validation.  
**Mental model:** A schema is like a typed interface or a contract — if the client breaks it, the server rejects the request immediately.

### Why Schemas?

Without schemas (Part 4):
```python
@app.post("/api/products")
async def create_product(name: str = Form(...), price: float = Form(...)):
    # No validation, no documentation
    product = Product(name=name, price=price)
```

With schemas (Part 5):
```python
@app.post("/api/products", status_code=201)
async def create_product(body: ProductCreate, db: Session = Depends(get_db)):
    # body is validated automatically by Pydantic
    product = Product(**body.model_dump())
```

### Product Schema (`app/schemas/product.py`)

```python
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str = ""
    price: float
    stock: int = 0
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    """Used for POST — all fields required (except optional ones)."""
    pass

class ProductUpdate(BaseModel):
    """Used for PATCH — all fields optional (only send what changes)."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None

class ProductResponse(ProductBase):
    """Used for GET responses — includes id and category_name."""
    id: int
    category_name: Optional[str] = None

    class Config:
        from_attributes = True  # Allows creating from SQLAlchemy model
```

### Key Pydantic Concepts

**1. `BaseModel` inheritance** — Every schema inherits from Pydantic's `BaseModel`,
which gives automatic validation, serialization, and JSON schema generation.

**2. Type hints = validation** — `name: str` means it must be a string. `price: float`
means it must be a number. FastAPI returns 400 automatically if types mismatch.

**3. `Optional[int]`** — The field can be `None` (null in JSON). Useful for nullable
foreign keys.

**4. `model_dump()`** — Converts the validated Pydantic model to a Python dict, ready
for SQLAlchemy: `Product(**body.model_dump())`.

**5. `model_dump(exclude_unset=True)`** — For PATCH: only include fields the client
actually sent, not the defaults.

**6. `from_attributes = True`** — Allows `ProductResponse.model_validate(product)` to
read attributes from a SQLAlchemy model object.

### Comparison: With and Without Schemas

| Aspect | Without Schemas (Part 4) | With Schemas (Part 5) |
|--------|-------------------------|----------------------|
| Input validation | Manual form parsing | Automatic (type + constraints) |
| Error messages | Generic 422 | Detailed field-level errors |
| API documentation | None | Auto‑generated OpenAPI docs |
| IDE autocomplete | None | Full type hints |
| Refactoring safety | Break silently | Typesafe changes |

### Try it Yourself

After creating the schema, attempt to send a `POST` to `/api/products` with a missing `price` field. You'll get a clear 422 error. That's Pydantic protecting your database from bad data.

**Checkpoint:** You now have a contract for your API. Every endpoint will use these schemas to validate incoming data and format outgoing data.

---

## Step 2: RESTful API Routes

**Goal:** Build full CRUD endpoints that follow REST conventions.  
**Mental model:** Each entity (Product, Category, etc.) gets its own `router` with the same six operations: list, get, create, update full (PUT), update partial (PATCH), delete.

### 2.1 Products API (`app/api/products_api.py`)

We'll build the products API step by step, explaining each pattern.

```python
from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/api/products", tags=["Products"])

def require_auth(request: Request):
    if not request.session.get("admin_id"):
        return False
    return True

def product_to_response(p: Product) -> ProductResponse:
    return ProductResponse(
        id=p.id, name=p.name, description=p.description or "",
        price=p.price, stock=p.stock, category_id=p.category_id,
        category_name=p.category.name if p.category else None,
    )

@router.get("")
async def list_products(request: Request, sort: str = Query("default"),
                        page: int = Query(1, ge=1), q: str = Query(""),
                        min_price: float = Query(None),
                        max_price: float = Query(None),
                        category_id: int = Query(None),
                        per_page: int = Query(10, ge=1, le=100),
                        db: Session = Depends(get_db)):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

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

    order_map = {"name": Product.name, "price": Product.price,
                 "stock": Product.stock}
    query = query.order_by(order_map.get(sort, Product.id))

    total = query.count()
    products = query.offset((page-1)*per_page).limit(per_page).all()

    return {
        "total": total, "page": page, "per_page": per_page,
        "total_pages": max(1, (total + per_page - 1) // per_page),
        "products": [product_to_response(p) for p in products],
        "categories": [{"id": c.id, "name": c.name}
                       for c in db.query(Category).all()],
    }

@router.get("/{product_id}")
async def get_product(request: Request, product_id: int,
                      db: Session = Depends(get_db)):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_response(product)

@router.post("", status_code=201)
async def create_product(request: Request, body: ProductCreate,
                         db: Session = Depends(get_db)):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = Product(**body.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product_to_response(product)

@router.put("/{product_id}")
async def update_product(request: Request, product_id: int,
                         body: ProductCreate, db: Session = Depends(get_db)):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, val in body.model_dump().items():
        setattr(product, key, val)
    db.commit()
    db.refresh(product)
    return product_to_response(product)

@router.patch("/{product_id}")
async def patch_product(request: Request, product_id: int,
                        body: ProductUpdate, db: Session = Depends(get_db)):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, val in body.model_dump(exclude_unset=True).items():
        setattr(product, key, val)
    db.commit()
    db.refresh(product)
    return product_to_response(product)

@router.delete("/{product_id}")
async def delete_product(request: Request, product_id: int,
                         db: Session = Depends(get_db)):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
```

### The API Design Pattern

Every entity follows the same pattern:

| Method | Endpoint | Purpose | Status Code |
|--------|----------|---------|-------------|
| `GET` | `/api/products` | List (with filters, sort, pagination) | 200 |
| `GET` | `/api/products/{id}` | Get single product | 200 |
| `POST` | `/api/products` | Create new product | 201 |
| `PUT` | `/api/products/{id}` | Full update (replace all fields) | 200 |
| `PATCH` | `/api/products/{id}` | Partial update (only sent fields) | 200 |
| `DELETE` | `/api/products/{id}` | Delete product | 200 |

### PUT vs PATCH — When to Use Each

| | PUT | PATCH |
|---|-----|-------|
| **Body schema** | `ProductCreate` (all required) | `ProductUpdate` (all optional) |
| **What it means** | “Make the resource look exactly like this” | “Apply these changes to the resource” |
| **Missing fields** | Set to defaults (e.g., stock = 0) | Left unchanged |
| **When to use** | Full form submission | Quick edits, status changes |

**Try it:** After creating a product, send a PATCH with only `{“price”: 42.0}`. Only the price changes; all other fields stay untouched.

### CORS — Cross‑Origin Resource Sharing

Since the frontend runs on `http://localhost:5173` and the backend on
`http://localhost:8000`, browsers block cross‑origin requests by default. We add CORS
middleware to allow it:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,   # Needed for session cookies
    allow_methods=["*"],      # Allow all HTTP methods
    allow_headers=["*"],      # Allow all headers
)
```

### Backend main.py — Wiring Everything Together

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import hashlib
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Admin
from app.api import auth_api, dashboard_api, products_api,
                   categories_api, customers_api, orders_api

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop Manager — Full‑Stack Edition",
              docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key="change-this-secret-key")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"],
                   allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_api.router)
app.include_router(dashboard_api.router)
app.include_router(products_api.router)
app.include_router(categories_api.router)
app.include_router(customers_api.router)
app.include_router(orders_api.router)

security = HTTPBasic(auto_error=False)

def verify_admin(credentials, db):
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated",
                            headers={"WWW-Authenticate": "Basic"})
    pw_hash = hashlib.sha256(credentials.password.encode()).hexdigest()
    admin = db.query(Admin).filter(
        Admin.username == credentials.username,
        Admin.password_hash == pw_hash,
    ).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Basic"})

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    verify_admin(credentials, db)
    return get_swagger_ui_html(openapi_url="/openapi.json",
                               title="Shop Manager API")

@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    verify_admin(credentials, db)
    return app.openapi()

@app.get("/")
async def root():
    return RedirectResponse("/docs")
```

> **Git commit:** `git add -A && git commit -m "Step 2: Add RESTful API routes with Pydantic schemas, CORS middleware, and password-protected Swagger docs"`

**Checkpoint:** Your backend now speaks pure JSON. The HTML template routes have been removed — the backend is a pure API server. Visit `http://localhost:8000/` — it redirects to `/docs`, which is protected by HTTP Basic Auth (use the same `admin` / `admin123` credentials from the database).

---

## Step 3: Vite Proxy — Connecting Frontend to Backend

**Goal:** Make the Vue dev server and the FastAPI backend work together as if they're the same origin.  
**Mental model:** The Vite dev server acts as a middleman that forwards API calls to the backend, so the browser never sees a cross‑origin request.

### Create `frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
      '/auth': { target: 'http://localhost:8000', changeOrigin: true },
    },
  },
})
```

### How the Proxy Works

```
Browser                  Vite Dev Server              Backend
  │                          │                          │
  │  fetch('/api/products')  │                          │
  │ ──────────────────────►  │                          │
  │                          │  http://localhost:8000    │
  │                          │ ──────────────────────►  │
  │                          │                          │
  │                          │  ◄────────────────────── │
  │  ◄────────────────────── │                          │
  │                          │                          │
```

The browser sees the request as same‑origin (both from `localhost:5173`), so cookies
work and no CORS errors occur in development.

### Why Two Servers?

One of the most important concepts in modern web development:

```
┌─────────────────────────────────────────────────────────────┐
│                     Development Mode                         │
│                                                             │
│  Terminal 1:    python -m uvicorn backend.app.main:app      │
│                 → Backend API at http://localhost:8000       │
│                                                             │
│  Terminal 2:    npm run dev (in frontend/)                  │
│                 → Dev server at http://localhost:5173        │
│                                                             │
│  Browser:       Open http://localhost:5173                   │
│                 → Vite serves the Vue app                    │
│                 → API calls proxied to port 8000             │
└─────────────────────────────────────────────────────────────┘
```

**Checkpoint:** You now understand why we have two terminals and how the frontend can talk to the backend without CORS headaches.

---

## Step 4: The API Client (Vue Side)

**Goal:** Create a single, reusable module for all HTTP calls.  
**Mental model:** This is your "data layer". Every component only imports `api` and calls methods like `api.products()`. No scattered `fetch()` calls.

### `frontend/src/api.js`

```javascript
const BASE = ''

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    credentials: 'include',  // Send session cookies
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

export default {
  // Auth
  login(username, password) {
    return request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
  },
  logout() {
    return request('/api/auth/logout', { method: 'POST' })
  },
  me() {
    return request('/api/auth/me')
  },

  // Dashboard
  dashboard() {
    return request('/api/dashboard')
  },

  // Products — all 6 CRUD operations
  products(params = {}) {
    return request(`/api/products?${new URLSearchParams(params)}`)
  },
  product(id) {
    return request(`/api/products/${id}`)
  },
  createProduct(data) {
    return request('/api/products', { method: 'POST', body: JSON.stringify(data) })
  },
  updateProduct(id, data) {
    return request(`/api/products/${id}`, { method: 'PUT', body: JSON.stringify(data) })
  },
  patchProduct(id, data) {
    return request(`/api/products/${id}`, { method: 'PATCH', body: JSON.stringify(data) })
  },
  deleteProduct(id) {
    return request(`/api/products/${id}`, { method: 'DELETE' })
  },

  // Categories, Customers, Orders — same pattern
  categories(params) { return request(`/api/categories?${new URLSearchParams(params)}`) },
  createCategory(data) { return request('/api/categories', { method: 'POST', body: JSON.stringify(data) }) },
  updateCategory(id, data) { return request(`/api/categories/${id}`, { method: 'PUT', body: JSON.stringify(data) }) },
  deleteCategory(id) { return request(`/api/categories/${id}`, { method: 'DELETE' }) },

  customers(params) { return request(`/api/customers?${new URLSearchParams(params)}`) },
  createCustomer(data) { return request('/api/customers', { method: 'POST', body: JSON.stringify(data) }) },
  updateCustomer(id, data) { return request(`/api/customers/${id}`, { method: 'PUT', body: JSON.stringify(data) }) },
  deleteCustomer(id) { return request(`/api/customers/${id}`, { method: 'DELETE' }) },

  orders(params) { return request(`/api/orders?${new URLSearchParams(params)}`) },
  order(id) { return request(`/api/orders/${id}`) },
  createOrder(data) { return request('/api/orders', { method: 'POST', body: JSON.stringify(data) }) },
  updateOrderStatus(id, status) {
    return request(`/api/orders/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    })
  },
}
```

### Key Concepts

**1. `credentials: 'include'`** — This tells the browser to send session cookies with
every request. Without this, the backend sees every request as unauthenticated.

**2. Single `request()` function** — Centralizes error handling. Every API call either
returns data or throws an error with a meaningful message. Components just `try/catch`.

**3. `URLSearchParams`** — Converts a JS object like `{ page: 1, sort: 'name' }` into
`?page=1&sort=name`.

**Checkpoint:** You've encapsulated all backend communication. Your Vue components will never call `fetch` directly.

---

## Step 5: Vue Router with Auth Guard

**Goal:** Set up client‑side navigation that protects pages behind login.  
**Mental model:** Vue Router intercepts URL changes, loads the right component, and prevents access to pages if the user isn't authenticated. It's a UX convenience — security still lives on the backend.

### `frontend/src/router.js`

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import Dashboard from './views/Dashboard.vue'
import Products from './views/Products.vue'
import ProductForm from './views/ProductForm.vue'
import Categories from './views/Categories.vue'
import CategoryForm from './views/CategoryForm.vue'
import Customers from './views/Customers.vue'
import CustomerForm from './views/CustomerForm.vue'
import Orders from './views/Orders.vue'
import OrderDetail from './views/OrderDetail.vue'
import OrderCreate from './views/OrderCreate.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/products', component: Products, meta: { requiresAuth: true } },
  { path: '/products/new', component: ProductForm, meta: { requiresAuth: true } },
  { path: '/products/:id/edit', component: ProductForm, meta: { requiresAuth: true } },
  { path: '/categories', component: Categories, meta: { requiresAuth: true } },
  { path: '/categories/new', component: CategoryForm, meta: { requiresAuth: true } },
  { path: '/categories/:id/edit', component: CategoryForm, meta: { requiresAuth: true } },
  { path: '/customers', component: Customers, meta: { requiresAuth: true } },
  { path: '/customers/new', component: CustomerForm, meta: { requiresAuth: true } },
  { path: '/customers/:id/edit', component: CustomerForm, meta: { requiresAuth: true } },
  { path: '/orders', component: Orders, meta: { requiresAuth: true } },
  { path: '/orders/new', component: OrderCreate, meta: { requiresAuth: true } },
  { path: '/orders/:id', component: OrderDetail, meta: { requiresAuth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

// Navigation guard — redirect to /login if not authenticated
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const res = await fetch('/api/auth/me', { credentials: 'include' })
      if (!res.ok) return next('/login')
    } catch {
      return next('/login')
    }
  }
  next()
})

export default router
```

### The Navigation Guard

The `beforeEach` hook runs before every route change. If the page requires auth, it
calls `/api/auth/me`. If the response is not 200, the user is redirected to `/login`.

This is the **frontend auth guard** — it's not security (the backend still enforces
auth on every API call). It's a UX convenience that prevents showing blank pages.

### Vue Route Parameter Binding

URL parameters like `/products/42/edit` are captured by `:id` in the route pattern.
The component accesses them via:

```javascript
this.$route.params.id  // "42"
```

**Checkpoint:** Your app now has multiple “pages” without any actual page reloads. Typing `/products` in the browser instantly shows the products view.

---

## Step 6: Vue Components — The SPA Pattern

**Goal:** Build the actual views that bring your data to life.  
**Mental model:** Every view follows a lifecycle: mount → fetch data → render → user interacts → fetch again. Vue's reactivity makes this seamless.

### 6.1 Login View

```vue
<template>
  <div class="card" style="max-width:400px; margin:3rem auto;">
    <div class="card-header"><i class="fas fa-lock"></i> Admin Login</div>
    <div class="card-body">
      <div v-if="error" class="error-msg">{{ error }}</div>
      <form @submit.prevent="doLogin">
        <div class="form-group">
          <label><i class="fas fa-user"></i> Username</label>
          <input v-model="username" type="text" required autofocus />
        </div>
        <div class="form-group">
          <label><i class="fas fa-key"></i> Password</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%;">
          <i class="fas fa-sign-in-alt"></i> Login
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() { return { username: '', password: '', error: null } },
  methods: {
    async doLogin() {
      try {
        await api.login(this.username, this.password)
        this.$router.push('/')
      } catch (e) { this.error = e.message }
    },
  },
}
</script>
```

**Key concepts:**
- `@submit.prevent` — Prevents the form's default page‑reload behavior
- `v-model` — Two‑way data binding (input ↔ data property)
- `this.$router.push('/')` — Navigates to dashboard after login (no page reload!)

### 6.2 Products List View

```vue
<template>
  <div>
    <h2><i class="fas fa-box"></i> Products</h2>
    <div class="card">
      <div class="card-header"><i class="fas fa-filter"></i> Search</div>
      <div class="card-body">
        <div class="d-flex gap-2" style="flex-wrap:wrap;">
          <div style="flex:2;"><label>Search</label><input v-model="filters.q" /></div>
          <div style="flex:1;"><label>Min price</label><input v-model.number="filters.min_price" type="number" /></div>
          <div style="flex:1;"><label>Max price</label><input v-model.number="filters.max_price" type="number" /></div>
          <div style="align-self:flex-end;">
            <button class="btn btn-primary" @click="load"><i class="fas fa-search"></i> Search</button>
          </div>
        </div>
      </div>
    </div>

    <div class="sort-controls">
      <span>Sort by:</span>
      <button v-for="s in sortOptions" :key="s.key" class="btn btn-sm"
              :class="filters.sort===s.key?'btn-active':''"
              @click="filters.sort=s.key; load()">{{ s.label }}</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="card">
      <div class="card-header">Products ({{ total }})</div>
      <div class="card-body" style="padding:0;">
        <table class="table">
          <thead>
            <tr><th>ID</th><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th>Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="p in products" :key="p.id">
              <td>{{ p.id }}</td><td>{{ p.name }}</td>
              <td>{{ p.category_name || '—' }}</td>
              <td>${{ p.price.toFixed(2) }}</td>
              <td :style="{ color: p.stock<5?'#d62828':'inherit' }">{{ p.stock }}</td>
              <td>
                <router-link :to="'/products/'+p.id+'/edit'" class="btn btn-warning btn-sm">Edit</router-link>
                <button class="btn btn-danger btn-sm" @click="doDelete(p)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button :disabled="page<=1" class="btn btn-sm" @click="goPage(page-1)">← Prev</button>
      <span v-for="n in totalPages" :key="n" class="btn btn-sm"
            :class="n===page?'btn-active':''" @click="goPage(n)">{{ n }}</span>
      <button :disabled="page>=totalPages" class="btn btn-sm" @click="goPage(page+1)">Next →</button>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() {
    return {
      products: [], total: 0, page: 1, totalPages: 1, loading: true,
      filters: { sort: 'default', q: '', min_price: null, max_price: null },
      sortOptions: [
        { key:'default', label:'Default' }, { key:'name', label:'Name' },
        { key:'price', label:'Price' }, { key:'stock', label:'Stock' },
      ],
    }
  },
  async created() { await this.load() },
  methods: {
    async load() {
      this.loading = true
      try {
        const params = { sort: this.filters.sort, page: this.page }
        if (this.filters.q) params.q = this.filters.q
        const res = await api.products(params)
        this.products = res.products
        this.total = res.total
        this.totalPages = res.total_pages
      } catch (e) { alert(e.message) }
      finally { this.loading = false }
    },
    goPage(n) { this.page = n; this.load() },
    async doDelete(p) {
      if (!confirm(`Delete "${p.name}"?`)) return
      await api.deleteProduct(p.id)
      this.load()
    },
  },
}
</script>
```

### Key Vue Concepts

| Concept | What It Does | Example |
|---------|-------------|---------|
| `v-for` | Loops over arrays, renders elements | `<tr v-for="p in products">` |
| `v-if` / `v-else` | Conditional rendering | `<div v-if="loading">Loading...</div>` |
| `v-model` | Two‑way data binding | `<input v-model="filters.q" />` |
| `v-model.number` | Auto‑convert to number | `<input v-model.number="price" type="number" />` |
| `@click` | Event handler | `<button @click="load()">Search</button>` |
| `@submit.prevent` | Form submit handler (no reload) | `<form @submit.prevent="doLogin">` |
| `:to` | Router link binding | `<router-link :to="'/products/'+p.id">` |
| `:class` | Dynamic CSS classes | `:class="sort==='name'?'btn-active':''"` |
| `:style` | Dynamic inline styles | `:style="{ color: p.stock<5?'red':'inherit' }"` |
| `{{ }}` | Text interpolation | `{{ p.name }}` |

### 6.3 Product Form View (Create + Edit)

```vue
<template>
  <div class="card" style="max-width:600px; margin:0 auto;">
    <div class="card-header">{{ isEdit ? 'Edit' : 'Add' }} Product</div>
    <div class="card-body">
      <div v-if="error" class="error-msg">{{ error }}</div>
      <form @submit.prevent="doSave">
        <div class="form-group">
          <label>Name</label>
          <input v-model="form.name" required />
        </div>
        <div class="form-group">
          <label>Price</label>
          <input v-model.number="form.price" type="number" step="0.01" required />
        </div>
        <div class="form-group">
          <label>Category</label>
          <select v-model.number="form.category_id">
            <option :value="null">— No category —</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary">
          {{ isEdit ? 'Update' : 'Create' }}
        </button>
        <router-link to="/products" class="btn btn-secondary">Cancel</router-link>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() {
    return {
      isEdit: false, error: null,
      form: { name: '', description: '', price: 0, stock: 0, category_id: null },
      categories: [],
    }
  },
  async created() {
    const id = this.$route.params.id
    this.isEdit = !!id
    const catRes = await api.categories({ per_page: 100 })
    this.categories = catRes.categories
    if (id) {
      const p = await api.product(id)
      this.form = { name: p.name, description: p.description, price: p.price,
                    stock: p.stock, category_id: p.category_id }
    }
  },
  methods: {
    async doSave() {
      try {
        if (this.isEdit) await api.updateProduct(this.$route.params.id, this.form)
        else await api.createProduct(this.form)
        this.$router.push('/products')
      } catch (e) { this.error = e.message }
    },
  },
}
</script>
```

**The dual‑purpose pattern:** The same component handles both Create and Edit. It checks `this.$route.params.id` — if there's an ID, it's editing; otherwise, it's creating. This DRY pattern saves you from writing two nearly identical forms.

### 6.4 Order Create View (Dynamic Line Items)

The order creation form is the most complex component:

```vue
<template>
  <div>
    <h2>Create New Order</h2>

    <div class="card">
      <div class="card-header">Customer</div>
      <div class="card-body">
        <select v-model="customerId" style="max-width:400px;">
          <option :value="null">— Choose customer —</option>
          <option v-for="c in customers" :key="c.id" :value="c.id">
            {{ c.name }} ({{ c.email }})
          </option>
        </select>
      </div>
    </div>

    <div class="card">
      <div class="card-header">Items</div>
      <div class="card-body">
        <div v-for="(item, idx) in items" :key="idx"
             class="d-flex gap-2" style="margin-bottom:0.8rem;align-items:end;">
          <div style="flex:2;">
            <label>Product</label>
            <select v-model="item.product_id">
              <option :value="null">— Select —</option>
              <option v-for="p in products" :key="p.id" :value="p.id">
                {{ p.name }} (${{ p.price.toFixed(2) }})
              </option>
            </select>
          </div>
          <div style="flex:1;">
            <label>Qty</label>
            <input v-model.number="item.quantity" type="number" min="1" />
          </div>
          <div style="align-self:flex-end;">
            <button class="btn btn-danger btn-sm" @click="items.splice(idx, 1)"
                    v-if="items.length > 1">×</button>
          </div>
        </div>
        <button class="btn btn-secondary btn-sm" @click="items.push({product_id:null, quantity:1})">
          + Add item
        </button>
      </div>
    </div>

    <button class="btn btn-primary" @click="doCreate">Create Order</button>
  </div>
</template>
```

**Dynamic line items concept:** The `items` array starts with one empty item. When "Add item" is clicked, a new object is pushed to the array. Vue's reactivity automatically renders the new row. When "×" is clicked, `splice()` removes it.

**Checkpoint:** You've built all the major UI patterns — lists, forms, pagination, sorting, dynamic arrays. The entire frontend is now a living, breathing application.

---

## Step 7: Running the Full‑Stack Application

**Goal:** Launch both servers and see your full‑stack app in action.

### 7.1 Start Both Servers

**Terminal 1 — Backend:**
```bash
cd item_management_fullstack/backend
python seed.py        # Only first time
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd item_management_fullstack/frontend
npm run dev           # Starts at http://localhost:5173
```

### 7.1a Password‑Protected Swagger UI

The built‑in FastAPI docs (`/docs`) are disabled (`docs_url=None`) and replaced with
a custom endpoint protected by HTTP Basic Auth (line 61 of `main.py`):

```
Browser → GET /docs → Basic Auth prompt → verify against Admin table in DB → Swagger UI
```

Credentials match the database: `admin` / `admin123`. On success, you see the full
OpenAPI documentation with all 24 REST endpoints ready to test.

### 7.2 Open the Application

1. Open `http://localhost:5173` in your browser
2. Log in with `admin` / `admin123`
3. Explore the Dashboard, Products, Categories, Customers, and Orders

### 7.3 Verify the API Docs

The backend is now a pure JSON API server — no HTML template routes:

- `http://localhost:8000/` — Redirects to `/docs`
- `http://localhost:8000/docs` — Password‑protected Swagger UI
- `http://localhost:8000/redoc` — Password‑protected ReDoc

Log in to Swagger with the same credentials: `admin` / `admin123`.

The frontend SPA:
- `http://localhost:5173/` — Vue‑rendered dashboard
- `http://localhost:5173/products` — Vue‑rendered product list

Both talk to the same database and the same API endpoints.

---

## Step 8: Comparison — Monolith vs SPA

### Data Flow Comparison

**Monolith (Part 4):**
```
Browser → GET /products/landing → Backend queries DB → Backend renders HTML
        → Returns full HTML page → Browser displays it
        → User clicks → Full page reload → Process repeats
```

**SPA (Part 5):**
```
Browser → GET /products → Vue router intercepts → component mounts
        → fetch('/api/products') → Backend returns JSON
        → Vue updates template → Only the table re‑renders
        → User clicks sort → fetch() again → Only data changes
        → NO page reload ever
```

### Code Size Comparison

| Metric | Monolith (Part 4) | Full‑Stack (Part 5) |
|--------|-------------------|---------------------|
| Backend Python files | 15 | 18 (+3 new, -6 removed) |
| Frontend files | Jinja2 templates (12) | Vue SFCs (11) + JS (3) |
| Total lines of code | ~2,000 | ~3,200 |
| API endpoints | 0 (HTML only) | 24 REST endpoints |
| State management | Server session | Browser + session cookie |
| Backend rendering | Jinja2 templates | None (pure JSON API) |

### Learning Progression

| Part | What You Learned | Stack |
|------|-----------------|-------|
| 1 | Python lists + JSON files | Server‑only |
| 2 | Sorting, searching, pagination | Server‑only |
| 3 | SQLite with raw SQL | Server + DB |
| 4 | SQLAlchemy ORM + relationships | Server + DB |
| 5 | REST API + Vue.js SPA | Full‑stack |

---

## Step 9: Complete API Endpoint Reference

### Authentication

| Method | Endpoint | Request Body | Response | Auth Required |
|--------|----------|-------------|----------|---------------|
| `POST` | `/api/auth/login` | `{ username, password }` | `{ success, admin_id }` | No |
| `GET` | `/api/auth/me` | — | `{ id, username }` | Yes |
| `POST` | `/api/auth/logout` | — | `{ success }` | Yes |

### Dashboard

| Method | Endpoint | Response | Auth Required |
|--------|----------|----------|---------------|
| `GET` | `/api/dashboard` | `{ total_products, total_categories, ..., recent_orders[] }` | Yes |

### Products

| Method | Endpoint | Request Body | Response | Auth |
|--------|----------|-------------|----------|------|
| `GET` | `/api/products?sort=&page=&q=&min_price=&max_price=&category_id=` | — | `{ total, products[], categories[] }` | Yes |
| `GET` | `/api/products/{id}` | — | `{ id, name, price, ... }` | Yes |
| `POST` | `/api/products` | `{ name, description?, price, stock?, category_id? }` | Created product | Yes |
| `PUT` | `/api/products/{id}` | `{ name, description, price, stock, category_id }` | Updated product | Yes |
| `PATCH` | `/api/products/{id}` | `{ any_field? }` | Updated product | Yes |
| `DELETE` | `/api/products/{id}` | — | `{ message }` | Yes |

### Categories

| Method | Endpoint | Request Body | Response | Auth |
|--------|----------|-------------|----------|------|
| `GET` | `/api/categories` | — | `{ total, categories[] }` | Yes |
| `GET` | `/api/categories/{id}` | — | `{ id, name, product_count }` | Yes |
| `POST` | `/api/categories` | `{ name, description? }` | Created category | Yes |
| `PUT` | `/api/categories/{id}` | `{ name, description }` | Updated category | Yes |
| `PATCH` | `/api/categories/{id}` | `{ name?, description? }` | Updated category | Yes |
| `DELETE` | `/api/categories/{id}` | — | `{ message }` | Yes |

### Customers

| Method | Endpoint | Request Body | Response | Auth |
|--------|----------|-------------|----------|------|
| `GET` | `/api/customers` | — | `{ total, customers[] }` | Yes |
| `GET` | `/api/customers/{id}` | — | `{ id, name, email, order_count }` | Yes |
| `POST` | `/api/customers` | `{ name, email, phone? }` | Created customer | Yes |
| `PUT` | `/api/customers/{id}` | `{ name, email, phone }` | Updated customer | Yes |
| `PATCH` | `/api/customers/{id}` | `{ name?, email?, phone? }` | Updated customer | Yes |
| `DELETE` | `/api/customers/{id}` | — | `{ message }` | Yes |

### Orders

| Method | Endpoint | Request Body | Response | Auth |
|--------|----------|-------------|----------|------|
| `GET` | `/api/orders` | — | `{ total, orders[] }` | Yes |
| `GET` | `/api/orders/{id}` | — | `{ id, customer_name, items[], ... }` | Yes |
| `POST` | `/api/orders` | `{ customer_id, items: [{product_id, quantity}] }` | Created order | Yes |
| `PATCH` | `/api/orders/{id}/status` | `{ status }` | Updated order | Yes |

---

## Step 10: Testing with curl

You can test the API without the frontend using `curl` or any HTTP client:

```bash
# 1. Login (save session cookie)
curl -c cookies.txt -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 2. Get dashboard
curl -b cookies.txt http://localhost:8000/api/dashboard

# 3. List products
curl -b cookies.txt "http://localhost:8000/api/products?sort=name&page=1"

# 4. Create a product (POST)
curl -b cookies.txt -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"New Widget","price":29.99,"stock":100}'

# 5. Update a product (PUT — all fields)
curl -b cookies.txt -X PUT http://localhost:8000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Widget","description":"Better","price":39.99,"stock":50,"category_id":1}'

# 6. Partial update (PATCH — only price)
curl -b cookies.txt -X PATCH http://localhost:8000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 34.99}'

# 7. Delete a product
curl -b cookies.txt -X DELETE http://localhost:8000/api/products/1

# 8. Create an order
curl -b cookies.txt -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"items":[{"product_id":2,"quantity":3}]}'

# 9. Update order status (PATCH)
curl -b cookies.txt -X PATCH http://localhost:8000/api/orders/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# 10. Logout
curl -b cookies.txt -X POST http://localhost:8000/api/auth/logout
```

---

## Common Pitfalls

### 1. CORS errors in the browser
```
Access to fetch at 'http://localhost:8000/api/products' from origin 'http://localhost:5173'
has been blocked by CORS policy.
```
**Fix:** Make sure the Vite proxy is configured correctly, OR add CORS middleware
with the correct `allow_origins`. The Vite proxy is the simpler approach.

### 2. Session cookies not sent
If you see 401 errors on authenticated endpoints:
**Fix:** Add `credentials: 'include'` to all `fetch()` calls.

### 3. 422 Validation Error
```
{"detail":[{"loc":["body","price"],"msg":"field required"}]}
```
**Fix:** Your Pydantic schema requires a field that you didn't send. Check the
schema definition matches what you're sending.

### 4. PUT vs PATCH confusion
- Use **PUT** when the client wants to replace the entire resource (sends all fields)
- Use **PATCH** when the client wants to modify specific fields (sends only changes)
- If your form always sends all fields, PUT is the right choice

### 5. Vue component not reactive
If you update `this.data` but the template doesn't change:
**Fix:** Make sure you're using Vue's reactive data (declared in `data()`) and not
plain variables. For deep reactivity, use `Vue.set()` or spread operator.

### 6. Nested template expressions
```
v-for="item in order.order_items"
```
**Fix:** Make sure the API response includes `order_items` or `items` (check the
response schema). The field name must match exactly.

---

## What You've Learned in Part 5

| Concept | Before | After |
|---------|--------|-------|
| **Backend** | Renders HTML templates | Returns JSON + Pydantic validation |
| **HTTP methods** | GET/POST only | GET, POST, PUT, PATCH, DELETE |
| **Status codes** | Always 200 | 200, 201, 400, 401, 404 |
| **Frontend** | Jinja2 templates in backend | Vue components in separate project |
| **State** | Full page reloads | Vue SPA, instant navigation |
| **Auth** | Server redirects to login | API returns 401, Vue redirects |
| **Data flow** | Server generates HTML | JSON over HTTP, browser renders |
| **Project structure** | One folder | `backend/` + `frontend/` |

### The Full‑Stack Mindset

A professional web application is never a single piece of code. It's:

```
┌──────────┐    JSON/HTTP    ┌──────────┐    SQL    ┌──────────┐
│          │  ◄────────────►  │          │  ◄──────► │          │
│  Browser │      REST       │   API    │           │ Database │
│ (Vue.js) │                 │ (FastAPI)│           │ (SQLite) │
│          │                 │          │           │          │
└──────────┘                 └──────────┘           └──────────┘
```

Each layer is independent, testable, and replaceable. You can:
- Swap Vue for React, Angular, or a mobile app — the API stays the same
- Swap FastAPI for Django, Express, or Go — the frontend stays the same
- Swap SQLite for PostgreSQL — nothing changes for either frontend or backend

This separation is what makes real‑world applications scalable, maintainable, and
team‑friendly. You're no longer writing “a web app” — you're building a **system of
services** that communicate through well‑defined APIs.