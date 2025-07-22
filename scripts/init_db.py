
from app.models.base import Base
from app.models import course, tracking, auth, webhook  # ensure import
from app.core.db import engine, SessionLocal
import uuid
def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    from app.models.auth import APIKey
    key = APIKey(id=str(uuid.uuid4()), client_id="demo", api_key="x-api-key-123")
    db.merge(key); db.commit(); db.close()
if __name__ == "__main__":
    init()
