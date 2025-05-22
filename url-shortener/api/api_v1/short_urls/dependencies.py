import logging

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
)
from starlette import status

from .crud import storage
from schemas.short_url import ShortUrl

log = logging.getLogger(__name__)

UNSAFE_METHOD = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


def prefetch_short_urls(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL{slug!r} not found",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    # сначала код до входа внутрь view функции
    yield
    # код после покидания view функции
    if request.method in UNSAFE_METHOD:
        log.info("Add background task to save storage")
        background_tasks.add_task(storage.save_state)
