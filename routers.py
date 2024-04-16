from fastapi import APIRouter, Request, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from repository import Repository
from schemas import Message, User, Settings
from typing import Dict, Optional
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
import datetime as dt
from jose import JWTError, jwt
from passlib.handlers.sha2_crypt import sha512_crypt as crypto



templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/api")
router_templates = APIRouter(prefix="/templates")
router_user = APIRouter(prefix="/users")
token = APIRouter(prefix="/token")


settings = Settings()

# --------------------------------------------------------------------------
# Authentication logic
# --------------------------------------------------------------------------
class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    Этот класс взят непосредственно из FastAPI. 
    Единственное изменение в том, что аутентификация берётся из файла cookie,
    а не из шапки.
    """
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        # IMPORTANT: this is the line that differs from FastAPI. Here we use 
        # `request.cookies.get(settings.COOKIE_NAME)` instead of 
        # `request.headers.get("Authorization")`
        authorization: str = request.cookies.get(settings.COOKIE_NAME) 
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


async def create_access_token(data: Dict) -> str:
    """ 
    Создаёт токен доступа JWT
    Используется ранее созданный класс Settings
    """
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(username: str, plain_password: str) -> User:
    """
    Асинхронная ф-ця принимающая имя пользователя и парроль
    Возвращает объект пользователя в случае успешной аутентификации
    """
    user = await Repository.get_user_by_username(username)
    if not user:
        return False
    if not crypto.verify(plain_password, user.hashed_password): # хешированный пароль сравнивается с текстовым
        return False
    return user


async def decode_token(token: str) -> User:
    """
    Раскодирует JWT токен
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials"
    )
    token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    user = await Repository.get_user_by_username(username)
    return user


async def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> User:
    """
    Получает текущего пользователя из файлов cookie в запросе

    Use this function when you want to lock down a route so that only 
    authenticated users can see access the route.
    """
    user = decode_token(token)
    return user


async def get_current_user_from_cookie(request: Request) -> User:
    """
    Получает текущего пользователя из файлов cookie в запросе
    
    Use this function from inside other routes to get the current user. Good
    for views that should work for both logged in, and not logged in users.
    """
    token = request.cookies.get(settings.COOKIE_NAME)
    user = decode_token(token)
    return user


@token.post("")
async def login_for_access_token(
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, str]:
    """
    Аутентификация пользователя и выдача доступного токена
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"username": user.username})
    # полученный токен добавляется в куки
    response.set_cookie(
        key=settings.COOKIE_NAME, 
        value=f"Bearer {access_token}", 
        httponly=True
    )  
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}
# --------------------------------------------------------------------------
# END authentication logic
# --------------------------------------------------------------------------







# Маршрут для обработки данных из формы
@router.post("/submit-form")
async def submit_form(
    message: Message
):
    message_id = await Repository.add_one(message)
    return JSONResponse(content={"message": "Данные успешно сохранены"}, status_code=200)

# Маршрут для получения стартовой страницы
@router_templates.get("/index.html")
async def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="index.html")

# Маршрут для получения страницы входа/регистрации в личном кабинете
@router_user.get("/login.html")
async def read_login(request:Request):
    return templates.TemplateResponse(request=request,
    name="login.html")

