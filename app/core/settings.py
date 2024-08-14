from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = 'dev'
    PROJECT_NAME: str = "event"

    # JWT
    JWT_ENCODE_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "secret"  # Варианты генерации можно посмотреть в документации.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120  # 2h
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # DATABASE
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "postgres"
    DB_DRIVER: str = "postgresql+asyncpg"

    @property
    def DATABASE_URL(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
