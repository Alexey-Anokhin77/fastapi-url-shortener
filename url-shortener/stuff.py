
from redis import Redis

from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def add(a: int, b: int) -> int:
    return a + b


def main() -> None:

    print(redis.ping())
    redis.set("name", "Alexey")
    redis.set("foo", "bar")
    redis.set("number", "42")
    print("name", redis.get("name"))
    print(
        [
            redis.get("foo"),
            redis.get("number"),
            redis.get("spam"),
        ],
    )
    redis.delete("name")
    print("name", redis.get("name"))
