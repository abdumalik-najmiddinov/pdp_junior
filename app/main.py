import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from app.router import read, contact, register, create_course, class_yozilish, techaer_create
from app.bot import dp, bot, setup_webhook
from fastapi.responses import JSONResponse

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/media"
os.makedirs(UPLOAD_DIRECTION, exist_ok=True)
app.mount("/static", StaticFiles(directory='app/static'), name="static")
app.mount("/media", StaticFiles(directory="app/media"), name="media")

app.include_router(read.router)
app.include_router(contact.router)
app.include_router(register.router)
app.include_router(create_course.router)
app.include_router(class_yozilish.router)
app.include_router(techaer_create.router)





@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    await dp.feed_raw_update(bot, data)
    return JSONResponse({"ok": True})


# --- FastAPI ishga tushganda webhookni o‘rnatish ---
@app.on_event("startup")
async def on_startup():
    await setup_webhook()
