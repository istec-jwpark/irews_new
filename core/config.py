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

    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_DAYS: int = 14

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

settings = Settings()

print("###### Setting Information ######")
print(settings)
print("###### Setting Information ######")