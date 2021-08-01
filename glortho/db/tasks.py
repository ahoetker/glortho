from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError
import logging
from fastapi import FastAPI
from databases import Database

from glortho.api.dependencies.settings import get_settings
from glortho.api.dependencies.user import UsersRepository
from glortho.models.user import (
    UserCreateHashedPassword,
    UserPublic,
)
from glortho.util.authentication import get_password_hash


logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    settings = get_settings()

    if settings.database_url.scheme == "postgresql":
        database = Database(
            settings.database_url, min_size=2, max_size=10,
        )
    else:
        database = Database(settings.database_url)

    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")


async def create_first_admin_user(app: FastAPI) -> None:
    settings = get_settings()
    users_repository = UsersRepository(db=app.state._db)
    first_admin_user = UserCreateHashedPassword(
        username=settings.first_admin_username,
        email=settings.first_admin_email,
        full_name=settings.first_admin_fullname,
        disabled=False,
        password=settings.first_admin_password,
        hashed_password=get_password_hash(settings.first_admin_password),
    )
    try:
        user = await users_repository.create_user(new_user=first_admin_user)
        logger.info(f"Created initial admin user: {user.username}")
    except UniqueViolationError:
        logger.info(
            f"Using existing initial admin user: {settings.first_admin_username}"
        )
    except IntegrityError:
        logger.info(
            f"Using existing initial admin user: {settings.first_admin_username}"
        )

