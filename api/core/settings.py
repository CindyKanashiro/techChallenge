from os import getenv
from dotenv import load_dotenv

load_dotenv(".env.example")  # remover em produção

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_TIME = int(getenv("ACCESS_TOKEN_EXPIRE_TIME"))  # minutes
ACCESS_TOKEN_REFRESH_TIME = int(getenv("ACCESS_TOKEN_REFRESH_TIME"))  # minutes

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 3

ADMIN_EMAIL = getenv("EMAIL_ADMIN")
ADMIN_PASSWORD = getenv("HASHED_ADMIN_PASSWORD")
