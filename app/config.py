from pydantic_settings import BaseSettings, SettingsConfigDict

import os

DOTENV = os.path.join(os.path.dirname(__file__), "../.env")


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_DBNAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM_NAME: str
    MAIL_SERVER: str
    MAIL_PORT: int
