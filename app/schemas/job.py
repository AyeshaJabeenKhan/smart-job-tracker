from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
from app.models.job import JobStatus

class JobBase(BaseModel):
    """
    Shared Data Transfer Object (DTO) containing core schema properties.
    Ensures structural data uniformity across request/response payloads.
    """
    title: str = Field(..., min_length=2, max_length=100, description="The job role title")
    company: str = Field(..., min_length=2, max_length=100, description="The hiring company name")
    job_url: Optional[str] = Field(None, description="Direct URL linking to the job post")
    status: JobStatus = Field(default=JobStatus.APPLIED, description="Current tracking state of the application")
    notes: Optional[str] = Field(None, max_length=2000, description="Personal application notes or reminders")

class JobCreate(JobBase):
    """
    Request Validation Schema strictly utilized for incoming HTTP POST payloads.
    Inherits all core fields from JobBase.
    """
    pass  # No extra mutations required for creation

class JobUpdate(BaseModel):
    """
    Request Validation Schema for HTTP PUT updates.
    Allows partial mutations; users can choose to update only the status or notes.
    """
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    company: Optional[str] = Field(None, min_length=2, max_length=100)
    job_url: Optional[str] = None
    status: Optional[JobStatus] = None
    notes: Optional[str] = Field(None, max_length=2000)

class JobResponse(JobBase):
    """
    Serialization Schema strictly utilized for outgoing HTTP response bodies.
    Guarantees internal system database IDs and metrics are safely serialized.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Enables seamless compatibility between SQLAlchemy ORM attributes and Pydantic DTOs."""
        from_attributes = True

class JobParseRequest(BaseModel):
    raw_text: str = Field(..., description="The unformatted text copy-pasted directly from a job board description.")

class InterviewPrepRequest(BaseModel):
    raw_text: str = Field(..., description="The unformatted job posting body text.")
    question_count: int = Field(default=3, ge=1, le=10, description="The dynamic number of questions requested by the user.")