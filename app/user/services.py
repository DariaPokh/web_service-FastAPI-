from fastapi import HTTPException

from . import tokenizator
from google.oauth2 import id_token
from google.auth.transport import requests

from . import schemas, models


GOOGLE_CLIENT_ID = "602538892345-9jk0h41g67f33sp3kled4apcb42m0ndv.apps.googleusercontent.com"


async def create_user(user: schemas.UserCreate) -> models.Users:
    _user = await models.Users.objects.get_or_create(**user.dict(exclude={"token"}))
    return _user


async def google_auth(user: schemas.UserCreate) -> tuple:
    try:
        idinfo = id_token.verify_oauth2_token(user.token, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(403, "Bad code")
    user = await create_user(user)
    internal_token = tokenizator.create_token(user.id)
    return user.id, internal_token.get("access_token")
