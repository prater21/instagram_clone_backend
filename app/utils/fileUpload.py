import uuid
from boto3 import BotoCoreError, ClientError
from app.config import AppConfig
import boto3

config = AppConfig()


s3 = boto3.client(
    "s3",
    aws_access_key_id=config.AWS_S3_ACCESS_KEY,
    aws_secret_access_key=config.AWS_S3_PRIVATE_KEY,
)


async def upload(file, directory: str):
    filename = f"{str(uuid.uuid4())}.jpg"
    s3_key = f"{directory}/{filename}"

    try:
        s3.upload_fileobj(file.file, config.AWS_S3_BUCKET_NAME, s3_key)
    except (BotoCoreError, ClientError) as e:
        print(e)
        # raise HTTPException(status_code=500, detail=f"S3 upload fails: {str(e)}")

    # url = "https://s3-ap-northeast-2.amazonaws.com/%s/%s" % (
    #     BUCKET_NAME,
    #     urllib.parse.quote(s3_key, safe="~()*!.'"),
    # )
    # return JSONResponse(content={"url": url})
