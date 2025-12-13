from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

from app.model import Course, get_db

from app.model import db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/media"


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/index.html", response_class=HTMLResponse)
async def index(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})




@router.get("/single.html", response_class=HTMLResponse)
async def single_page(request: Request):
    return templates.TemplateResponse("single.html", {"request": request})


@router.get("/about.html", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/blog.html", response_class=HTMLResponse)
async def blog_page(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})


@router.get("/class.html", response_class=HTMLResponse)
async def class_page(request: Request):
    courses = db.query(Course).all()
    return templates.TemplateResponse("class.html", {"request": request, "courses": courses})





@router.get("/gallery.html", response_class=HTMLResponse)
async def gallery_page(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request})
