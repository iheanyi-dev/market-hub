from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.

    Values are loaded automatically from the `.env` file,
    keeping environment-specific configuration outside the codebase.
    """

    APP_NAME: str = "Market Hub API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    @property
    def DATABASE_URL(self) -> str:
        """
        Build the database connection string from individual
        environment variables to avoid storing duplicate values.
        """
        return (
            f"postgresql+asyncpg://"
            f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )

    # Configure Pydantic to load settings from the project's .env file.
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Create a single Settings instance for the entire application.

    Configuration is immutable during runtime, so recreating the
    object on every import is unnecessary.
    """
    return Settings()


# Shared settings instance imported throughout the application.
settings = get_settings()