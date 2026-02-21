from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class PatientData(BaseModel):
    patient_name: str = Field(..., min_length=1, max_length=255)
    age: int = Field(..., ge=0, le=150)
    gender: str = Field(..., min_length=1, max_length=50)
    admission_date: date
    discharge_date: date
    diagnosis: str = Field(..., min_length=1)
    procedures: str = Field(..., min_length=1)
    lab_results: str = Field(..., min_length=1)
    medications: str = Field(..., min_length=1)
    hospital_course: str = Field(..., min_length=1)
    follow_up: str = Field(..., min_length=1)

class DischargeSummaryResponse(BaseModel):
    id: int
    patient_name: str
    age: int
    gender: str
    admission_date: date
    discharge_date: date
    diagnosis: str
    procedures: str
    lab_results: str
    medications: str
    hospital_course: str
    follow_up: str
    ai_summary: Optional[str] = None
    patient_summary: Optional[str] = None
    risk_score: Optional[int] = None
    risk_level: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class RiskAssessment(BaseModel):
    score: int
    level: str
