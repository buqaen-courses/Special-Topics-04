from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: str = ""
    price: float
    stock: int = 0
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    category_name: Optional[str] = None

    class Config:
        from_attributes = True
