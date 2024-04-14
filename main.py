from fastapi import FastAPI
import json
from contextlib import asynccontextmanager
from database import create_db, delete_db, create_users, delete_users
from routers import router, router_templates, router_user
from rich.console import Console

console = Console()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_db()
    print("База сообщений очищена")
    await delete_users()
    print("База пользователей очищена")
    await create_db() # await - ждем выполнения асинхронной функции create_db
    print("База готова к работе")
    await create_users()
    print("База пользователей готова")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.include_router(router_templates)
app.include_router(router_user)
