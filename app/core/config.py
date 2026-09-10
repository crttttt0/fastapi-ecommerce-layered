from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Настройки приложения."""

    NAME: str = "FastAPI Ecommerce"
    DEBUG: bool
    VERSION: str = "1.0.0"


class JWTSettings(BaseSettings):
    """Настройки JWT."""

    ALGORITHM: str
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


class DatabaseSettings(BaseSettings):
    """Настройки подключения к БД."""

    URL: SecretStr
    ECHO: bool
    POOL_SIZE: int
    MAX_OVERFLOW: int
    POOL_PRE_PING: bool = True


class Settings(BaseSettings):
    """Корневые настройки приложения."""

    app: AppSettings
    jwt: JWTSettings
    database: DatabaseSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
