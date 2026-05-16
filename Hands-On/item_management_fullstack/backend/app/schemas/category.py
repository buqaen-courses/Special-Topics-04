from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    description: str = ""


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    product_count: int = 0

    class Config:
        from_attributes = True
