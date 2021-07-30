from fastapi import APIRouter
from glortho.api.routes.users import (
    router as users_router,
)

router = APIRouter()
router.include_router(users_router, prefix="", tags=["users"])
