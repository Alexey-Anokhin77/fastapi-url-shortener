import random
import string

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.short_url import ShortUrl, ShortUrlCreate


def test_create_short_url(auth_client: TestClient) -> None:
    url = app.url_path_for("create_short_url")
    data: dict[str, str] = ShortUrlCreate(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=10,
            ),
        ),
        description="Some description",
        target_url="https://www.example.com",
    ).model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = {
        "slug": response_data["slug"],
        "description": response_data["description"],
        "target_url": response_data["target_url"],
    }
    assert received_values == data, response_data


def test_create_short_url_already_exist(
    auth_client: TestClient,
    short_url: ShortUrl,
) -> None:
    short_url_create = ShortUrlCreate(**short_url.model_dump())
    data = short_url_create.model_dump(mode="json")
    url = app.url_path_for("create_short_url")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Short URL with slug={short_url.slug!r} already exist"
    assert response_data["detail"] == expected_error_detail, response.text
