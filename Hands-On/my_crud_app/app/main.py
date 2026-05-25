from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.items import router as item_router
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates



app = FastAPI(title="Items CRUD - Step by Step")

# Serve static files (CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# http://localhost:8000/static/css/custom.css -->> http://localhost:8000/app/static/css/custom.css

# Include the items router (all routes under /items)
app.include_router(item_router, prefix="/items")

# ---------------------------
# Template Engine Setup
# ---------------------------
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def root():
    return RedirectResponse(url="/items/landing")