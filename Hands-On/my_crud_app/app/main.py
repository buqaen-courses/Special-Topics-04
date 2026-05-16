from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.routes.items import router as item_router
from fastapi.templating import Jinja2Templates

import json
import os

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
    items = load_items()
    total = len(items)
    offers = [i for i in items if i.get("is_offer", False)]
    offers_count = len(offers)
    regular_count = total - offers_count
    prices = [i["price"] for i in items if "price" in i]
    total_value = sum(prices) if prices else 0
    avg_price = total_value / total if total > 0 else 0
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    offers_pct = (offers_count / total * 100) if total > 0 else 0

    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={
            "total_items": total,
            "offers_count": offers_count,
            "regular_count": regular_count,
            "total_value": total_value,
            "avg_price": avg_price,
            "min_price": min_price,
            "max_price": max_price,
            "offers_pct": offers_pct
        }
    )