import hashlib
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login")
async def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)):
    pw_hash = hashlib.sha256(body.password.encode()).hexdigest()
    admin = db.query(Admin).filter(
        Admin.username == body.username, Admin.password_hash == pw_hash
    ).first()
    if not admin:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Invalid username or password"},
        )
    request.session["admin_id"] = admin.id
    return {"success": True, "admin_id": admin.id, "message": "Logged in"}


@router.get("/me")
async def me(request: Request, db: Session = Depends(get_db)):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    return {"id": admin.id, "username": admin.username}


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"success": True, "message": "Logged out"}
