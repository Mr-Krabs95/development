from database import new_session, MessagesTable
from schemas import Message
from sqlalchemy import select

class Repository:
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