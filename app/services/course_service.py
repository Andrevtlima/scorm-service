
import uuid, os, zipfile, tempfile
from app.utils.storage import upload_file_multipart
from app.models.course import Course
from sqlalchemy.orm import Session

def handle_upload(db: Session, course_id: str, file_bytes: bytes):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(file_bytes); tmp.close()
    upload_file_multipart(tmp.name, f"{course_id}/{uuid.uuid4()}.zip")
    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        course = Course(id=course_id, title=course_id)
        db.add(course)
    course.deleted_at = None
    db.commit()
    os.remove(tmp.name)
    return course
