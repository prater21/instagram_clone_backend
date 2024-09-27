from passlib.context import CryptContext
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import random
import math
from pathlib import Path
from app.config import AppConfig
from app.schemas import EmailSchema, Message

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

config = AppConfig()


def hash_pw(pwd: str):
    return pwd_context.hash(pwd)


def verify_pw(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)


def set_mail_config():
    conf = ConnectionConfig(
        MAIL_USERNAME=config.MAIL_USERNAME,
        MAIL_PASSWORD=config.MAIL_PASSWORD,
        MAIL_FROM=config.MAIL_USERNAME,
        MAIL_PORT=config.MAIL_PORT,
        MAIL_SERVER=config.MAIL_SERVER,
        MAIL_FROM_NAME=config.MAIL_FROM_NAME,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        TEMPLATE_FOLDER=Path(__file__).parent / "./templates",
    )
    return conf


def get_auth_number(_len=6):
    chars = "0123456789"
    ran_num = ""

    for _ in range(_len):
        rnum = math.floor(random.random() * len(chars))
        ran_num += chars[rnum : rnum + 1]

    return ran_num


async def send_mail(email: EmailSchema, auth_code: int):
    config = set_mail_config()

    message = MessageSchema(
        subject="mail verification",
        recipients=[email],
        template_body={"auth_code": auth_code},
        subtype=MessageType.html,
    )

    fm = FastMail(config)
    await fm.send_message(message, template_name="email_template.html")

    return Message(message="email has been sent")
