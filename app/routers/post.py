from fastapi import APIRouter, Request, status, UploadFile

from app.models import Comment, Post
from app.schemas import CreateComment, CreatePost, ImageResponse, Message
from app.utils.common import raise_error
from app.utils.fileUpload import upload_to_s3
from app.utils.logger import log_request, log_request_auth
from app.oauth2 import user_dependency
from app.database import db_dependency


router = APIRouter()


# 게시물 조회(좋아요수, 댓글, 사진, 컨텐츠)
# 게시물 등록
# 게시물 삭제
# 게시물 수정
# 게시물 좋아요(등록, 취소)
# 게시물 댓글달기
# 게시물 댓글삭제

# 전체 검색
# 해시태그 검색


@router.post(
    "/img/upload",
    status_code=status.HTTP_200_OK,
    response_model=ImageResponse | Message,
)
async def img_upload(request: Request, file: UploadFile, user_info: user_dependency):
    """
    upload image
    """
    log_request_auth(request.url.path, user_info.id, request.method, file)

    try:
        img_src = await upload_to_s3(file)

    except Exception as e:
        raise_error(request.url.path, request.method, 406, "Image upload fail")

    return ImageResponse(img_src=img_src)


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
async def create_post(
    db: db_dependency, user_info: user_dependency, request: Request, post: CreatePost
):
    """
    create post
    """
    log_request_auth(request.url.path, request.method, user_info.id, post)

    # user_id = Column(Integer, ForeignKey("user.id"))
    # content = Column(String(2000))
    # reg_date = Column(DateTime, default=datetime.datetime.now())
    new_post = Post(user_id=user_info.id, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post.id)

    return Message(message="post create successful")


@router.post(
    "/comment",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
async def add_comment(
    db: db_dependency,
    user_info: user_dependency,
    request: Request,
    comment_info: CreateComment,
):
    """
    add comment
    """
    log_request_auth(request.url.path, request.method, user_info.id, comment_info)

    new_comment = Comment(user_id=user_info.id, **comment_info.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return Message(message="comment add successful")
