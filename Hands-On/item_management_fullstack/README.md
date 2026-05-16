# Workshop 5 — Full-Stack: REST API + Vue.js SPA

Teaches separating frontend from backend. The backend exposes JSON REST API endpoints (GET/POST/PUT/PATCH/DELETE) with Pydantic schemas. The frontend is a Vue 3 SPA with Vue Router, no page reloads.

## How to run (two terminals)

### Terminal 1 — Backend

```bash
cd item_management_fullstack/backend

# Install deps
pip install -r requirements.txt

# Seed database (first time only)
python seed.py

# Start API server
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend

```bash
cd item_management_fullstack/frontend

# Install deps (first time only)
npm install

# Start dev server (proxies /api → localhost:8000)
npm run dev
```

### Open in browser
```
http://localhost:5173
Login: admin / admin123
```

## Architecture

```
┌──────────────────┐   JSON/HTTP    ┌──────────────┐   SQL    ┌────────┐
│  Vue.js SPA      │ ←───────────→ │  FastAPI API  │ ←─────→ │ SQLite │
│  localhost:5173   │   REST calls   │  localhost:8000 │         │  DB    │
└──────────────────┘               └──────────────┘         └────────┘
```

## Backend API endpoints (24 total)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/login` | Login (returns session cookie) |
| `GET` | `/api/auth/me` | Check authentication |
| `POST` | `/api/auth/logout` | Logout |
| `GET` | `/api/dashboard` | Aggregate stats |
| `GET/POST/PUT/PATCH/DELETE` | `/api/products[/{id}]` | Products CRUD |
| `GET/POST/PUT/PATCH/DELETE` | `/api/categories[/{id}]` | Categories CRUD |
| `GET/POST/PUT/PATCH/DELETE` | `/api/customers[/{id}]` | Customers CRUD |
| `GET/POST` | `/api/orders[/{id}]` | Orders list/create/detail |
| `PATCH` | `/api/orders/{id}/status` | Update order status |

The original HTML template routes still work at `http://localhost:8000/`.

## Frontend structure

| File | Purpose |
|------|---------|
| `src/api.js` | Unified fetch client with cookie auth |
| `src/router.js` | 15 routes with `beforeEach` auth guard |
| `src/views/Login.vue` | Login form, POSTs to `/api/auth/login` |
| `src/views/Dashboard.vue` | Stats cards + recent orders table |
| `src/views/Products.vue` | List with sort/search/pagination |
| `src/views/ProductForm.vue` | Create/edit (dual-purpose, category dropdown) |
| `src/views/Categories.vue` | List with product count |
| `src/views/Customers.vue` | List with order count |
| `src/views/Orders.vue` | Orders list |
| `src/views/OrderDetail.vue` | Line items + status update |
| `src/views/OrderCreate.vue` | Dynamic JS-powered line items |

## Reference

Full walkthrough: `full-crud-from-scratch-part5.md` (in the parent directory)
