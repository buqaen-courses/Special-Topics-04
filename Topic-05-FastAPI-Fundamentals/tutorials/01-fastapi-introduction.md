# Tutorial 01: FastAPI Introduction

## Overview
This tutorial introduces FastAPI, a modern, fast web framework for building APIs with Python. You'll learn the core concepts, basic structure, and how FastAPI differs from other web frameworks.

## What is FastAPI?

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

### Key Features

- **Fast**: Very high performance, on par with NodeJS and Go
- **Fast to code**: Increase development speed by 200-300%
- **Fewer bugs**: Reduce human-induced errors by 40%
- **Intuitive**: Great editor support with auto-completion
- **Easy**: Designed to be easy to use and learn
- **Short**: Minimize code duplication
- **Robust**: Get production-ready code with automatic interactive documentation

### Why FastAPI?

Compared to other frameworks like Flask and Django:

| Feature | Flask | Django | FastAPI |
|---------|-------|--------|---------|
| Performance | Good | Good | Excellent |
| Type Safety | None | Limited | Full |
| Auto Docs | Manual | Manual | Automatic |
| Validation | Manual | Manual | Automatic |
| Async Support | Limited | Limited | Full |
| Learning Curve | Low | Medium | Low |

## Installation and Setup

### Requirements
- Python 3.8+
- pip (Python package installer)

### Installation
```bash
# Create virtual environment
uv venv

# Activate virtual environment (optional - uv run is preferred)
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install FastAPI and Uvicorn
uv add fastapi uvicorn

# Optional: Install additional dependencies
uv add pydantic requests
```

## Your First FastAPI Application

### Basic Application Structure
```python
from fastapi import FastAPI

# Create FastAPI application instance
app = FastAPI(
    title="My API",
    description="A simple FastAPI application",
    version="1.0.0"
)

# Define a route
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### Running the Application
```bash
# Run with uvicorn
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Access your API:**
- **Root endpoint**: http://localhost:8000/
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## Core Concepts

### Path Parameters
```python
from fastapi import FastAPI

app = FastAPI()

# Path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Multiple path parameters
@app.get("/users/{user_id}/posts/{post_id}")
async def read_user_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}

# String path parameter
@app.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}
```

### Query Parameters
```python
from typing import Optional

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10, q: Optional[str] = None):
    return {"skip": skip, "limit": limit, "q": q}

# Optional query parameters
@app.get("/search")
async def search_items(
    q: Optional[str] = None,
    category: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None
):
    return {
        "query": q,
        "category": category,
        "price_range": {"min": price_min, "max": price_max}
    }
```

### Request Body
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.post("/items/")
async def create_item(item: Item):
    return item

# Using the Item model
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
```

### HTTP Methods
```python
@app.get("/items")
async def read_items():
    return {"message": "Read items"}

@app.post("/items")
async def create_item():
    return {"message": "Create item"}

@app.put("/items/{item_id}")
async def update_item(item_id: int):
    return {"item_id": item_id, "message": "Update item"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"item_id": item_id, "message": "Delete item"}

@app.patch("/items/{item_id}")
async def partial_update_item(item_id: int):
    return {"item_id": item_id, "message": "Partial update"}
```

### Status Codes
```python
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return {"item_id": item_id}

# Custom status codes
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return {"message": "Item created", "item": item}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None
```
## A Sample Project
```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
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

@app.post("/items/")
async def create_item(item: Item):
    items = load_items()
    items.append(item.model_dump())
    save_items(items)
    return {"message": "Item added", "items": items}


# ---------------------------
# UPDATE
# ---------------------------

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    items = load_items()

    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id] = item.model_dump()
    save_items(items)

    return {"message": "Item updated", "items": items}


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

```
## Advanced Features

### Async Support
```python
import asyncio

@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(1)
    return {"message": "This was async"}

# Mixing sync and async
@app.get("/sync")
def sync_endpoint():
    # This will run in a thread pool
    return {"message": "This was sync"}
```

### Background Tasks
```python
from fastapi import BackgroundTasks

def send_email_notification(email: str, message: str):
    # Simulate sending email
    print(f"Sending email to {email}: {message}")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_notification, email, "Your order is ready!")
    return {"message": "Notification will be sent"}
```

### Response Models
```python
from typing import List
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    tax: Optional[float] = None

class ItemResponse(BaseModel):
    item: Item
    message: str

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    # Calculate tax
    item.tax = item.price * 0.1
    return {"item": item, "message": "Item created successfully"}

# List response
@app.get("/items/", response_model=List[Item])
async def read_items():
    return [
        Item(name="Item 1", price=10.0),
        Item(name="Item 2", price=20.0)
    ]
```

### Error Handling
```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

@app.get("/divide/{x}/{y}")
async def divide(x: float, y: float):
    if y == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": x / y}

# Custom exception
class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=422,
        content={"error": exc.message},
    )
```

## Project Structure Best Practices

### Basic Structure
```
myapi/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app instance
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   ├── models.py        # Pydantic models
│   ├── routes/          # Route handlers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   ├── dependencies.py  # Dependencies
│   └── utils.py         # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_routes.py
├── requirements.txt
├── .env
└── README.md
```

### Modular Application
```python
# app/main.py
from fastapi import FastAPI
from .routes import items, users

app = FastAPI()

app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(users.router, prefix="/users", tags=["users"])
```

```python
# app/routes/items.py
from fastapi import APIRouter, HTTPException
from ..models import Item, ItemCreate

router = APIRouter()

items_db = []

@router.get("/", response_model=list[Item])
async def read_items():
    return items_db

@router.post("/", response_model=Item)
async def create_item(item: ItemCreate):
    new_item = Item(id=len(items_db) + 1, **item.dict())
    items_db.append(new_item)
    return new_item
```

## Testing FastAPI Applications

### Basic Testing
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post("/items/", json={"name": "Test Item", "price": 10.0})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data
```

### Async Testing
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_items():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/items/")
        assert response.status_code == 200
```

## Performance Considerations

### Startup Time
- Use async when possible
- Minimize imports at module level
- Use lazy loading for heavy dependencies

### Response Time
- Use response caching
- Implement pagination for large datasets
- Use background tasks for heavy operations
- Optimize database queries

### Memory Usage
- Use streaming responses for large data
- Implement proper cleanup
- Monitor memory usage in production

## Hands-on Exercises

### Exercise 1: Basic API
1. Create a FastAPI application with basic endpoints
2. Add path parameters, query parameters, and request bodies
3. Test all endpoints using the interactive docs

### Exercise 2: Data Validation
1. Create Pydantic models for a blog post system
2. Implement validation rules (length, format, etc.)
3. Handle validation errors gracefully

### Exercise 3: RESTful Design
1. Design a complete REST API for a resource
2. Implement all CRUD operations
3. Add proper HTTP status codes and error handling

## Next Steps
- [Pydantic Models Tutorial](../tutorials/02-pydantic-models.md)
- [Workshop: Basic API](../workshops/workshop-01-basic-api.md)

## Additional Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
