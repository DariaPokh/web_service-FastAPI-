import os
import uuid
from datetime import datetime
from typing import List
import aiofiles
import psycopg2

from fastapi import FastAPI, UploadFile, File, APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.user.api import templates
from .schemas import GetImage, GetListImage
from .models import Image

app = FastAPI()

image_router = APIRouter(prefix='/images', tags=["images"])
templates = Jinja2Templates(directory="templates")


@image_router.post("/post")
async def post(files: List[UploadFile] = File(...)):
    request_code = str(int(datetime.now().timestamp()))
    directory = f"app/data/{datetime.now().strftime('%Y%m%d')}"
    if not os.path.exists(directory):
        os.mkdir(directory)
    for image in files:
        if image.content_type != "image/jpeg":
            raise HTTPException(status_code=418, detail="Неверный формат. Загрузите jpeg.")
        else:
            filename = str(uuid.uuid4()) + ".jpg"
            await Image.objects.create(request_code=request_code, filename=filename)
            async with aiofiles.open(f"{directory}/{filename}", "wb") as buffer:
                data = await image.read()
                await buffer.write(data)
    return {f"Файлы загружены. Код запроса: {request_code}"}


@image_router.get("/get/{request_code}", response_model=List[GetListImage])
async def get(request_code: str):
    return await Image.objects.filter(request_code=request_code).all()


@image_router.delete("/delete/{request_code}", response_model=List[Image])
async def get(request_code: str):
    connection = psycopg2.connect(database="web_services",
                                  user="root",
                                  password="root",
                                  host="127.0.0.1",
                                  port="5432")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM public.images WHERE request_code = '{request_code}'")
    rows = cursor.fetchall()
    temp_folder = datetime.strptime(rows[0][3], "%d.%m.%Y %H:%M:%S")
    folder = datetime.strftime(temp_folder, "%Y%m%d")
    for row in rows:
        os.remove(f"app/data/{folder}/{row[2]}")
    directory = f"app/data/{folder}"
    test = os.walk(directory)
    path, dirs, files = next(test)
    if not files:
        os.chdir("data/")
        os.remove(folder)
    return await Image.objects.delete(request_code=request_code)


@image_router.get("/404", response_class=HTMLResponse)
async def error_404(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})
