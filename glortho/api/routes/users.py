from asyncpg.exceptions import UniqueViolationError
from datetime import timedelta
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from glortho.api.dependencies.database import get_repository
from glortho.api.dependencies.settings import get_settings
from glortho.api.dependencies.user import (
    get_current_active_user,
)
from glortho.core.config import Settings
from glortho.db.repositories.users import UsersRepository
from glortho.models.token import Token
from glortho.models.user import (
    User,
    UserPublic,
    UserCreate,
    UserCreateHashedPassword,
)
from glortho.util.authentication import (
    authenticate_user,
    get_password_hash,
)
from glortho.util.token import create_access_token

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    settings: Settings = Depends(get_settings),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    user = await authenticate_user(
        username=form_data.username, password=form_data.password, users_repo=users_repo
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users", response_model=UserPublic)
async def create_user(
    new_user: UserCreate = Body(...),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    hashed_password = get_password_hash(new_user.password)
    new_user_hashed_password = UserCreateHashedPassword(
        hashed_password=hashed_password, **new_user.dict()
    )
    try:
        user = await users_repo.create_user(new_user=new_user_hashed_password)
        return user.dict()
    except UniqueViolationError as e:
        raise HTTPException(status_code=409, detail=str(e.detail))


@router.get("/users/me/", response_model=UserPublic)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
