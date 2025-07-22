
import uuid, os, zipfile, tempfile, shutil
from app.utils.storage import upload_folder
from app.utils.ims_parser import parse_manifest
from app.static import scorm_hook_js
from app.models.course import Course
from sqlalchemy.orm import Session

def handle_upload(db: Session, course_id: str, file_bytes: bytes):
    """Process uploaded SCORM package and store files in GCS."""
    tmpdir = tempfile.mkdtemp()
    zpath = os.path.join(tmpdir, "package.zip")
    with open(zpath, "wb") as f:
        f.write(file_bytes)

    with zipfile.ZipFile(zpath) as zf:
        zf.extractall(tmpdir)

    manifest_path = os.path.join(tmpdir, "imsmanifest.xml")
    title, _ = parse_manifest(manifest_path)

    index_path = os.path.join(tmpdir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r+", encoding="utf-8") as f:
            html = f.read()
            if "scorm-hook.js" not in html:
                injection = '<script src="scorm-hook.js"></script>'
                if "</head>" in html:
                    html = html.replace("</head>", f"{injection}</head>")
                else:
                    html += injection
            f.seek(0)
            f.write(html)
            f.truncate()

    # ensure hook script uploaded
    hook_path = os.path.join(tmpdir, "scorm-hook.js")
    with open(hook_path, "w", encoding="utf-8") as f:
        f.write(scorm_hook_js)

    upload_folder(tmpdir, course_id)

    shutil.rmtree(tmpdir)

    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        course = Course(id=course_id, title=title)
        db.add(course)
    else:
        course.title = title
    course.deleted_at = None
    db.commit()
    return course
