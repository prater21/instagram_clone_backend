from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pw(pwd: str):
    return pwd_context.hash(pwd)


def verify_pw(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)
