from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from repository import Repository
from schemas import Message, User


router = APIRouter(
    prefix="/api"
)

templates = Jinja2Templates(
    directory="templates"
)

router_templates = APIRouter(
    prefix="/templates"
)

router_user = APIRouter(
    prefix="/users"
)

# Маршрут для обработки данных из формы
@router.post("/submit-form")
async def submit_form(
    message: Message
):
    message_id = await Repository.add_one(message)
    return JSONResponse(content={"message": "Данные успешно сохранены"}, status_code=200)

@router_templates.get("/index.html")
async def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="index.html")
    
@router_templates.get("/about.html")
async def read_about(request:Request):
    return templates.TemplateResponse(request=request,
    name="about.html")

@router_templates.get("/form_data.html")
async def read_form_data(request:Request):
    return templates.TemplateResponse(request=request,
    name="form_data.html")

@router_user.get("/login.html")
async def read_login(request:Request):
    return templates.TemplateResponse(request=request,
    name="login.html")


# @router_user.post("")
# async def create_user(username: str, email: str, password: str):
#     user = User(username=username, email=email, password=password)
#     query = User.__table__.insert().values(username=username, email=email, password=password)
#     await database.execute(query)
#     return {"message": "User created successfully"}