from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/api/products", tags=["Products"])


def require_auth(request: Request):
    if not request.session.get("admin_id"):
        return False
    return True


def product_to_response(p: Product) -> ProductResponse:
    return ProductResponse(
        id=p.id,
        name=p.name,
        description=p.description or "",
        price=p.price,
        stock=p.stock,
        category_id=p.category_id,
        category_name=p.category.name if p.category else None,
    )


@router.get("")
async def list_products(
    request: Request,
    sort: str = Query("default"),
    page: int = Query(1, ge=1),
    q: str = Query(""),
    min_price: float = Query(None),
    max_price: float = Query(None),
    category_id: int = Query(None),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    query = db.query(Product)
    if q:
        query = query.filter(
            Product.name.ilike(f"%{q}%") | Product.description.ilike(f"%{q}%")
        )
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    order_map = {"name": Product.name, "price": Product.price, "stock": Product.stock}
    order_col = order_map.get(sort, Product.id)
    query = query.order_by(order_col)

    total = query.count()
    products = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": max(1, (total + per_page - 1) // per_page),
        "products": [product_to_response(p) for p in products],
        "categories": [
            {"id": c.id, "name": c.name} for c in db.query(Category).all()
        ],
    }


@router.get("/{product_id}")
async def get_product(
    request: Request, product_id: int, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_response(product)


@router.post("", status_code=201)
async def create_product(
    request: Request, body: ProductCreate, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = Product(**body.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product_to_response(product)


@router.put("/{product_id}")
async def update_product(
    request: Request, product_id: int, body: ProductCreate, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, val in body.model_dump().items():
        setattr(product, key, val)
    db.commit()
    db.refresh(product)
    return product_to_response(product)


@router.patch("/{product_id}")
async def patch_product(
    request: Request, product_id: int, body: ProductUpdate, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, val in body.model_dump(exclude_unset=True).items():
        setattr(product, key, val)
    db.commit()
    db.refresh(product)
    return product_to_response(product)


@router.delete("/{product_id}")
async def delete_product(
    request: Request, product_id: int, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
