from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
import hashlib
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Admin
from app.api import auth_api, dashboard_api, products_api, categories_api, customers_api, orders_api

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop Manager — Full-Stack Edition", docs_url=None, redoc_url=None)

app.add_middleware(SessionMiddleware, secret_key="change-this-secret-key-in-production")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_api.router)
app.include_router(dashboard_api.router)
app.include_router(products_api.router)
app.include_router(categories_api.router)
app.include_router(customers_api.router)
app.include_router(orders_api.router)

security = HTTPBasic(auto_error=False)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )
    pw_hash = hashlib.sha256(credentials.password.encode()).hexdigest()
    admin = db.query(Admin).filter(
        Admin.username == credentials.username,
        Admin.password_hash == pw_hash,
    ).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Shop Manager API")


@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )
    pw_hash = hashlib.sha256(credentials.password.encode()).hexdigest()
    admin = db.query(Admin).filter(
        Admin.username == credentials.username,
        Admin.password_hash == pw_hash,
    ).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return app.openapi()


@app.get("/")
async def root():
    return RedirectResponse("/docs")
