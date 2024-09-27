from fastapi import APIRouter, status, HTTPException, Request

from app.utils.authUtils import hash_pw
from app.schemas import Message, ResetPasswordBase
from app.models import User
from app.database import db_dependency
from app.utils.logger import log_request
from app.utils.common import raise_error

router = APIRouter(prefix="/user", tags=["user"])

# api list
# password reset
# login
# username check
# email check, send authcode, confirm autocode


@router.post("/password/reset", status_code=status.HTTP_200_OK, response_model=Message)
async def reset_password(
    db: db_dependency,
    request: Request,
    user_info: ResetPasswordBase,
):
    """
    reset password
    """
    log_request(request.url.path, request.method, body=user_info)
    user = db.query(User).filter(User.email == user_info.email).first()

    if user is None:
        raise_error(request.url.path, request.method, 406, "Invalid user info")

    user.password = hash_pw(user_info.password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return Message(message="Password reset was successful")
