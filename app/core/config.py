
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://scorm:scormpass@db:5432/scormdb")
    API_KEY_SECRET = os.getenv("API_KEY_SECRET", "supersecretkey")
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    MINIO_BUCKET = os.getenv("MINIO_BUCKET", "scorm-prod")
    MINIO_MODE = os.getenv("MINIO_MODE", "gcs")

settings = Settings()
