from functools import lru_cache

from jwt_authentication_python_postgres.core.config import Settings


@lru_cache()
def get_settings() -> Settings:
    return Settings()
