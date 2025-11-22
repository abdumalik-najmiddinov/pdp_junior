import os
import shutil

from fastapi import APIRouter, Request, Form, UploadFile, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.model import Teacher, Registration, db, get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIRECTION = 'app/media'
@router.get("/teacher-create", response_class=HTMLResponse)
async def form_teacher(request: Request):
    return templates.TemplateResponse("teacher_create.html", {"request": request})


@router.post("/teacher-create")
async def create_teacher(request: Request):
    form = await request.form()

    name = form.get("name")
    position = form.get("position")
    image: UploadFile = form.get("image")
    file_path = os.path.join(UPLOAD_DIRECTION, image.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    teacher = Teacher(name=name, position=position, image=image.filename)

    db.add(teacher)
    db.commit()
    db.close()
    return RedirectResponse("/team.html", status_code=HTTP_302_FOUND)


# @router.get("/team.html", response_class=HTMLResponse)
# async def get_team(request: Request):
#     teachers = db.query(Teacher).all()
#     return templates.TemplateResponse("team.html", {"request": request, "teachers": teachers})
#


@router.get("/team.html", response_class=HTMLResponse)
async def shop_func(request: Request, page: int = 1, db: Session = Depends(get_db)):
    per_page = 4
    offset_value = (page - 1) * per_page
    teachers = db.query(Teacher).offset(offset_value).limit(per_page).all()
    total = db.query(Teacher).count()
    total_pages = (total + per_page - 1) // per_page

    return templates.TemplateResponse("team.html", {
        "request": request,
        "page": page,
        "total_pages": total_pages,
        "teachers": teachers
    })


