from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes.books import router as books_router
from app.routes.members import router as members_router
import json
import os

BOOKS_FILE = "books.json"
MEMBERS_FILE = "members.json"

def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r") as f:
        return json.load(f)

def load_members():
    if not os.path.exists(MEMBERS_FILE):
        return []
    with open(MEMBERS_FILE, "r") as f:
        return json.load(f)

app = FastAPI(title="Library Manager")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(books_router, prefix="/books")
app.include_router(members_router, prefix="/members")

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def root(request: Request):
    books = load_books()
    members = load_members()

    total_books = len(books)
    available_books = len([b for b in books if not b["is_loaned"]])
    loaned_books = total_books - available_books
    total_members = len(members)
    unique_authors = len(set(b["author"] for b in books)) if books else 0

    oldest = min(books, key=lambda b: b["year"]) if books else None
    newest = max(books, key=lambda b: b["year"]) if books else None

    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={
            "total_books": total_books,
            "available_books": available_books,
            "loaned_books": loaned_books,
            "total_members": total_members,
            "unique_authors": unique_authors,
            "oldest_title": oldest["title"] if oldest else "—",
            "oldest_year": oldest["year"] if oldest else "",
            "newest_title": newest["title"] if newest else "—",
            "newest_year": newest["year"] if newest else ""
        }
    )
