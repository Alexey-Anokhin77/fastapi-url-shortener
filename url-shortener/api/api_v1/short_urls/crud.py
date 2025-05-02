from pydantic import BaseModel, AnyHttpUrl

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
)


# Создаем класс со словарем, в котором будем вытаскивать ссылку по slug-ключу
class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    # Метод получения slug ключей
    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.slug_to_short_url[short_url.slug] = short_url
        return short_url


storage = ShortUrlsStorage()

storage.create(
    ShortUrlCreate(
        target_url=AnyHttpUrl("https://example.com"),
        slug="example",
    ),
)
storage.create(
    ShortUrlCreate(
        target_url=AnyHttpUrl("https://google.com"),
        slug="search",
    ),
)
