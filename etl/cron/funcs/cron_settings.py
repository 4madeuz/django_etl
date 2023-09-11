from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_host: str = 'localhost'
    postgres_port: str = '5432'
    postgres_db: str
    postgres_user: str
    postgres_password: str
