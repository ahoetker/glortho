from pathlib import Path
from typing import Optional

from databases import DatabaseURL
from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    access_token_expire_minutes: int
    algorithm: str
    first_admin_email: str = None
    first_admin_fullname: str = "admin"
    first_admin_username: str = "admin"
    first_admin_password: str
    secret_key: str
    postgres_user: Optional[str]
    postgres_password: Optional[str]
    postgres_server: Optional[str]
    postgres_port: Optional[int]
    postgres_db: Optional[str]
    sqlite_db: Optional[Path] = Path("app.db")

    @root_validator(pre=True)
    def validate_postgres_values(cls, values):
        postgres_values = {'postgres_user', 'postgres_password', 'postgres_server', 'postgres_port', 'postgres_db'}
        if any(value in values for value in postgres_values):
            for value in postgres_values:
                assert value in values, f"Missing Postgres configuration value: {value}"
        return values

    @property
    def postgres_url(self) -> Optional[DatabaseURL]:
        if self.postgres_db is not None:  # Other Postgres values are guaranteed by validate_postgres_values
            return DatabaseURL("postgresql://{0}:{1}@{2}:{3}/{4}".format(self.postgres_user, self.postgres_password,
                                                                         self.postgres_server, self.postgres_port,
                                                                         self.postgres_db))
        else:
            return None

    @property
    def sqlite_uri(self) -> DatabaseURL:
        return DatabaseURL(
            f"sqlite:///{str(self.sqlite_db.absolute())}"
        )

    @property
    def database_url(self) -> DatabaseURL:
        if self.postgres_url is not None:
            return self.postgres_url
        else:
            return self.sqlite_uri

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        secrets_dir = "/run/secrets"
