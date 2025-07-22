
import boto3, os
from botocore.client import Config
from app.core.config import settings

session = boto3.session.Session()
s3 = session.client(
    "s3",
    endpoint_url=settings.MINIO_ENDPOINT,
    aws_access_key_id=settings.MINIO_ACCESS_KEY if hasattr(settings, "MINIO_ACCESS_KEY") else None,
    aws_secret_access_key=settings.MINIO_SECRET_KEY if hasattr(settings, "MINIO_SECRET_KEY") else None,
    config=Config(signature_version="s3v4"),
    region_name="auto"
)

def upload_file_multipart(file_path: str, key: str):
    s3.upload_file(file_path, settings.MINIO_BUCKET, key)
def generate_public_url(key: str):
    return f"{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}/{key}"
