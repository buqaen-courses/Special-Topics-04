from fastapi import APIRouter, HTTPException
from app.models import Item, ItemResponse, ItemsResponse
from typing import List
from fastapi import HTTPException,status
import json

DATA_FILE = "items.json"
router = APIRouter()

# ---------------------------
# Helpers
# ---------------------------

def load_items() -> List[dict]:
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file deleted or corrupted, recreate it
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []


def save_items(items: List[dict]):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)




# ---------------------------
# CREATE
# ---------------------------

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
async def create_item(item: Item):
    items = load_items()
    item.tax = item.price * 0.1    
    items.append(item.model_dump())
    save_items(items)
    return {"item": item, "message": "Item created successfully"}


# ---------------------------
# UPDATE
# ---------------------------

@router.put("/{item_id}", response_model=ItemResponse )
async def update_item(item_id: int, item: Item):
    items = load_items()

    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id] = item.model_dump()
    save_items(items)

    return {"message": "Item updated", "item": item}


# ---------------------------
# DELETE
# ---------------------------

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    items = load_items()

    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    deleted = items.pop(item_id)
    save_items(items)

    return {"message": "Item deleted", "deleted": deleted}


@router.get("/", response_model=ItemsResponse)
async def read_items():
    items = load_items()
    length = len(items)
    msg = f"Total Items: {length}"
    return {"items": items, "length" : length, "message" : msg}
