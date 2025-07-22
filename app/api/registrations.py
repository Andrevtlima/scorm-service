
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import verify_api_key
from app.core.db import get_db
from app.utils.registration import make_registration_id
from app.models.tracking import ExecutionTracking, ExecutionStatus
import uuid, datetime

router = APIRouter(prefix="/registrations", tags=["Registrations"])

class RegIn(BaseModel):
    course_id: str
    learner_id: str

class RegOut(BaseModel):
    registration_id: str
    course_id: str
    learner_id: str
    status: str

@router.post("/", response_model=RegOut, status_code=status.HTTP_201_CREATED)
def create_reg(payload: RegIn, client=Depends(verify_api_key), db: Session = Depends(get_db)):
    reg_id = make_registration_id(payload.learner_id, payload.course_id)
    track = db.query(ExecutionTracking).filter_by(registration_id=reg_id).first()
    if not track:
        track = ExecutionTracking(
            id=str(uuid.uuid4()),
            course_id=payload.course_id,
            registration_id=reg_id,
            client_id=client,
            status=ExecutionStatus.not_started
        )
        db.add(track); db.commit(); db.refresh(track)
    return RegOut(registration_id=reg_id, course_id=payload.course_id, learner_id=payload.learner_id, status=track.status)
