import uuid
import boto3
from app.config import AppConfig
import boto3

from app.schemas import Message
from botocore.exceptions import NoCredentialsError

config = AppConfig()


s3 = boto3.client(
    "s3",
    aws_access_key_id=config.AWS_S3_ACCESS_KEY,
    aws_secret_access_key=config.AWS_S3_PRIVATE_KEY,
    region_name=config.AWS_S3_REGION,
)

BUCKET_NAME = config.AWS_S3_BUCKET_NAME


async def upload_to_s3(file, directory="post"):
    filename = f"{str(uuid.uuid4())}.jpg"
    filename = f"{directory}/{filename}"

    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, filename)
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

    except Exception as e:
        return e

    # try:
    #     s3.upload_fileobj(file.file, config.AWS_S3_BUCKET_NAME, s3_key)
    # except (BotoCoreError, ClientError) as e:
    #     print(e)
    # raise HTTPException(status_code=500, detail=f"S3 upload fails: {str(e)}")

    # url = "https://s3-ap-northeast-2.amazonaws.com/%s/%s" % (
    #     BUCKET_NAME,
    #     urllib.parse.quote(s3_key, safe="~()*!.'"),
    # )
    # return JSONResponse(content={"url": url})
