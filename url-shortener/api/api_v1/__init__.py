from fastapi import APIRouter

from api.api_v1.short_urls.views import router as short_urls_router

router = APIRouter(
    prefix="/v_1",
)

router.include_router(short_urls_router)
