from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from api.api_v1.short_urls.crud import ShortUrlAlreadyExistsError, storage
from api.api_v1.short_urls.dependencies import (
    api_token_or_user_basic_auth_required__for_unsafe_methods,
)
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlRead,
)

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
    dependencies=[
        # Depends(api_token_required_for_unsafe_methods),
        Depends(api_token_or_user_basic_auth_required__for_unsafe_methods),
    ],
    responses={
        # status.HTTP_204_NO_CONTENT: None,
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only  for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
)


@router.get(
    "/",
    response_model=list[ShortUrlRead],
)
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get()


# Создаем эндпоинт запроса
@router.post(
    "/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Conflict. Short URL with this slug already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Short URL with slug='example' already exists",
                    },
                },
            },
        },
    },
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrl:
    try:
        return storage.create_or_raise_if_exist(short_url_create)
    except ShortUrlAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Short URL with slug={short_url_create.slug!r} already exist",
        ) from None
