from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import json


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Модель данных для сообщения от формы
class Message(BaseModel):
    name: str
    email: str
    message: str

# Функция для записи данных в файл JSON
def write_to_json(data):
    with open("messages.json", "a") as file:
        json.dump(data.dict(), file)
        file.write("\n")

# Маршрут для обработки данных из формы и записи их в файл JSON
@app.post("/submit-form")
async def submit_form(data: Message):
    write_to_json(data)
    return JSONResponse(content={"message": "Данные успешно сохранены"}, status_code=200)

@app.get("/index.html")
def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="index.html")

@app.get("/about.html")
def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="about.html")

@app.get("/form_data.html")
def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="form_data.html")