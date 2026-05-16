from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/api/customers", tags=["Customers"])


def require_auth(request: Request):
    if not request.session.get("admin_id"):
        return False
    return True


@router.get("")
async def list_customers(
    request: Request,
    sort: str = Query("default"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    order_map = {"name": Customer.name, "email": Customer.email}
    order_col = order_map.get(sort, Customer.id)
    total = db.query(Customer).count()
    customers = (
        db.query(Customer)
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
        "customers": [
            CustomerResponse(
                id=c.id, name=c.name, email=c.email,
                phone=c.phone or "", order_count=len(c.orders)
            )
            for c in customers
        ],
    }


@router.get("/{customer_id}")
async def get_customer(
    request: Request, customer_id: int, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerResponse(
        id=c.id, name=c.name, email=c.email,
        phone=c.phone or "", order_count=len(c.orders)
    )


@router.post("", status_code=201)
async def create_customer(
    request: Request, body: CustomerCreate, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    c = Customer(**body.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return CustomerResponse(
        id=c.id, name=c.name, email=c.email,
        phone=c.phone or "", order_count=0
    )


@router.put("/{customer_id}")
async def update_customer(
    request: Request, customer_id: int, body: CustomerCreate,
    db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    c.name = body.name
    c.email = body.email
    c.phone = body.phone
    db.commit()
    db.refresh(c)
    return CustomerResponse(
        id=c.id, name=c.name, email=c.email,
        phone=c.phone or "", order_count=len(c.orders)
    )


@router.patch("/{customer_id}")
async def patch_customer(
    request: Request, customer_id: int, body: CustomerUpdate,
    db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, val in body.model_dump(exclude_unset=True).items():
        setattr(c, key, val)
    db.commit()
    db.refresh(c)
    return CustomerResponse(
        id=c.id, name=c.name, email=c.email,
        phone=c.phone or "", order_count=len(c.orders)
    )


@router.delete("/{customer_id}")
async def delete_customer(
    request: Request, customer_id: int, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(c)
    db.commit()
    return {"message": "Customer deleted"}
