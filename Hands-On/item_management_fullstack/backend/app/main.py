from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, products, categories, customers, orders
from app.api import auth_api, dashboard_api, products_api, categories_api, customers_api, orders_api

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop Manager — Full-Stack Edition")

app.add_middleware(SessionMiddleware, secret_key="change-this-secret-key-in-production")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# HTML template routes
app.include_router(auth.router, prefix="/auth")
app.include_router(products.router, prefix="/products")
app.include_router(categories.router, prefix="/categories")
app.include_router(customers.router, prefix="/customers")
app.include_router(orders.router, prefix="/orders")

# JSON API routes
app.include_router(auth_api.router)
app.include_router(dashboard_api.router)
app.include_router(products_api.router)
app.include_router(categories_api.router)
app.include_router(customers_api.router)
app.include_router(orders_api.router)

templates = Jinja2Templates(directory="app/templates")


from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, Category, Customer, Order
from sqlalchemy import func


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
    revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
    low_stock = db.query(Product).filter(Product.stock < 5).count()
    recent_orders = (
        db.query(Order).order_by(Order.order_date.desc()).limit(5).all()
    )
    return templates.TemplateResponse(
        request=request, name="landing.html", context={
            "total_products": total_products,
            "total_categories": total_categories,
            "total_customers": total_customers,
            "total_orders": total_orders,
            "total_revenue": round(revenue, 2),
            "low_stock": low_stock,
            "recent_orders": recent_orders,
        },
    )
