from pydantic_settings import BaseSettings, SettingsConfigDict

import os

DOTENV = os.path.join(os.path.dirname(__file__), "../.env")


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    # DB Config
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_DBNAME: str

    # jwt config
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # email config
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM_NAME: str
    MAIL_SERVER: str
    MAIL_PORT: int

    # s3 config
    AWS_S3_ACCESS_KEY: str
    AWS_S3_PRIVATE_KEY: str
    AWS_S3_BUCKET_NAME: str
    AWS_S3_REGION: str
