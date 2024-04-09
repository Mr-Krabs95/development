from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from repository import Repository
from schemas import Message


router = APIRouter(
    prefix="/api"
)

templates = Jinja2Templates(
    directory="templates"
)

router_templates = APIRouter(
    prefix="/templates"
)

# Маршрут для обработки данных из формы
@router.post("/submit-form")
async def submit_form(
    message: Message
):
    message_id = await Repository.add_one(message)
    return JSONResponse(content={"message": "Данные успешно сохранены"}, status_code=200)

@router_templates.get("/index.html")
def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="index.html")
    
@router_templates.get("/about.html")
def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="about.html")

@router_templates.get("/form_data.html")
def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="form_data.html")