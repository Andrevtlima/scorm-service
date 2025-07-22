
from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON
from app.models.base import Base
import datetime

class WebhookConfig(Base):
    __tablename__ = "webhook_configs"
    id = Column(String, primary_key=True)
    client_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    hmac_secret = Column(String, nullable=True)

class WebhookHistory(Base):
    __tablename__ = "webhook_history"
    id = Column(String, primary_key=True)
    client_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON)
    url = Column(String, nullable=False)
    status_code = Column(Integer)
    success = Column(Boolean, default=False)
    retries = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
