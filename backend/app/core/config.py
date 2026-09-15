from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Learning Backend"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    mysql_user: str = "learning_user"
    mysql_password: str = "learning_pass"
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_database: str = "learning_db"
    mysql_test_database: str = "learning_test_db"

    # Authentication. The default secret is fine for local development only;
    # set JWT_SECRET_KEY in the environment for anything else.
    jwt_secret_key: str = "local-development-only-secret-change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )

    @property
    def test_database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_test_database}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
