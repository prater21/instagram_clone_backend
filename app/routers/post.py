from fastapi import APIRouter, Request, status, UploadFile

from app.schemas import ImageResponse, Message
from app.utils.common import raise_error
from app.utils.fileUpload import upload_to_s3
from app.utils.logger import log_request


router = APIRouter(prefix="/post", tags=["post"])


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
async def img_upload(request: Request, file: UploadFile):
    """
    upload image
    """
    log_request(request.url.path, request.method, body=file)

    try:
        img_src = await upload_to_s3(file)

    except Exception as e:
        raise_error(request.url.path, request.method, 406, "Image upload fail")

    return ImageResponse(img_src=img_src)
