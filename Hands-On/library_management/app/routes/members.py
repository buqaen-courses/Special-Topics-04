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
MEMBERS_FILE = "members.json"
ITEMS_PER_PAGE = 5

def load_members():
    if not os.path.exists(MEMBERS_FILE):
        return []
    with open(MEMBERS_FILE, "r") as f:
        return json.load(f)

def next_member_id(members):
    if not members:
        return "M001"
    max_num = max(int(m["member_id"][1:]) for m in members)
    return f"M{max_num + 1:03d}"

@router.get("/landing", response_class=HTMLResponse)
async def members_landing(
    request: Request,
    sort: str = Query("default", pattern="^(default|name|email)$"),
    page: int = Query(1, ge=1),
    search: str = Query(None)
):
    members = load_members()

    # Step 1: Search filter
    if search:
        search_lower = search.lower()
        filtered = []
        for m in members:
            if (search_lower in m["name"].lower() or
                search_lower in m["email"].lower() or
                search_lower in m["member_id"].lower()):
                filtered.append(m)
        members = filtered

    # Step 2: Sort
    if sort == "name":
        members = sorted(members, key=lambda x: x["name"].lower())
    elif sort == "email":
        members = sorted(members, key=lambda x: x["email"].lower())

    # Step 3: Paginate
    total_items = len(members)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

    if page > total_pages and total_pages > 0:
        search_param = f"&search={search}" if search else ""
        return RedirectResponse(
            url=f"/members/landing?sort={sort}&page={total_pages}{search_param}",
            status_code=303
        )

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    paginated_members = members[start:end]

    return templates.TemplateResponse(
        request=request,
        name="members/members_landing.html",
        context={
            "members": paginated_members,
            "current_sort": sort,
            "current_page": page,
            "total_pages": total_pages,
            "items_per_page": ITEMS_PER_PAGE,
            "search": search
        }
    )

@router.get("/add", response_class=HTMLResponse)
async def add_member_form(request: Request):
    members = load_members()
    next_id = next_member_id(members)
    return templates.TemplateResponse(
        request=request,
        name="members/member_form.html",
        context={"editing": False, "member": None, "member_id": next_id}
    )

@router.post("/")
async def create_member(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form("")
):
    members = load_members()
    new_id = next_member_id(members)
    new_member = {
        "member_id": new_id,
        "name": name,
        "email": email,
        "phone": phone
    }
    members.append(new_member)
    with open(MEMBERS_FILE, "w") as f:
        json.dump(members, f, indent=4)
    return RedirectResponse("/members/landing", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/edit/{member_id}", response_class=HTMLResponse)
async def edit_member_form(request: Request, member_id: str):
    members = load_members()
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return templates.TemplateResponse(
        request=request,
        name="members/member_form.html",
        context={"editing": True, "member": member, "member_id": member_id}
    )

@router.post("/{member_id}")
async def update_member(
    member_id: str,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form("")
):
    members = load_members()
    for i, m in enumerate(members):
        if m["member_id"] == member_id:
            members[i] = {
                "member_id": member_id,
                "name": name,
                "email": email,
                "phone": phone
            }
            with open(MEMBERS_FILE, "w") as f:
                json.dump(members, f, indent=4)
            return RedirectResponse("/members/landing", status_code=status.HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=404, detail="Member not found")

@router.get("/delete/{member_id}", response_class=HTMLResponse)
async def confirm_delete_member(request: Request, member_id: str):
    members = load_members()
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    return templates.TemplateResponse(
        request=request,
        name="members/member_delete.html",
        context={"member": member, "member_id": member_id}
    )

@router.post("/delete/{member_id}")
async def delete_member(member_id: str):
    members = load_members()
    for i, m in enumerate(members):
        if m["member_id"] == member_id:
            members.pop(i)
            with open(MEMBERS_FILE, "w") as f:
                json.dump(members, f, indent=4)
            return RedirectResponse("/members/landing", status_code=status.HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=404, detail="Member not found")
