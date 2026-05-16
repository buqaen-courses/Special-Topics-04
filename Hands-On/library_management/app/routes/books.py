from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form, status
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
import json
import os
import math

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
BOOKS_FILE = "books.json"
ITEMS_PER_PAGE = 5

def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r") as f:
        return json.load(f)

@router.get("/landing", response_class=HTMLResponse)
async def books_landing(
    request: Request,
    sort: str = Query("default", pattern="^(default|title|author|year)$"),
    page: int = Query(1, ge=1),
    search: str = Query(None)
):
    books = load_books()

    # Step 1: Search filter (by title, author, or ISBN)
    if search:
        search_lower = search.lower()
        filtered = []
        for b in books:
            if (search_lower in b["title"].lower() or
                search_lower in b["author"].lower() or
                search_lower in b["isbn"].lower()):
                filtered.append(b)
        books = filtered

    # Step 2: Sort
    if sort == "title":
        books = sorted(books, key=lambda x: x["title"].lower())
    elif sort == "author":
        books = sorted(books, key=lambda x: x["author"].lower())
    elif sort == "year":
        books = sorted(books, key=lambda x: x["year"])

    # Step 3: Paginate
    total_items = len(books)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

    if page > total_pages and total_pages > 0:
        search_param = f"&search={search}" if search else ""
        return RedirectResponse(
            url=f"/books/landing?sort={sort}&page={total_pages}{search_param}",
            status_code=303
        )

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    paginated_books = books[start:end]

    return templates.TemplateResponse(
        request=request,
        name="books/books_landing.html",
        context={
            "books": paginated_books,
            "current_sort": sort,
            "current_page": page,
            "total_pages": total_pages,
            "items_per_page": ITEMS_PER_PAGE,
            "search": search
        }
    )

@router.get("/add", response_class=HTMLResponse)
async def add_book_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="books/book_form.html",
        context={"editing": False, "book": None, "book_isbn": None}
    )

@router.post("/")
async def create_book(
    isbn: str = Form(...),
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    is_loaned: bool = Form(False),
    loaned_to: str = Form("")
):
    books = load_books()

    # Check for duplicate ISBN
    for b in books:
        if b["isbn"] == isbn:
            return templates.TemplateResponse(
                request=None,
                name="books/book_form.html",
                context={
                    "editing": False,
                    "book": None,
                    "book_isbn": None,
                    "error": f"ISBN {isbn} already exists!"
                }
            )

    new_book = {
        "isbn": isbn,
        "title": title,
        "author": author,
        "year": year,
        "is_loaned": is_loaned,
        "loaned_to": loaned_to if is_loaned else None
    }
    books.append(new_book)
    with open(BOOKS_FILE, "w") as f:
        json.dump(books, f, indent=4)
    return RedirectResponse("/books/landing", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/edit/{book_isbn}", response_class=HTMLResponse)
async def edit_book_form(request: Request, book_isbn: str):
    books = load_books()
    book = None
    for b in books:
        if b["isbn"] == book_isbn:
            book = b
            break
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse(
        request=request,
        name="books/book_form.html",
        context={"editing": True, "book": book, "book_isbn": book_isbn}
    )

@router.post("/{book_isbn}")
async def update_book(
    book_isbn: str,
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    is_loaned: bool = Form(False),
    loaned_to: str = Form("")
):
    books = load_books()
    for i, b in enumerate(books):
        if b["isbn"] == book_isbn:
            books[i] = {
                "isbn": book_isbn,
                "title": title,
                "author": author,
                "year": year,
                "is_loaned": is_loaned,
                "loaned_to": loaned_to if is_loaned else None
            }
            with open(BOOKS_FILE, "w") as f:
                json.dump(books, f, indent=4)
            return RedirectResponse("/books/landing", status_code=status.HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=404, detail="Book not found")

@router.get("/delete/{book_isbn}", response_class=HTMLResponse)
async def confirm_delete_book(request: Request, book_isbn: str):
    books = load_books()
    book = None
    for b in books:
        if b["isbn"] == book_isbn:
            book = b
            break
    return templates.TemplateResponse(
        request=request,
        name="books/book_delete.html",
        context={"book": book, "book_isbn": book_isbn}
    )

@router.post("/delete/{book_isbn}")
async def delete_book(book_isbn: str):
    books = load_books()
    for i, b in enumerate(books):
        if b["isbn"] == book_isbn:
            books.pop(i)
            with open(BOOKS_FILE, "w") as f:
                json.dump(books, f, indent=4)
            return RedirectResponse("/books/landing", status_code=status.HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=404, detail="Book not found")
