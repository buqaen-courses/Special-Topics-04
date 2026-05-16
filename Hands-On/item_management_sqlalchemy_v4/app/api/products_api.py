from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product

router = APIRouter(prefix="/api/products", tags=["Products API"])


@router.get("")
async def list_products_api(
    request: Request,
    sort: str = Query("name"),
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """JSON product list with sort and pagination. Requires auth."""
    if not request.session.get("admin_id"):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    order_map = {"name": Product.name, "price": Product.price, "stock": Product.stock}
    order_col = order_map.get(sort, Product.id)

    query = db.query(Product).order_by(order_col)
    total = query.count()
    products = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "stock": p.stock,
                "category_name": p.category.name if p.category else None,
            }
            for p in products
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": max(1, (total + per_page - 1) // per_page),
    }
