from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    DATABASE_URL: str = "sqlite:///./test.db"
    DATABASE_URL_TEST: str = "sqlite:///./test.db"
    SECRET_KEY: str = "dev-secret"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()