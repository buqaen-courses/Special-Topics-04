from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.routes.items import router as item_router
from fastapi.templating import Jinja2Templates
from app.db import init_db, get_connection, dict_from_row


import json
import os

# Create the table and seed it on first run
init_db()

DATA_FILE = "items.json"

def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

app = FastAPI(title="Items CRUD - Step by Step")

# Serve static files (CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# http://localhost:8000/static/css/custom.css -->> http://localhost:8000/app/static/css/custom.css

# Include the items router (all routes under /items)
app.include_router(item_router, prefix="/items")

# ---------------------------
# Template Engine Setup
# ---------------------------
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