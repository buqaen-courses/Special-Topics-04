from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
import json
import os
from app.routes import items as items_router
from app.routes.items import api_router as items_api_router

from fastapi.staticfiles import StaticFiles

# ---------------------------
# Model
# ---------------------------
from app.models import *

app = FastAPI(title="Items CRUD with File Storage")

# Mount /static -> app/static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ---------------------------
# Template Engine Setup
# ---------------------------
templates = Jinja2Templates(directory="app/templates")

# ---------------------------
# Include existing items API router
# ---------------------------
app.include_router(items_router.router, prefix="/items", tags=["items"])
app.include_router(items_api_router, prefix="/api/items", tags=["items-api"])


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
# Home Page (redirects to /landing)
# ---------------------------

@app.get("/", response_class=HTMLResponse)
async def home():
    items = items_router.load_items()

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
# Landing Page (New!)
# ---------------------------
@app.get("/landing", response_class=HTMLResponse)
async def landing(request: Request):
    items = items_router.load_items()
    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={"items": items}
    )
