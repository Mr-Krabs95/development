from pydantic import BaseModel

# Модель данных для сообщения от формы
class Message(BaseModel):
    name: str
    email: str
    message: str

# Модель данных для регистрации пользователя
class User(BaseModel):
    username: str
    hashed_password: str
