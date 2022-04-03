from pydantic import BaseModel

from app.user.schemas import UserOut


class GetListImage(BaseModel):
    id: str
    request_code: str
    filename: str
    date_and_time: str


class GetImage(GetListImage):
    user: UserOut


class Message(BaseModel):
    message: str
