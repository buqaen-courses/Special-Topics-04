import hashlib
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_current_admin(request: Request, db: Session = Depends(get_db)):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return None
    return db.query(Admin).filter(Admin.id == admin_id).first()


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"error": None}
    )


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    admin = (
        db.query(Admin)
        .filter(Admin.username == username, Admin.password_hash == pw_hash)
        .first()
    )
    if not admin:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid username or password"},
        )
    request.session["admin_id"] = admin.id
    return RedirectResponse("/", status_code=303)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/auth/login", status_code=303)
