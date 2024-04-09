
from pydantic import BaseModel


# Модель данных для сообщения от формы
class Message(BaseModel):
    name: str
    email: str
    message: str