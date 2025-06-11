from redis import Redis

from core import config

r = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def main():
    print(r.ping())
    r.set("name", "Alexey")
    r.set("foo", "bar")
    r.set("number", "42")
    print("name", r.get("name"))
    print(
        [
            r.get("foo"),
            r.get("number"),
            r.get("spam"),
        ]
    )
    r.delete("name")
    print("name", r.get("name"))


if __name__ == "__main__":
    main()
