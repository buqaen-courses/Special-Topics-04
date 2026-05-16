from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
import math
from fastapi.templating import Jinja2Templates
from fastapi import Form, status
from fastapi.responses import RedirectResponse
from fastapi import HTTPException

import json
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
DATA_FILE = "items.json"
ITEMS_PER_PAGE = 5

def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

@router.get("/landing", response_class=HTMLResponse)
async def landing_page(
    request: Request,
    sort: str = Query("default", pattern="^(default|name|price)$"),
    page: int = Query(1, ge=1)
):
    # Step 1: Load all items
    items = load_items()   # each item is a dict with keys: id, name, price, is_offer
    
    # Step 2: Apply sorting
    if sort == "name":
        items = sorted(items, key=lambda x: x["name"].lower())
    elif sort == "price":
        items = sorted(items, key=lambda x: x["price"])
    
    # Step 3: Calculate pagination
    total_items = len(items)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    # Step 4: Validate page number
    if page > total_pages and total_pages > 0:
        # Redirect to last valid page (using correct route "/landing")
        return RedirectResponse(
            url=f"/items/landing?sort={sort}&page={total_pages}",
            status_code=303
        )
    
    # Step 5: Slice items for current page
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    paginated_items = items[start:end]
    
    # Step 6: Render template
    return templates.TemplateResponse(
        request=request,
        name="items/items_landing.html",
        context={
            "products": paginated_items,      # used in template as "products"
            "current_sort": sort,
            "current_page": page,
            "total_pages": total_pages,
            "items_per_page": ITEMS_PER_PAGE
        }
    )
@router.get("/add", response_class=HTMLResponse)
async def add_item_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="item_form.html",
        context={"editing": False, "item": None, "item_id": None}
    )


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

@router.get("/delete/{item_id}", response_class=HTMLResponse)
async def confirm_delete(request: Request, item_id: int):
    items = load_items()
    item = None
    if not(item_id < 0 or item_id >= len(items)):
        #     raise HTTPException(status_code=404, detail="Item not found")
        item = items[item_id]
    return templates.TemplateResponse(
        request=request,
        name="delete_confirm.html",
        context={"item": item , "item_id": item_id}
)

@router.post("/delete/{item_id}")
async def delete_item(item_id: int):
    items = load_items()
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    items.pop(item_id)
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)
    return RedirectResponse("/items/landing", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/search")
async def search_items(
    request: Request,
    min_price: float = None,
    max_price: float = None,
    sort: str = Query("default", pattern="^(default|name|price)$"),
    page: int = Query(1, ge=1)
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

    if sort == "name":
        filtered = sorted(filtered, key=lambda x: x["name"].lower())
    elif sort == "price":
        filtered = sorted(filtered, key=lambda x: x["price"])

    total_items = len(filtered)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

    if page > total_pages and total_pages > 0:
        return RedirectResponse(
            url=f"/items/search?min_price={min_price}&max_price={max_price}&sort={sort}&page={total_pages}",
            status_code=303
        )

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    paginated_items = filtered[start:end]

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
            "max_price": max_price
        }
    )