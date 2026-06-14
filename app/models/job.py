from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from app.database import Base
import enum
import datetime

class JobStatus(str, enum.Enum):
    """
    Python Enum representing strict domain-level boundaries 
    for an application state machine.
    """
    APPLIED = "Applied"
    INTERVIEW = "Interviewing"
    REJECTED = "Rejected"
    OFFER = "Offer"

class JobModel(Base):
    """
    SQLAlchemy Data Model representing the 'job_applications' relational table.
    Defines schemas, constraints, and operational metadata.
    """
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False, index=True)
    company = Column(String(100), nullable=False, index=True)
    job_url = Column(String(500), nullable=True)
    status = Column(
        SQLEnum(JobStatus), 
        default=JobStatus.APPLIED, 
        nullable=False,
        server_default=JobStatus.APPLIED.value
    )
    notes = Column(String(2000), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow, 
        onupdate=datetime.datetime.utcnow, 
        nullable=False
    )