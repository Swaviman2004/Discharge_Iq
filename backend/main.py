from fastapi import FastAPI, Depends, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from database import get_db, engine, Base
from models import DischargeSummary
from auth_models import AdminUser
from schemas import PatientData, DischargeSummaryResponse
from auth_schemas import LoginRequest, LoginResponse, UserResponse
from ai_service import AIService
from risk_engine import RiskEngine
from pdf_generator import PDFGenerator
from auth_service import auth_service

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Discharge IQ API",
    description="Smart Discharge Summary Generator",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize services
ai_service = AIService()
risk_engine = RiskEngine()
pdf_generator = PDFGenerator()

# Authentication dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user = auth_service.get_current_user(db, token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.get("/")
async def root():
    return {"message": "Discharge IQ API is running"}

@app.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint for doctors/technicians"""
    try:
        access_token, user = auth_service.login_user(db, login_data.username, login_data.password)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "role": user.role
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@app.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: AdminUser = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@app.post("/generate-summary", response_model=DischargeSummaryResponse)
async def generate_summary(
    patient_data: PatientData, 
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Generate AI-powered discharge summary and store in database
    """
    try:
        # Create initial record with patient data
        db_discharge = DischargeSummary(
            patient_name=patient_data.patient_name,
            age=patient_data.age,
            gender=patient_data.gender,
            admission_date=patient_data.admission_date,
            discharge_date=patient_data.discharge_date,
            diagnosis=patient_data.diagnosis,
            procedures=patient_data.procedures,
            lab_results=patient_data.lab_results,
            medications=patient_data.medications,
            hospital_course=patient_data.hospital_course,
            follow_up=patient_data.follow_up,
            created_by=current_user.id
        )
        
        db.add(db_discharge)
        db.commit()
        db.refresh(db_discharge)
        
        # Calculate risk score
        patient_dict = patient_data.dict()
        risk_assessment = risk_engine.calculate_risk_score(patient_dict)
        
        # Generate AI summaries
        professional_summary, patient_summary = ai_service.generate_summaries(patient_dict)
        
        # Update record with AI results and risk assessment
        db_discharge.ai_summary = professional_summary
        db_discharge.patient_summary = patient_summary
        db_discharge.risk_score = risk_assessment.score
        db_discharge.risk_level = risk_assessment.level
        
        db.commit()
        db.refresh(db_discharge)
        
        return db_discharge
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@app.get("/records", response_model=List[DischargeSummaryResponse])
async def get_all_records(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Get all discharge summaries from database
    """
    try:
        # Doctors and Technicians can only see their own records
        if current_user.role in ["Doctor", "Technician"]:
            records = db.query(DischargeSummary).filter(
                DischargeSummary.created_by == current_user.id
            ).order_by(DischargeSummary.created_at.desc()).all()
        else:
            # Admins can see all records
            records = db.query(DischargeSummary).order_by(DischargeSummary.created_at.desc()).all()
        
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching records: {str(e)}")

@app.get("/records/{record_id}", response_model=DischargeSummaryResponse)
async def get_record(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Get a single discharge summary by ID
    """
    try:
        record = db.query(DischargeSummary).filter(DischargeSummary.id == record_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        # Check access permissions
        if current_user.role in ["Doctor", "Technician"] and record.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied to this record")
        
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching record: {str(e)}")

@app.get("/download-pdf/{record_id}")
async def download_pdf(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Generate and download PDF for a discharge summary
    """
    try:
        record = db.query(DischargeSummary).filter(DischargeSummary.id == record_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        # Check access permissions
        if current_user.role in ["Doctor", "Technician"] and record.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied to this record")
        
        # Convert record to dictionary
        record_dict = {
            'patient_name': record.patient_name,
            'age': record.age,
            'gender': record.gender,
            'admission_date': record.admission_date,
            'discharge_date': record.discharge_date,
            'diagnosis': record.diagnosis,
            'procedures': record.procedures,
            'hospital_course': record.hospital_course,
            'medications': record.medications,
            'follow_up': record.follow_up,
            'ai_summary': record.ai_summary,
            'patient_summary': record.patient_summary,
            'risk_level': record.risk_level,
            'risk_score': record.risk_score
        }
        
        # Generate PDF
        pdf_buffer = pdf_generator.generate_discharge_pdf(record_dict)
        
        # Return PDF as response
        pdf_content = pdf_buffer.getvalue()
        pdf_buffer.close()
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=discharge_summary_{record.patient_name}_{record_id}.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "Discharge IQ API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
