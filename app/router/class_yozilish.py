import os
import shutil
from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.model import db, Course, Registration

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/media"




@router.post("/class.html")
async def create_register(request: Request):
    form = await request.form()

    name = form.get("name") or ""
    phone = form.get("phone") or ""
    course_id = form.get("course_id") or ""

    registration = Registration(
        name=name,
        phone=phone,
        course_id=int(course_id)
    )

    db.add(registration)
    db.commit()
    db.refresh(registration)

    # Redirect orqali register sahifasiga qaytish
    return RedirectResponse("/class.html", status_code=HTTP_302_FOUND)
