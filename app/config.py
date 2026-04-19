from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    DATABASE_URL: str = "sqlite:///./app.db"
    DATABASE_URL_TEST: str = "sqlite:///./test.db"
    SECRET_KEY: str = "dev-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()