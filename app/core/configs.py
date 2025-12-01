from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sistema de Portões Eletrônicos"
    DATABASE_URL: str = "postgresql://portoes_user:portoes_password@db:5432/portoes_db"

    SECRET_KEY: str = "botafogo24"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 semana

    class Config:
        case_sensitive = True


settings = Settings()
