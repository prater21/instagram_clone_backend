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
