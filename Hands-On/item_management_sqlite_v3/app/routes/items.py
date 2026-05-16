from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
import math
from fastapi.templating import Jinja2Templates
from fastapi import Form, status
from fastapi.responses import RedirectResponse
from fastapi import HTTPException

from app.db import get_connection, dict_from_row

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
ITEMS_PER_PAGE = 5


def load_items():
    """Load all items from SQLite as a list of dicts."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    return [dict_from_row(r) for r in rows]


@router.get("/landing", response_class=HTMLResponse)
async def landing_page(
    request: Request,
    sort: str = Query("default", pattern="^(default|name|price)$"),
    page: int = Query(1, ge=1),
):
    conn = get_connection()

    # Build sort clause
    order = "ORDER BY id ASC"
    if sort == "name":
        order = "ORDER BY name COLLATE NOCASE ASC"
    elif sort == "price":
        order = "ORDER BY price ASC"

    # Count total
    total_items = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1

    # Validate page
    if page > total_pages and total_pages > 0:
        conn.close()
        return RedirectResponse(
            url=f"/items/landing?sort={sort}&page={total_pages}", status_code=303
        )

    # Paginated query
    offset = (page - 1) * ITEMS_PER_PAGE
    rows = conn.execute(
        f"SELECT * FROM items {order} LIMIT ? OFFSET ?",
        (ITEMS_PER_PAGE, offset),
    ).fetchall()
    conn.close()

    paginated_items = [dict_from_row(r) for r in rows]

    return templates.TemplateResponse(
        request=request,
        name="items/items_landing.html",
        context={
            "products": paginated_items,
            "current_sort": sort,
            "current_page": page,
            "total_pages": total_pages,
            "items_per_page": ITEMS_PER_PAGE,
        },
    )


@router.get("/add", response_class=HTMLResponse)
async def add_item_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="item_form.html",
        context={"editing": False, "item": None, "item_id": None},
    )


@router.post("/")
async def create_item(
    name: str = Form(...),
    price: float = Form(...),
    is_offer: bool = Form(False),
):
    conn = get_connection()
    conn.execute(
        "INSERT INTO items (name, price, is_offer, tax) VALUES (?, ?, ?, ?)",
        (name, price, int(is_offer), round(price * 0.1, 2)),
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/items/landing", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/edit/{item_id}", response_class=HTMLResponse)
async def edit_item_form(request: Request, item_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item = dict_from_row(row)
    return templates.TemplateResponse(
        request=request,
        name="item_form.html",
        context={"editing": True, "item": item, "item_id": item_id},
    )


@router.post("/{item_id}")
async def update_item(
    item_id: int,
    name: str = Form(...),
    price: float = Form(...),
    is_offer: bool = Form(False),
):
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
    return RedirectResponse("/items/landing", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/delete/{item_id}", response_class=HTMLResponse)
async def confirm_delete(request: Request, item_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    item = dict_from_row(row) if row else None
    return templates.TemplateResponse(
        request=request,
        name="delete_confirm.html",
        context={"item": item, "item_id": item_id},
    )


@router.post("/delete/{item_id}")
async def delete_item(item_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/items/landing", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/search")
async def search_items(
    request: Request,
    min_price: float = None,
    max_price: float = None,
    sort: str = Query("default", pattern="^(default|name|price)$"),
    page: int = Query(1, ge=1),
):
    conn = get_connection()
    conditions = []
    params = []

    if min_price is not None:
        conditions.append("price >= ?")
        params.append(min_price)
    if max_price is not None:
        conditions.append("price <= ?")
        params.append(max_price)

    where = " AND ".join(conditions) if conditions else "1=1"
    count_sql = f"SELECT COUNT(*) FROM items WHERE {where}"
    total_items = conn.execute(count_sql, params).fetchone()[0]
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1

    if page > total_pages and total_pages > 0:
        conn.close()
        return RedirectResponse(
            url=f"/items/search?min_price={min_price}&max_price={max_price}&sort={sort}&page={total_pages}",
            status_code=303,
        )

    order = "ORDER BY id ASC"
    if sort == "name":
        order = "ORDER BY name COLLATE NOCASE ASC"
    elif sort == "price":
        order = "ORDER BY price ASC"

    offset = (page - 1) * ITEMS_PER_PAGE
    rows = conn.execute(
        f"SELECT * FROM items WHERE {where} {order} LIMIT ? OFFSET ?",
        params + [ITEMS_PER_PAGE, offset],
    ).fetchall()
    conn.close()

    paginated_items = [dict_from_row(r) for r in rows]

    return templates.TemplateResponse(
        request=request,
        name="items/items_landing.html",
        context={
            "products": paginated_items,
            "current_sort": sort,
            "current_page": page,
            "total_pages": total_pages,
            "items_per_page": ITEMS_PER_PAGE,
            "min_price": min_price,
            "max_price": max_price,
        },
    )
