import logging

from pathlib import Path

# C:\Users\Alexey\Desktop\Python\Stepic_Suren\fastapi-url-shortener\url-shortener\core\config.py
BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILEPATH = BASE_DIR / "short-urls.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# Never store real tokens here!
# Only fake values
API_TOKENS: frozenset[str] = frozenset(
    {
        "fMm9eOevFKZUuRZlA-Lagw",
        "Gv70ciWBJErh_4Z2HB9l4g",
    }
)

# Only for demo!
# no real users in code!!
USERS_DB: dict[str, str] = {
    # username: password
    "sam": "password",
    "bob": "qwerty",
}
