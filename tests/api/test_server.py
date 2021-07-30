import logging
import os
import pytest
from httpx import AsyncClient
from databases import Database
from fastapi import FastAPI

from glortho.api import server
from glortho.api.dependencies.database import get_database
from glortho.core.config import Settings

logger = logging.getLogger(__name__)


def get_test_postgres_url():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    server = os.getenv("POSTGRES_SERVER")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    return f"postgresql://{user}:{password}@{server}:{port}/{db}"


async def override_get_database():
    database = Database(get_test_postgres_url(), min_size=2, max_size=10)
    try:
        await database.connect()
        return database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


def get_settings_override():
    return Settings(
        algorithm="HS256",
        secret_key="TestingKeyForConsistentHashes",
    )


app = server.get_application()
app.dependency_overrides[get_database] = override_get_database
app.dependency_overrides[server.get_settings] = get_settings_override

test_user = {
    "username": "testUser",
    "email": "testuser@hoetker.engineer",
    "full_name": "Test User",
    "password": "ValidPassword123",
}


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users", json=test_user)
        assert response.status_code == 200
        assert isinstance(response.json()["id"], int)
        response_json = response.json()
        del response_json["id"]
        assert response_json == {
            "username": "testuser",
            "email": "testuser@hoetker.engineer",
            "full_name": "Test User",
            "disabled": False,
        }
