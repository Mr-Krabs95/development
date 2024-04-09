from fastapi import FastAPI
import json
from contextlib import asynccontextmanager
from database import create_db, delete_db
from routers import router, router_templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_db()
    print("База очищена")
    await create_db() # await - ждем выполнения асинхронной функции create_db
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.include_router(router_templates)


# # Функция для записи данных в файл JSON
# def write_to_json(data):
#     # Открываем файл JSON для добавления данных
#     with open("messages.json", "a") as file:
#         # Генерируем уникальный ID на основе текущего времени
#         unique_id = str(int(datetime.now().timestamp()))

#         # Создаем словарь с уникальным ID и данными из формы
#         entry = {"id": unique_id, **data.dict()}

#         # Записываем словарь в файл JSON
#         json.dump(entry, file)
#         file.write("\n")

# @app.post("/submit-form")
# async def submit_form(data: Message):
#     write_to_json(data)
#     return JSONResponse(content={"message": "Данные успешно сохранены"}, status_code=200)