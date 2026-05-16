from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Product, Category, Customer, Order, OrderItem

router = APIRouter(prefix="/api", tags=["Dashboard"])


def require_auth(request: Request):
    if not request.session.get("admin_id"):
        return False
    return True


@router.get("/dashboard")
async def dashboard(request: Request, db: Session = Depends(get_db)):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    total_products = db.query(Product).count()
    total_categories = db.query(Category).count()
    total_customers = db.query(Customer).count()
    total_orders = db.query(Order).count()
    revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
    low_stock = db.query(Product).filter(Product.stock < 5).count()

    recent_orders = (
        db.query(Order).order_by(Order.order_date.desc()).limit(5).all()
    )

    return {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_revenue": round(revenue, 2),
        "low_stock": low_stock,
        "recent_orders": [
            {
                "id": o.id,
                "customer_name": o.customer.name if o.customer else "N/A",
                "order_date": o.order_date.isoformat(),
                "total_amount": o.total_amount,
                "status": o.status,
            }
            for o in recent_orders
        ],
    }
