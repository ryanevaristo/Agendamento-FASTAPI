from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):

    DB_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/agendamento"
    DB_BASE_MODEL = declarative_base()

    JWT_SECRET: str = 'JcyBvNgLOFi9J4ifeeBthZ7C1uzlAVroZQ'

    '''
        Gerar token automatico:
        import secrets
        token: str = secrets.token_urlsafe(25)

    '''
    ALGHORITM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()