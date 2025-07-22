
import time, hmac, hashlib, base64, urllib.parse
from app.core.config import settings

def generate_launch_url(course_id: str, registration_id: str, expires_in: int, metadata: dict, reuse_limit:int):
    now = int(time.time())
    exp = now + expires_in
    params = { "course_id": course_id, "registration_id": registration_id, "exp": exp, "reuse": reuse_limit, **metadata }
    query = urllib.parse.urlencode(params)
    sig = hmac.new(settings.API_KEY_SECRET.encode(), query.encode(), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode().rstrip("=")
    url = f"http://localhost:8000/player?{query}&sig={sig_b64}"
    return { "launch_url": url, "expires_at": exp }
