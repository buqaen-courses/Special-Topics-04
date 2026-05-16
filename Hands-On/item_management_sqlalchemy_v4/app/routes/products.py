import math
from fastapi import APIRouter, Request, Form, Depends, Query, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Product, Category

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
ITEMS_PER_PAGE = 5


def require_admin(request: Request):
    if not request.session.get("admin_id"):
        return None
    return True


@router.get("/landing", response_class=HTMLResponse)
async def products_landing(
    request: Request,
    sort: str = Query("default", pattern="^(default|name|price|stock)$"),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)

    order_col = Product.id
    if sort == "name":
        order_col = Product.name
    elif sort == "price":
        order_col = Product.price
    elif sort == "stock":
        order_col = Product.stock

    total_items = db.query(Product).count()
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1

    if page > total_pages and total_pages > 0:
        return RedirectResponse(
            url=f"/products/landing?sort={sort}&page={total_pages}", status_code=303
        )

    offset = (page - 1) * ITEMS_PER_PAGE
    products = (
        db.query(Product)
        .order_by(order_col)
        .offset(offset)
        .limit(ITEMS_PER_PAGE)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="products/products_landing.html",
        context={
            "products": products,
            "current_sort": sort,
            "current_page": page,
            "total_pages": total_pages,
            "items_per_page": ITEMS_PER_PAGE,
        },
    )


@router.get("/search")
async def search_products(
    request: Request,
    q: str = Query(""),
    min_price: float = None,
    max_price: float = None,
    category_id: int = None,
    sort: str = Query("default", pattern="^(default|name|price|stock)$"),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)

    query = db.query(Product)

    if q:
        query = query.filter(
            Product.name.ilike(f"%{q}%")
            | Product.description.ilike(f"%{q}%")
        )
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    order_col = Product.id
    if sort == "name":
        order_col = Product.name
    elif sort == "price":
        order_col = Product.price
    elif sort == "stock":
        order_col = Product.stock

    total_items = query.count()
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1

    if page > total_pages and total_pages > 0:
        return RedirectResponse(
            url=f"/products/search?q={q}&min_price={min_price}&max_price={max_price}&sort={sort}&page={total_pages}",
            status_code=303,
        )

    offset = (page - 1) * ITEMS_PER_PAGE
    products = (
        query.order_by(order_col).offset(offset).limit(ITEMS_PER_PAGE).all()
    )
    categories = db.query(Category).all()

    return templates.TemplateResponse(
        request=request,
        name="products/products_landing.html",
        context={
            "products": products,
            "current_sort": sort,
            "current_page": page,
            "total_pages": total_pages,
            "items_per_page": ITEMS_PER_PAGE,
            "q": q,
            "min_price": min_price,
            "max_price": max_price,
            "category_id": category_id,
            "categories": categories,
        },
    )


@router.get("/add", response_class=HTMLResponse)
async def add_product_form(request: Request, db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    categories = db.query(Category).all()
    return templates.TemplateResponse(
        request=request,
        name="products/product_form.html",
        context={"editing": False, "product": None, "product_id": None, "categories": categories},
    )


@router.post("/")
async def create_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    stock: int = Form(0),
    category_id: int = Form(None),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id if category_id else None,
    )
    db.add(product)
    db.commit()
    return RedirectResponse("/products/landing", status_code=303)


@router.get("/edit/{product_id}", response_class=HTMLResponse)
async def edit_product_form(
    request: Request, product_id: int, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    categories = db.query(Category).all()
    return templates.TemplateResponse(
        request=request,
        name="products/product_form.html",
        context={
            "editing": True,
            "product": product,
            "product_id": product_id,
            "categories": categories,
        },
    )


@router.post("/{product_id}")
async def update_product(
    request: Request,
    product_id: int,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    stock: int = Form(0),
    category_id: int = Form(None),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = name
    product.description = description
    product.price = price
    product.stock = stock
    product.category_id = category_id if category_id else None
    db.commit()
    return RedirectResponse("/products/landing", status_code=303)


@router.get("/delete/{product_id}", response_class=HTMLResponse)
async def confirm_delete_product(
    request: Request, product_id: int, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    product = db.query(Product).filter(Product.id == product_id).first()
    return templates.TemplateResponse(
        request=request,
        name="products/product_delete.html",
        context={"product": product, "product_id": product_id},
    )


@router.post("/delete/{product_id}")
async def delete_product(
    request: Request, product_id: int, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return RedirectResponse("/products/landing", status_code=303)
