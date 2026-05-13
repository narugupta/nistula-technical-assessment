from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    DATABASE_URL: str = (
        "postgresql+asyncpg://"
        "nistula:nistula@localhost:5432/nistula_db"
    )

    ANTHROPIC_API_KEY: str = ""

    # pydantic v2 is strict about unknown env vars
    # docker injects postgres vars we are not explicitly using yet
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()