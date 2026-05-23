from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Product, Category, Customer, Order
from app.routes import auth, products, categories, customers, orders
from app.api import auth_api, products_api

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop Manager — SQLAlchemy CRUD")

app.add_middleware(SessionMiddleware, secret_key="change-this-secret-key-in-production")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router, prefix="/auth")
app.include_router(products.router, prefix="/products")
app.include_router(categories.router, prefix="/categories")
app.include_router(customers.router, prefix="/customers")
app.include_router(orders.router, prefix="/orders")

# JSON API routes (used by Vue.js in Part 4.5)
app.include_router(auth_api.router)
app.include_router(products_api.router)

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def root(request: Request, db: Session = Depends(get_db)):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return templates.TemplateResponse(
            request=request, name="login.html", context={"error": None}
        )

    total_products = db.query(Product).count()
    total_categories = db.query(Category).count()
    total_customers = db.query(Customer).count()
    total_orders = db.query(Order).count()

    from sqlalchemy import func
    revenue_result = db.query(func.sum(Order.total_amount)).scalar() or 0
    low_stock = db.query(Product).filter(Product.stock < 5).count()
    recent_orders = (
        db.query(Order)
        .order_by(Order.order_date.desc())
        .limit(5)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={
            "total_products": total_products,
            "total_categories": total_categories,
            "total_customers": total_customers,
            "total_orders": total_orders,
            "total_revenue": round(revenue_result, 2),
            "low_stock": low_stock,
            "recent_orders": recent_orders,
        },
    )


@app.get("/viewer", include_in_schema=False)
async def product_viewer():
    """Serves the Vue.js product viewer HTML file (Workshop 4.5)."""
    with open("product-viewer.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())
