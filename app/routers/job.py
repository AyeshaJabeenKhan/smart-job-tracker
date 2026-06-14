from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os
from google import genai

from app.database import get_db
from app.models.job import JobModel
from app.schemas.job import JobCreate, JobUpdate, JobResponse, JobParseRequest, InterviewPrepRequest

router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Job Applications"]
)

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job_application(job_payload: JobCreate, db: Session = Depends(get_db)):
    """
    HTTP POST Endpoint to instantiate a new job tracking resource inside the system.
    """
    db_job = JobModel(**job_payload.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/", response_model=List[JobResponse])
def read_job_applications(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    HTTP GET Endpoint to fetch collections of job records with built-in database-level pagination.
    """
    jobs = db.query(JobModel).offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
def read_single_job_application(job_id: int, db: Session = Depends(get_db)):
    """
    HTTP GET Endpoint to retrieve a specific job asset by its unique Primary Key.
    """
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job application with ID {job_id} does not exist in our ecosystem."
        )
    return db_job


@router.put("/{job_id}", response_model=JobResponse)
def update_job_application(job_id: int, update_payload: JobUpdate, db: Session = Depends(get_db)):
    """
    HTTP PUT Endpoint handling mutations and updates to tracking records.
    """
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot execute mutation. Job ID {job_id} not found."
        )
    
    update_data = update_payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job, key, value)
        
    db.commit()
    db.refresh(db_job)
    return db_job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_application(job_id: int, db: Session = Depends(get_db)):
    """
    HTTP DELETE Endpoint that safely expunges a tracking record from storage.
    """
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deletion aborted. Job ID {job_id} does not exist."
        )
    
    db.delete(db_job)
    db.commit()
    return None


@router.post("/parse-ai", response_model=JobCreate, status_code=status.HTTP_200_OK)
def parse_job_description_with_ai(payload: JobParseRequest):
    """
    Leverages Google Gemini AI to analyze raw, unformatted text from a job posting 
    and automatically extract structured details matching the application schema.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gemini API Key is missing from environment configurations."
        )
    
    try:
        # Initialize the official Google GenAI client locally within the request handler
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert recruitment data parser. Analyze the following raw text from a job posting.
        Extract the exact Job Title, the Company Name, and if available, a relevant URL or core notes.
        
        Raw Job Text:
        \"\"\"{payload.raw_text}\"\"\"
        """
        
        # Request Gemini to populate our Pydantic schema using structured outputs
        # Note the fix: genai.types.GenerateContentConfig
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=JobCreate,
                temperature=0.1
            ),
        )
        
        # The response text is a validated JSON string matching JobCreate
        return JobCreate.model_validate_json(response.text)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"AI Engine failed to parse the text layout: {str(e)}"
        )
    
@router.post("/generate-prep", status_code=status.HTTP_200_OK)
def generate_interview_prep_questions(payload: InterviewPrepRequest):
    """
    Leverages Gemini AI to generate a user-defined number of tailored, high-signal 
    technical interview questions based specifically on the target job profile details.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gemini API configuration key missing."
        )
        
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert technical interviewer. Review the following job description context.
        Generate exactly {payload.question_count} highly targeted technical interview questions 
        that a candidate applying to this specific role should prepare for. 
        Provide a concise, helpful "hint" or focus point for what the interviewer is looking for under each question.
        
        Format your response cleanly using structured markdown with bullet points.
        
        Job Posting Details:
        \"\"\"{payload.raw_text}\"\"\"
        """
        
        # Request Gemini to populate our content using structured configurations
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=genai.types.GenerateContentConfig(  # <--- Changed "types." to "genai.types."
                temperature=0.7 
            ),
        )
        
        return {"questions_markdown": response.text}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Interview Engine component failed: {str(e)}"
        )
