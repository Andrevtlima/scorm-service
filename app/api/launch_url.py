
from fastapi import APIRouter, Depends, Query
from app.api.auth import verify_api_key
from app.utils.registration import make_registration_id
from app.services.launch_service import generate_launch_url

router = APIRouter(prefix="/launch-url", tags=["Launch"])

@router.get("/")
def get_launch(course_id: str, learner_id: str = Query(...), client=Depends(verify_api_key)):
    reg_id = make_registration_id(learner_id, course_id)
    info = generate_launch_url(course_id, reg_id, 3600, {"learner_id": learner_id}, 1)
    info["registration_id"] = reg_id
    return info
