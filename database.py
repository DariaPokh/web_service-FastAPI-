import databases
import ormar
import sqlalchemy


POSTGRES_USER = "root"
POSTGRES_PASSWORD = "root"
POSTGRES_DB = "web_services"

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"

metadata = sqlalchemy.MetaData()
database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)


class MainMata(ormar.ModelMeta):
    metadata = metadata
    database = database

