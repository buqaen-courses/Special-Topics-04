import math
from fastapi import APIRouter, Request, Form, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Category, Product

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
ITEMS_PER_PAGE = 5


def require_admin(request: Request):
    if not request.session.get("admin_id"):
        return None
    return True


@router.get("/landing", response_class=HTMLResponse)
async def categories_landing(
    request: Request,
    sort: str = Query("default", pattern="^(default|name)$"),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)

    order_col = Category.id
    if sort == "name":
        order_col = Category.name

    total = db.query(Category).count()
    total_pages = math.ceil(total / ITEMS_PER_PAGE) if total > 0 else 1

    if page > total_pages and total_pages > 0:
        return RedirectResponse(
            url=f"/categories/landing?sort={sort}&page={total_pages}", status_code=303
        )

    offset = (page - 1) * ITEMS_PER_PAGE
    categories = (
        db.query(Category)
        .order_by(order_col)
        .offset(offset)
        .limit(ITEMS_PER_PAGE)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="categories/categories_landing.html",
        context={
            "categories": categories,
            "current_sort": sort,
            "current_page": page,
            "total_pages": total_pages,
        },
    )


@router.get("/add", response_class=HTMLResponse)
async def add_category_form(request: Request):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="categories/category_form.html",
        context={"editing": False, "category": None, "category_id": None},
    )


@router.post("/")
async def create_category(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    cat = Category(name=name, description=description)
    db.add(cat)
    db.commit()
    return RedirectResponse("/categories/landing", status_code=303)


@router.get("/edit/{category_id}", response_class=HTMLResponse)
async def edit_category_form(
    request: Request, category_id: int, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return templates.TemplateResponse(
        request=request,
        name="categories/category_form.html",
        context={"editing": True, "category": cat, "category_id": category_id},
    )


@router.post("/{category_id}")
async def update_category(
    request: Request,
    category_id: int,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    cat.name = name
    cat.description = description
    db.commit()
    return RedirectResponse("/categories/landing", status_code=303)


@router.get("/delete/{category_id}", response_class=HTMLResponse)
async def confirm_delete_category(
    request: Request, category_id: int, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    cat = db.query(Category).filter(Category.id == category_id).first()
    return templates.TemplateResponse(
        request=request,
        name="categories/category_delete.html",
        context={"category": cat, "category_id": category_id},
    )


@router.post("/delete/{category_id}")
async def delete_category(
    request: Request, category_id: int, db: Session = Depends(get_db)
):
    if not require_admin(request):
        return RedirectResponse("/auth/login", status_code=303)
    cat = db.query(Category).filter(Category.id == category_id).first()
    if cat:
        db.delete(cat)
        db.commit()
    return RedirectResponse("/categories/landing", status_code=303)
