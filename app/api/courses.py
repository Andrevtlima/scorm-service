
from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from app.api.auth import verify_api_key
from app.core.db import get_db
from app.services.course_service import handle_upload

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/upload")
async def upload_course(course_id: str, file: UploadFile = File(...), client=Depends(verify_api_key), db: Session = Depends(get_db)):
    bytes_data = await file.read()
    course = handle_upload(db, course_id, bytes_data)
    return {"course_id": course.id, "title": course.title}
