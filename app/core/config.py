from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    NAME: str = "FastAPI Ecommerce"
    DEBUG: bool
    VERSION: str = "1.0.0"


class JWTSettings(BaseSettings):
    ALGORITHM: str
    SECRET_KEY: SecretStr


class DatabaseSettings(BaseSettings):
    URL: SecretStr
    ECHO: bool
    POOL_SIZE: int
    MAX_OVERFLOW: int
    POOL_PRE_PING: bool = True


class Settings(BaseSettings):
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
