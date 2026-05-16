from pydantic import BaseModel
from typing import Optional


class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str = ""


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int
    order_count: int = 0

    class Config:
        from_attributes = True
