from passlib.context import CryptContext
from glortho.models.user import UserInDB
from fastapi import Depends

from glortho.db.repositories.users import (
    UsersRepository,
)
from glortho.api.dependencies.database import get_repository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(
    username: str,
    password: str,
    users_repo: UsersRepository,
) -> UserInDB:
    try:
        user = await users_repo.get_user(username=username)
    except TypeError:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
