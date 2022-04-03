import jwt
from jwt import PyJWTError
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN

from .models import Users

from .tokenizator import ALGORITHM, SECRET_KEY
from .schemas import TokenPayload


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


async def get_current_user(token: str = Security(reusable_oauth2)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Не удалось найти учетные данные"
        )
    user = await Users.objects.get_or_none(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


async def get_user(current_user: Users = Security(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return current_user
