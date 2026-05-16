from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Category, Product
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/api/categories", tags=["Categories"])


def require_auth(request: Request):
    if not request.session.get("admin_id"):
        return False
    return True


@router.get("")
async def list_categories(
    request: Request,
    sort: str = Query("default"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    order_col = Category.name if sort == "name" else Category.id
    total = db.query(Category).count()
    categories = (
        db.query(Category)
        .order_by(order_col)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": max(1, (total + per_page - 1) // per_page),
        "categories": [
            CategoryResponse(
                id=c.id, name=c.name, description=c.description or "",
                product_count=len(c.products)
            )
            for c in categories
        ],
    }


@router.get("/{category_id}")
async def get_category(
    request: Request, category_id: int, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryResponse(
        id=cat.id, name=cat.name, description=cat.description or "",
        product_count=len(cat.products)
    )


@router.post("", status_code=201)
async def create_category(
    request: Request, body: CategoryCreate, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    cat = Category(**body.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return CategoryResponse(
        id=cat.id, name=cat.name, description=cat.description or "", product_count=0
    )


@router.put("/{category_id}")
async def update_category(
    request: Request, category_id: int, body: CategoryCreate,
    db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    cat.name = body.name
    cat.description = body.description
    db.commit()
    db.refresh(cat)
    return CategoryResponse(
        id=cat.id, name=cat.name, description=cat.description or "",
        product_count=len(cat.products)
    )


@router.patch("/{category_id}")
async def patch_category(
    request: Request, category_id: int, body: CategoryUpdate,
    db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, val in body.model_dump(exclude_unset=True).items():
        setattr(cat, key, val)
    db.commit()
    db.refresh(cat)
    return CategoryResponse(
        id=cat.id, name=cat.name, description=cat.description or "",
        product_count=len(cat.products)
    )


@router.delete("/{category_id}")
async def delete_category(
    request: Request, category_id: int, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()
    return {"message": "Category deleted"}
