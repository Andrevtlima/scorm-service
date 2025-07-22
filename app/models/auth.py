
from sqlalchemy import Column, String, Boolean, DateTime
from app.models.base import Base
import datetime

class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(String, primary_key=True)
    client_id = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    scopes = Column(String, default="*")
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.datetime.utcnow)
