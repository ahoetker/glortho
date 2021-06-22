from fastapi import APIRouter
from jwt_authentication_python_postgres.api.routes.cleanings import (
    router as cleanings_router,
)
from jwt_authentication_python_postgres.api.routes.users import (
    router as users_router,
)

router = APIRouter()
router.include_router(cleanings_router, prefix="/cleanings", tags=["cleanings"])
router.include_router(users_router, prefix="", tags=["users"])
