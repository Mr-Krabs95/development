from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db, delete_db, create_users, delete_users
from routers import router, router_templates, router_user, token
from rich.console import Console

print("hello")

console = Console()



@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_db()
    await delete_users()
    print("Базы очищены")
    await create_db() # await - ждем выполнения асинхронной функции create_db
    await create_users()
    print("Базы готовы к работе")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.include_router(router_templates)
app.include_router(router_user)
app.include_router(token)
