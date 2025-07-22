
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.auth import APIKey

def verify_api_key(x_api_key: str = Header(...), db: Session = Depends(get_db)):
    key = db.query(APIKey).filter_by(api_key=x_api_key, ativo=True).first()
    if not key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return key.client_id
