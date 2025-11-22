from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from app.model import db, User
from app.schemes import UserCreate
from pydantic import ValidationError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def create_register(request: Request):
    form = await request.form()

    gmail = form.get("gmail")
    password = form.get("password")
    confirm_password = form.get("confirm_password")

    try:
        data = UserCreate(
            gmail=gmail,
            password=password,
            confirm_password=confirm_password
        )
    except ValidationError as e:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": e.errors()[0]["msg"]
        })

    old_user = db.query(User).filter(User.gmail == gmail).first()
    if old_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Bu email allaqachon ro‘yxatdan o‘tgan!"
        })

    user = User(
        gmail=gmail,
        password=password,
        confirm_password=confirm_password,
        is_active=True
    )

    db.add(user)
    db.commit()

    return RedirectResponse("/login", status_code=HTTP_302_FOUND)


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_user(request: Request):
    form = await request.form()

    gmail = form.get("gmail")
    password = form.get("password")

    user = db.query(User).filter(User.gmail == gmail).first()

    if not user or user.password != password:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Email yoki parol noto‘g‘ri!"
        })

    response = RedirectResponse("/", status_code=HTTP_302_FOUND)
    response.set_cookie("user_id", str(user.id), httponly=True, samesite="lax")

    return response


