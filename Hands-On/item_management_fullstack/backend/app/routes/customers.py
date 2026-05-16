import math
from fastapi import APIRouter, Request, Form, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Customer

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
ITEMS_PER_PAGE = 5


def require_admin(request: Request):
    if not request.session.get("admin_id"):
        return None
    return True


@router.get("/landing", response_class=HTMLResponse)
async def customers_landing(
    request: Request,
    sort: str = Query("default", pattern="^(default|name|email)$"),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)

    order_col = Customer.id
    if sort == "name":
        order_col = Customer.name
    elif sort == "email":
        order_col = Customer.email

    total = db.query(Customer).count()
    total_pages = math.ceil(total / ITEMS_PER_PAGE) if total > 0 else 1

    if page > total_pages and total_pages > 0:
        return RedirectResponse(
            url=f"/customers/landing?sort={sort}&page={total_pages}", status_code=303
        )

    offset = (page - 1) * ITEMS_PER_PAGE
    customers = (
        db.query(Customer)
        .order_by(order_col)
        .offset(offset)
        .limit(ITEMS_PER_PAGE)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="customers/customers_landing.html",
        context={
            "customers": customers,
            "current_sort": sort,
            "current_page": page,
            "total_pages": total_pages,
        },
    )


@router.get("/add", response_class=HTMLResponse)
async def add_customer_form(request: Request):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="customers/customer_form.html",
        context={"editing": False, "customer": None, "customer_id": None},
    )


@router.post("/")
async def create_customer(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    customer = Customer(name=name, email=email, phone=phone)
    db.add(customer)
    db.commit()
    return RedirectResponse("/customers/landing", status_code=303)


@router.get("/edit/{customer_id}", response_class=HTMLResponse)
async def edit_customer_form(
    request: Request, customer_id: int, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return templates.TemplateResponse(
        request=request,
        name="customers/customer_form.html",
        context={
            "editing": True,
            "customer": customer,
            "customer_id": customer_id,
        },
    )


@router.post("/{customer_id}")
async def update_customer(
    request: Request,
    customer_id: int,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.name = name
    customer.email = email
    customer.phone = phone
    db.commit()
    return RedirectResponse("/customers/landing", status_code=303)


@router.get("/delete/{customer_id}", response_class=HTMLResponse)
async def confirm_delete_customer(
    request: Request, customer_id: int, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    return templates.TemplateResponse(
        request=request,
        name="customers/customer_delete.html",
        context={"customer": customer, "customer_id": customer_id},
    )


@router.post("/delete/{customer_id}")
async def delete_customer(
    request: Request, customer_id: int, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        db.delete(customer)
        db.commit()
    return RedirectResponse("/customers/landing", status_code=303)
