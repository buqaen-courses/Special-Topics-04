import hashlib
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin

router = APIRouter(prefix="/api/auth", tags=["Auth API"])


@router.post("/login")
async def api_login(request: Request, db: Session = Depends(get_db)):
    """JSON login endpoint. Accepts {username, password}, returns session cookie."""
    body = await request.json()
    pw_hash = hashlib.sha256(body["password"].encode()).hexdigest()
    admin = db.query(Admin).filter(
        Admin.username == body["username"],
        Admin.password_hash == pw_hash,
    ).first()
    if not admin:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Invalid credentials"},
        )
    request.session["admin_id"] = admin.id
    return {"success": True, "admin_id": admin.id}
