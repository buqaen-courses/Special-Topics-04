from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.routes.items import router as item_router
from fastapi.templating import Jinja2Templates

from app.db import init_db, get_connection, dict_from_row

# Initialise the database on startup (creates table + seeds data)
init_db()

app = FastAPI(title="Items CRUD - Step by Step (SQLite)")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(item_router, prefix="/items")

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
            "offers_pct": offers_pct,
        },
    )
