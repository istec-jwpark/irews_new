from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str
    APP_NAME: str
    APP_DEBUG: bool = False

    ORACLE_USER: str
    ORACLE_PASSWORD: str
    ORACLE_DSN: str
    DB_POOL_MIN: int = 1
    DB_POOL_MAX: int = 10
    DB_POOL_INC: int = 1
    DB_AUTOCOMMIT: bool = False

    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_MINUTES: int = 15
    REFRESH_TOKEN_DAYS: int = 14
    REFRESH_TOKEN_ROTATE: bool = True
    REFRESH_TOKEN_HASH: bool = True

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

settings = Settings()

print("###### Setting Information ######")
print(settings)
print("###### Setting Information ######")