from redis import Redis

from core import config
from core.config import settings

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=config.REDIS_DB,
    decode_responses=True,
)


def add(a: int, b: int) -> int:
    return a + b


def main() -> None:

    print(redis.ping())
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


if __name__ == "__main__":
    main()
