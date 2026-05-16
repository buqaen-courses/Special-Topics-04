import math
from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Order, OrderItem, Customer, Product

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
ITEMS_PER_PAGE = 10


def require_admin(request: Request):
    if not request.session.get("admin_id"):
        return None
    return True


@router.get("/landing", response_class=HTMLResponse)
async def orders_landing(
    request: Request,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)

    total = db.query(Order).count()
    total_pages = math.ceil(total / ITEMS_PER_PAGE) if total > 0 else 1

    if page > total_pages and total_pages > 0:
        return RedirectResponse(
            url=f"/orders/landing?page={total_pages}", status_code=303
        )

    offset = (page - 1) * ITEMS_PER_PAGE
    orders = (
        db.query(Order)
        .options(joinedload(Order.customer))
        .order_by(Order.order_date.desc())
        .offset(offset)
        .limit(ITEMS_PER_PAGE)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="orders/orders_landing.html",
        context={
            "orders": orders,
            "current_page": page,
            "total_pages": total_pages,
        },
    )


@router.get("/create", response_class=HTMLResponse)
async def create_order_form(request: Request, db: Session = Depends(get_db)):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    customers = db.query(Customer).all()
    products = db.query(Product).all()
    return templates.TemplateResponse(
        request=request,
        name="orders/order_form.html",
        context={"customers": customers, "products": products, "error": None},
    )


@router.post("/create")
async def create_order(
    request: Request,
    customer_id: int = Form(...),
    product_ids: list[int] = Form(...),
    quantities: list[int] = Form(...),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)

    customers = db.query(Customer).all()
    products_list = db.query(Product).all()

    if not product_ids or not quantities or len(product_ids) != len(quantities):
        return templates.TemplateResponse(
            request=request,
            name="orders/order_form.html",
            context={
                "customers": customers,
                "products": products_list,
                "error": "Please select at least one product with a quantity.",
            },
        )

    total_amount = 0.0
    items_data = []

    for pid, qty in zip(product_ids, quantities):
        if qty < 1:
            continue
        product = db.query(Product).filter(Product.id == pid).first()
        if not product:
            continue
        if product.stock < qty:
            return templates.TemplateResponse(
                request=request,
                name="orders/order_form.html",
                context={
                    "customers": customers,
                    "products": products_list,
                    "error": f"Insufficient stock for '{product.name}'. Available: {product.stock}",
                },
            )
        total_amount += product.price * qty
        items_data.append((product, qty))

    order = Order(
        customer_id=customer_id,
        order_date=datetime.utcnow(),
        total_amount=round(total_amount, 2),
        status="pending",
    )
    db.add(order)
    db.flush()

    for product, qty in items_data:
        oi = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=qty,
            unit_price=product.price,
        )
        db.add(oi)
        product.stock -= qty

    db.commit()
    return RedirectResponse(f"/orders/{order.id}", status_code=303)


@router.get("/{order_id}", response_class=HTMLResponse)
async def order_detail(
    request: Request, order_id: int, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)

    order = (
        db.query(Order)
        .options(
            joinedload(Order.customer),
            joinedload(Order.order_items).joinedload(OrderItem.product),
        )
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        return RedirectResponse("/orders/landing", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="orders/order_detail.html",
        context={"order": order},
    )


@router.get("/{order_id}/status/{new_status}")
async def update_order_status(
    request: Request, order_id: int, new_status: str, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    order = db.query(Order).filter(Order.id == order_id).first()
    if order and new_status in ("pending", "completed", "cancelled"):
        order.status = new_status
        db.commit()
    return RedirectResponse(f"/orders/{order_id}", status_code=303)
