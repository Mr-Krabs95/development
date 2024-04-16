from pydantic import BaseModel

class Settings:
    SECRET_KEY: str = "secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins
    COOKIE_NAME = "access_token"

# Модель данных для сообщения от формы
class Message(BaseModel):
    name: str
    email: str
    message: str

# Модель данных для регистрации пользователя
class User(BaseModel):
    username: str
    hashed_password: str
