
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.auth import verify_api_key
from app.core.db import get_db
from app.services.course_service import handle_upload
from app.models.course import Course
import datetime

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/upload")
async def upload_course(course_id: str, file: UploadFile = File(...), client=Depends(verify_api_key), db: Session = Depends(get_db)):
    bytes_data = await file.read()
    course = handle_upload(db, course_id, bytes_data)
    return {"course_id": course.id, "title": course.title}


@router.get("/")
def list_courses(client=Depends(verify_api_key), db: Session = Depends(get_db)):
    courses = db.query(Course).filter_by(deleted_at=None).all()
    return [{"course_id": c.id, "title": c.title} for c in courses]


@router.delete("/{course_id}")
def delete_course(course_id: str, client=Depends(verify_api_key), db: Session = Depends(get_db)):
    course = db.query(Course).filter_by(id=course_id, deleted_at=None).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.deleted_at = datetime.datetime.utcnow()
    db.commit()
    return {"detail": "deleted"}
