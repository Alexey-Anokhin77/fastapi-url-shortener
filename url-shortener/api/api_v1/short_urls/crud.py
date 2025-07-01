import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from core.config import SHORT_URLS_STORAGE_FILEPATH
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)

log = logging.getLogger(__name__)


redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_SHORT_URLS,
    decode_responses=True,
)


# Создаем класс со словарем, в котором будем вытаскивать ссылку по slug-ключу
class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    # Метод сохранения данных локально на жесткий диск
    def save_state(self) -> None:
        for _ in range(30_000):
            SHORT_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))

        SHORT_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Saved short urls to storage file.")

    # Кастомный инициализатор на проверку существования и чтения файла
    @classmethod
    def from_state(cls) -> "ShortUrlsStorage":
        if not SHORT_URLS_STORAGE_FILEPATH.exists():
            log.info("Short urls to storage file doesn't exist!")
            return ShortUrlsStorage()
        return cls.model_validate_json(SHORT_URLS_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = ShortUrlsStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error.")
            return

        # обновление свойства напрямую
        # если будут новые свойства,
        # то их тоже надо обновить.
        self.slug_to_short_url.update(
            data.slug_to_short_url,
        )
        log.warning("Recovered data from storage file.")

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

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.save_short_url(short_url)
        log.info("Created short url %s")
        return short_url

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
    ):
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        self.save_short_url(short_url)
        return short_url


storage = ShortUrlsStorage()
