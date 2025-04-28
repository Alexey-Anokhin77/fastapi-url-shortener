from fastapi import HTTPException
from starlette import status

from .crud import SHORT_URLS
from schemas.short_url import ShortUrl


def prefetch_short_urls(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = next(
        (url for url in SHORT_URLS if url.slug == slug),
        None,
    )
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL{slug!r} not found",
    )
