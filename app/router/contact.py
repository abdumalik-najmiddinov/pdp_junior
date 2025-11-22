import os
import shutil
from fastapi import APIRouter
from fastapi import Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

from app.bot import bot, CHAT_ID
from app.model import db,  Contact

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/media"


@router.get("/contact.html", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html",
                                      {"request": request})


@router.post("/contact.html")
async def create_register(request: Request):
    form = await request.form()

    your_name = form.get("your_name")
    gmail = form.get("gmail")
    subject = form.get("subject")
    message = form.get("message")

    contact = Contact(
        your_name=your_name,
        gmail=gmail,
        subject=subject,
        message=message
    )
    db.add(contact)
    db.commit()

    text = f"""Ismi : {your_name},
Gmail : {gmail},
Subject : {subject},
Message : {message}"""
    await bot.send_message(chat_id=CHAT_ID,
                           text=text,
                           parse_mode="HTML")

    return RedirectResponse("/", status_code=HTTP_302_FOUND)
