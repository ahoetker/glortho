from databases import DatabaseURL
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    access_token_expire_minutes: int
    algorithm: str
    secret_key: str
    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_port: int
    postgres_db: str

    @property
    def postgres_url(self) -> DatabaseURL:
        return DatabaseURL(
            f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
