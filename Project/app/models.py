
from pydantic import BaseModel
from typing import Optional, List

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False
    tax : Optional[float] = None

class ItemResponse(BaseModel):
    item: Item
    message: str

class ItemsResponse(BaseModel):
    items : List[Item]
    length : int 
    message : str