from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Pydantic will look for these exact names (case-insensitive) in the environment
    DATABASE_URL: str
    REDIS_URL: str
    APP_ENV: str = "production"

    # Tell Pydantic to read from a .env file if those variables aren't in the OS environment
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


# Instantiate a singleton to be imported across the app
settings = Settings()
