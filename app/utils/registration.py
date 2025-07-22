
import hashlib, base64
def make_registration_id(learner_id: str, course_id: str) -> str:
    raw = f"{learner_id}|{course_id}".encode()
    return base64.urlsafe_b64encode(hashlib.sha256(raw).digest())[:22].decode().rstrip("=")
