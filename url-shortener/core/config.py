import logging
from pathlib import Path

# Путь к конфигу:
# C:\Users\Alexey\Desktop\Python\Stepic_Suren\
# fastapi-url-shortener\url-shortener\core\config.py

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILEPATH = BASE_DIR / "short-urls.json"

LOG_LEVEL = logging.INFO
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
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2
REDIS_DB_SHORT_URLS = 3

REDIS_TOKENS_SET_NAME = "tokens"
REDIS_SHORT_URLS_HASH_NAME = "short-urls"
