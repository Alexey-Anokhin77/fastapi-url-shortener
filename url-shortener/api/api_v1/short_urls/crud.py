__all__ = (
    "ShortUrlAlreadyExistsError",
    "storage",
)

import logging

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)

log = logging.getLogger(__name__)


redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_SHORT_URLS,
    decode_responses=True,
)


# Класс для ошибки
class ShortUrlBaseError(Exception):
    """
    Base exception for short url CRUD actions.
    """


class ShortUrlAlreadyExistsError(ShortUrlBaseError):
    """
    Raised on short url creation if such slug already exists.
    """


# Создаем класс со словарем, в котором будем вытаскивать ссылку по slug-ключу
class ShortUrlsStorage(BaseModel):

    def save_short_url(self, short_url: ShortUrl) -> None:
        redis.hset(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    # Метод получения slug ключей
    def get(self) -> list[ShortUrl]:
        return [
            ShortUrl.model_validate_json(value)
            for value in redis.hvals(name=config.REDIS_SHORT_URLS_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        if data := redis.hget(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=slug,
        ):
            return ShortUrl.model_validate_json(data)
        return None

    def exist(self, slug: str) -> bool:
        result = redis.hexists(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=slug,
        )
        return bool(result)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.save_short_url(short_url)
        log.info("Created short url %s")
        return short_url

    def create_or_raise_if_exist(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        if not self.exist(short_url_in.slug):
            return self.create(short_url_in)

        log.info("Short URL can not be created!")
        raise ShortUrlAlreadyExistsError(short_url_in.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(config.REDIS_SHORT_URLS_HASH_NAME, slug)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self.save_short_url(short_url)
        return short_url

    def partial_update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        self.save_short_url(short_url)
        return short_url


storage = ShortUrlsStorage()
