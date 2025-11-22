import os
import shutil
from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.model import db, Course

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/media"


@router.get("/course-create", response_class=HTMLResponse)
async def form_course(request: Request):
    return templates.TemplateResponse(
        "course_create.html",
        {"request": request}
    )


@router.post("/course-create")
async def create_course(request: Request):
    form = await request.form()

    course_name = form.get("course_name")
    about = form.get("about")
    age_limit = int(form.get("age_limit"))
    price = int(form.get("price"))
    image: UploadFile = form.get("image")

    file_path = os.path.join(UPLOAD_DIRECTION, image.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    course = Course(
        image=image.filename,
        course_name=course_name,
        about=about,
        age_limit=age_limit,
        price=price
    )

    db.add(course)
    db.commit()
    db.close()

    return RedirectResponse("/class.html", status_code=HTTP_302_FOUND)
