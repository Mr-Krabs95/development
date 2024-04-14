"""Импортирование асинхронного движка,
который отправляет запрос в базу данных."""

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# создание асинхронного движка для базы данных с сообщениями
engine = create_async_engine(
    "sqlite+aiosqlite:///database.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

# создание асинхронного движка для базы пользователей
users = create_async_engine(
    "sqlite+aiosqlite:///users.db"
)
user_session = async_sessionmaker(users, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class MessagesTable(Model):
    """Модель для хранения отправляемых сообщений из формы"""
    
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    message: Mapped[str]

class UsersTable(Model):
    """Модель для хранения информации о пользователях"""
    
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

async def create_db():
    """Создание базы сообщений"""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_db():
    """Удаление базы сообщений"""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

async def create_users():
    """Создание базы пользователей"""
    async with users.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_users():
    """Удаление базы пользователей"""
    async with users.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
