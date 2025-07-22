
from sqlalchemy import Column, String, Float, Enum, JSON, DateTime
from app.models.base import Base
import enum, datetime

class ExecutionStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class ExecutionTracking(Base):
    __tablename__ = "execution_tracking"
    id = Column(String, primary_key=True)
    course_id = Column(String, nullable=False)
    registration_id = Column(String, unique=True, nullable=False)
    client_id = Column(String, nullable=False)
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.not_started)
    total_time = Column(Float, default=0.0)
    score_raw = Column(Float, nullable=True)
    score_min = Column(Float, nullable=True)
    score_max = Column(Float, nullable=True)
    interactions = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
