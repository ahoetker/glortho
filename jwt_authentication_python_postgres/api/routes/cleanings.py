from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED

from jwt_authentication_python_postgres.models.cleaning import (
    CleaningCreate,
    CleaningPublic,
)
from jwt_authentication_python_postgres.db.repositories.cleanings import (
    CleaningsRepository,
)
from jwt_authentication_python_postgres.api.dependencies.database import get_repository

router = APIRouter()


@router.get("/")
async def get_all_cleanings(
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> List[dict]:
    cleanings = await cleanings_repo.get_cleanings()
    return cleanings


@router.get("/{id}", response_model=CleaningPublic)
async def get_cleaning(
    id: int,
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    try:
        cleaning = await cleanings_repo.get_cleaning(id=id)
        return cleaning
    except TypeError:
        raise HTTPException(status_code=404, detail="Item not found")


@router.post(
    "/",
    response_model=CleaningPublic,
    name="cleanings:create-cleaning",
    status_code=HTTP_201_CREATED,
)
async def create_new_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=True),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning)
    return created_cleaning


@router.delete("/{id}", response_model=CleaningPublic)
async def get_cleaning(
    id: int,
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    try:
        cleaning = await cleanings_repo.delete_cleaning(id=id)
        return cleaning
    except TypeError:
        raise HTTPException(status_code=404, detail="Item not found")
