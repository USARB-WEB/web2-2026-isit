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

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
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
