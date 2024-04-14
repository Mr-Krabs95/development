from database import new_session, user_session, MessagesTable, UsersTable
from schemas import Message, User
from sqlalchemy import select

class Repository:
    # -------------------------------------------------------------
    # Методы для базы сообщений
    # -------------------------------------------------------------
    @classmethod
    async def add_one(cls, data: Message) -> int:
        async with new_session() as session:
            message_dict = data.model_dump()
            message = MessagesTable(**message_dict)
            session.add(message)
            await session.flush()
            await session.commit()
            return message.id   
            
    @classmethod
    async def get_all(cls):
        async with new_session() as session:
            query = select(MessagesTable)
            result = await session.execute(query)
            message_model = result.scalars().all()
            return message_model

    # -------------------------------------------------------------
    # Методы для базы пользователей
    # -------------------------------------------------------------
    @classmethod
    async def add_user(cls, data: User) -> int:
        async with user_session() as session:
            user_dict = data.model_dump()
            user = UsersTable(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
        
    @classmethod
    async def get_user_by_username(cls, username: str):
        async with user_session() as session:
            query = select(UsersTable).filter(UsersTable.username == username)
            result = await session.execute(query)
            user_model = result.one_or_none()
            return user_model
        