import random
import string
from os import getenv
from unittest import TestCase

from api.api_v1.short_urls.crud import storage
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    raise OSError(msg)


class ShortUrlsStorageUpdateTestCase(TestCase):
    # Добавляем и сохраняем экземпляр, который будем использовать постоянно
    def setUp(self) -> None:
        self.short_url = self.create_short_url()

    # Создаем метод чистки базы
    def tearDown(self) -> None:
        storage.delete(self.short_url)

    def create_short_url(self) -> ShortUrl:
        short_url_in = ShortUrlCreate(
            slug="".join(
                random.choices(
                    string.ascii_letters,
                    k=8,
                ),
            ),
            description="Some description",
            target_url="https://www.example.com",
        )
        return storage.create(short_url_in)

    def test_update(self) -> None:
        short_url_update = ShortUrlUpdate(
            **self.short_url.model_dump(),
        )
        source_description = self.short_url.description
        short_url_update.description *= 2
        updated_short_url = storage.update(
            short_url=self.short_url,
            short_url_in=short_url_update,
        )
        self.assertNotEqual(
            source_description,
            updated_short_url.description,
        )

        self.assertEqual(
            short_url_update,
            ShortUrlUpdate(**updated_short_url.model_dump()),
        )

    def test_update_partial(self) -> None:
        short_url_partial_update = ShortUrlPartialUpdate(
            description=self.short_url.description * 2,
        )
        source_description = self.short_url.description

        updated_short_url = storage.partial_update(
            short_url=self.short_url,
            short_url_in=short_url_partial_update,
        )

        self.assertNotEqual(
            source_description,
            updated_short_url.description,
        )

        self.assertEqual(
            short_url_partial_update.description,
            updated_short_url.description,
        )
