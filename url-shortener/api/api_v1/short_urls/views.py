from typing import Annotated


from fastapi import (
    Depends,
    APIRouter,
    status,
)

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
)

from .crud import storage
from .dependencies import (
    prefetch_short_urls,
)

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
)


@router.get(
    "/",
    response_model=list[ShortUrl],
)
def read_short_urls_list():
    return storage.get()


# Создаем эндпоинт запроса
@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrl:
    return storage.create(short_url_create)


@router.get(
    "/{slug}/",
    response_model=ShortUrl,
)
def read_short_urls_details(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
) -> ShortUrl:
    return url
