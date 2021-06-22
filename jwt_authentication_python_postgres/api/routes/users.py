from datetime import timedelta
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from jwt_authentication_python_postgres.api.dependencies.database import get_repository
from jwt_authentication_python_postgres.api.dependencies.user import (
    get_current_active_user,
)
from jwt_authentication_python_postgres.db.repositories.users import UsersRepository
from jwt_authentication_python_postgres.core.config import get_settings, Settings
from jwt_authentication_python_postgres.models.token import Token
from jwt_authentication_python_postgres.models.user import User, UserPublic
from jwt_authentication_python_postgres.util.authentication import authenticate_user
from jwt_authentication_python_postgres.util.token import create_access_token

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


@router.get("/users/me/", response_model=UserPublic)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
