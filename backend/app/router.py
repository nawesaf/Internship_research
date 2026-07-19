from fastapi import APIRouter

from app.routers.uploads import router as uploads_router
from app.routers.matching import router as matching_router

api_router = APIRouter()

api_router.include_router(
    uploads_router,
    prefix="/uploads",
    tags=["Uploads"],
)

api_router.include_router(
    matching_router,
    prefix="/matching",
    tags=["Matching"],
)