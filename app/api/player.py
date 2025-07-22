from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.services.launch_service import verify_signature
from app.utils.storage import generate_public_url
from app.core.db import get_db
from app.models.tracking import ExecutionTracking, ExecutionStatus
import time

router = APIRouter(tags=["Player"])

@router.get("/player")
def launch_player(request: Request, course_id: str, registration_id: str, exp: int, reuse: int, sig: str, db: Session = Depends(get_db)):
    params = {
        "course_id": course_id,
        "registration_id": registration_id,
        "exp": exp,
        "reuse": reuse,
    }
    for k in ["session_id", "utm", "context"]:
        if k in request.query_params:
            params[k] = request.query_params[k]
    if not verify_signature(params, sig):
        raise HTTPException(status_code=403, detail="Invalid signature")
    if exp < int(time.time()):
        raise HTTPException(status_code=403, detail="Launch URL expired")
    track = db.query(ExecutionTracking).filter_by(registration_id=registration_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Registration not found")
    track.status = ExecutionStatus.in_progress
    db.commit()
    url = generate_public_url(f"{course_id}/index.html")
    return RedirectResponse(url)
