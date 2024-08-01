from pydantic.v1 import BaseSettings
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
import glob
import json
import os.path


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str
    OPENAI_API_KEY: str

    class Config:
        env_file = r'.env'


load_dotenv(override=True)
MIDDLEWARE_KEY = os.environ.get("MIDDLEWARE_KEY", None)
API_KEY = os.environ.get("OPENAI_API_KEY")
CLIENT_ID = os.environ.get('client-id', None)
CLIENT_SECRET = os.environ.get('client-secret', None)
MIDDLEWARE_KEY = os.environ.get("EMAIL_PASSWORD", None)
CAPTCHA_SECRET_KEY = os.environ.get("CAPTCHA_SECRET_KEY", None)
BOT_TOKEN = os.environ.get("TOKEN", None)
settings = Settings()

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME")
DATABASE_PORT = os.environ.get("DATABASE_PORT")

ALEMBIC_HOST = os.environ.get("POSTGRES_HOST_ALEMBIC")


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}"
    f":{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOSTNAME}:{DATABASE_PORT}/"
    f"{POSTGRES_DB}"
)

ALEMBIC_SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}"
    f":{POSTGRES_PASSWORD}@"
    f"{ALEMBIC_HOST}:{DATABASE_PORT}/"
    f"{POSTGRES_DB}"
)

templates = Jinja2Templates(directory="templates")
whiteList = ['6210231417', '1020618396', '677977580']
app_language = "ru"
