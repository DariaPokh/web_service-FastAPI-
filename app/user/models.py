import ormar
from database import MainMata


class Users(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.UUID(primary_key=True, uuid_format='string')
    username: str = ormar.String(max_length=100)
    phone: str = ormar.String(max_length=14)
    email: str = ormar.String(index=True, unique=True, nullable=False, max_length=255)
