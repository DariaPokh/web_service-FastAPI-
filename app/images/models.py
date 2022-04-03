import ormar
from datetime import datetime
from database import MainMata


class Image(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)
    request_code: str = ormar.String(max_length=500)
    filename: str = ormar.String(max_length=500)
    date_and_time: str = ormar.String(max_length=100, default=datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
