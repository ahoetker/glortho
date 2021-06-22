import logging
from fastapi import FastAPI, Depends
from databases import Database

from jwt_authentication_python_postgres.api.dependencies.settings import get_settings


logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    settings = get_settings()
    database = Database(
        settings.postgres_url, min_size=2, max_size=10
    )  # these can be configured in config as well
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
