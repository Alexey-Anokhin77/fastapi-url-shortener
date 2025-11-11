import logging
from os import getenv
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# Путь к конфигу:
# C:\Users\Alexey\Desktop\Python\Stepic_Suren\
# fastapi-url-shortener\url-shortener\core\config.py

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


# Only for demo!
# no real users in code!!
# USERS_DB: dict[str, str] = {
#     # username: password
#     "sam": "password",
#     "bob": "qwerty",
# }
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2
REDIS_DB_SHORT_URLS = 3

REDIS_TOKENS_SET_NAME = "tokens"
REDIS_SHORT_URLS_HASH_NAME = "short-urls"

class LoggingConfig(BaseModel):
    log_level: int = logging.INFO
    log_format: str = LOG_FORMAT
    date_format: str ="%Y-%m-%d %H:%M:%S"



class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379

class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()

class Settings(BaseSettings):
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


# noinspection PyArgumentList
settings = Settings()

