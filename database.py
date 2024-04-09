"""Импортирование асинхронного движка,
который отправляет запрос в базу данных."""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    "sqlite+aiosqlite:///database.db" # асинхронный драйвер
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class MessagesTable(Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    message: Mapped[str]

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_db():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)