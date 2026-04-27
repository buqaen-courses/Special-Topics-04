from fastapi import FastAPI, HTTPException,status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI(title="Items CRUD with File Storage")

DATA_FILE = "items.json"


# ---------------------------
# Ensure file exists on startup
# ---------------------------

@app.on_event("startup")
def create_file_if_not_exists():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


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
# Model
# ---------------------------

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

# ---------------------------
# Home Page
# ---------------------------

@app.get("/", response_class=HTMLResponse)
async def home():
    items = load_items()

    html = """
    <html>
    <head>
        <title>Items</title>
        <style>
            table { border-collapse: collapse; width: 60%; margin: 20px auto; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #f4f4f4; }
            body { font-family: Arial; background: #fafafa; }
        </style>
    </head>
    <body>
        <h2 style="text-align:center;">Items List</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Price</th>
                <th>Is Offer</th>
            </tr>
    """

    for idx, item in enumerate(items):
        html += f"""
            <tr>
                <td>{idx}</td>
                <td>{item['name']}</td>
                <td>{item['price']}</td>
                <td>{item['is_offer']}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html


# ---------------------------
# CREATE
# ---------------------------

@app.post("/items/", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
async def create_item(item: Item):
    items = load_items()
    item.tax = item.price * 0.1    
    items.append(item.model_dump())
    save_items(items)
    return {"item": item, "message": "Item created successfully"}


# ---------------------------
# UPDATE
# ---------------------------

@app.put("/items/{item_id}", response_model=ItemResponse )
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

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    items = load_items()

    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    deleted = items.pop(item_id)
    save_items(items)

    return {"message": "Item deleted", "deleted": deleted}


@app.get("/items/", response_model=ItemsResponse)
async def read_items():
    items = load_items()
    length = len(items)
    msg = f"Total Items: {length}"
    return {"items": items, "length" : length, "message" : msg}