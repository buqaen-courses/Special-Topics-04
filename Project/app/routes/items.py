"""
app/routes/items.py
-------------------

Routes for item management.

Two interfaces are provided:

1. HTML + Forms (No JavaScript)
   Used by the web UI.

2. REST API (JSON)
   Used by API clients.

"""

from fastapi import APIRouter, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
import json

from app.models import Item, ItemResponse, ItemsResponse


# ---------------------------------------------------------------------
# Router Setup
# ---------------------------------------------------------------------

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

DATA_FILE = "items.json"


# ---------------------------------------------------------------------
# Persistence Helpers
# ---------------------------------------------------------------------

def load_items() -> List[dict]:
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []


def save_items(items: List[dict]):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)


# =====================================================================
# HTML FORM ROUTES (NO JAVASCRIPT)
# =====================================================================

@router.post("/")
async def create_item_form(
    name: str = Form(...),
    price: float = Form(...),
    is_offer: Optional[bool] = Form(False)
):
    """
    Create item from HTML form.
    """
    items = load_items()

    item = Item(name=name, price=price, is_offer=bool(is_offer))
    item.tax = item.price * 0.1

    items.append(item.model_dump())
    save_items(items)

    return RedirectResponse("/landing", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{item_id}")
async def update_item_form(
    item_id: int,
    name: str = Form(...),
    price: float = Form(...),
    is_offer: Optional[bool] = Form(False)
):
    """
    Update item using HTML form.
    """
    items = load_items()

    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    item = Item(name=name, price=price, is_offer=bool(is_offer))
    item.tax = item.price * 0.1

    items[item_id] = item.model_dump()
    save_items(items)

    return RedirectResponse("/landing", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/delete/{item_id}")
async def delete_item_form(item_id: int):
    """
    Delete item via form confirmation page.
    """
    items = load_items()

    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    items.pop(item_id)
    save_items(items)

    return RedirectResponse("/landing", status_code=status.HTTP_303_SEE_OTHER)


# ---------------------------------------------------------------------
# HTML PAGE ROUTES
# ---------------------------------------------------------------------

@router.get("/add", response_class=HTMLResponse)
async def add_item_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="item_form.html",
        context={
            "editing": False,
            "item": None,
            "item_id": None
        }
    )


@router.get("/edit/{item_id}", response_class=HTMLResponse)
async def edit_item_page(request: Request, item_id: int):

    items = load_items()

    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    return templates.TemplateResponse(
        request=request,
        name="item_form.html",
        context={
            "editing": True,
            "item": items[item_id],
            "item_id": item_id
        }
    )


@router.get("/delete/{item_id}", response_class=HTMLResponse)
async def delete_confirm_page(request: Request, item_id: int):

    items = load_items()

    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    return templates.TemplateResponse(
        request=request,
        name="delete_confirm.html",
        context={
            "item": items[item_id],
            "item_id": item_id
        }
    )

@router.get("/search", response_class=HTMLResponse)
async def search_items(request: Request,
                       min_price: float | None = None,
                       max_price: float | None = None):

    items = load_items()

    # Filtering logic
    filtered = []
    for item in items:
        price = float(item["price"])

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
            "active": "landing",
            "min_price": min_price,
            "max_price": max_price
        }
    )


# =====================================================================
# REST API ROUTES (JSON)
# =====================================================================

api_router = APIRouter()


@api_router.get("/", response_model=ItemsResponse)
async def read_items():
    items = load_items()
    return {
        "items": items,
        "length": len(items),
        "message": f"Total Items: {len(items)}"
    }


@api_router.post("/", response_model=ItemResponse)
async def create_item_api(item: Item):

    items = load_items()

    item.tax = item.price * 0.1
    items.append(item.model_dump())

    save_items(items)

    return {"item": item, "message": "Item created"}


@api_router.put("/{item_id}", response_model=ItemResponse)
async def update_item_api(item_id: int, item: Item):

    items = load_items()

    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id] = item.model_dump()
    save_items(items)

    return {"item": item, "message": "Item updated"}


@api_router.delete("/{item_id}")
async def delete_item_api(item_id: int):

    items = load_items()

    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    deleted = items.pop(item_id)
    save_items(items)

    return {"deleted": deleted, "message": "Item deleted"}
