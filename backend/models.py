from sqlalchemy import Column, Integer, String, Date, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class DischargeSummary(Base):
    __tablename__ = "discharge_summaries"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(50), nullable=False)
    admission_date = Column(Date, nullable=False)
    discharge_date = Column(Date, nullable=False)
    diagnosis = Column(Text, nullable=False)
    procedures = Column(Text, nullable=False)
    lab_results = Column(Text, nullable=False)
    medications = Column(Text, nullable=False)
    hospital_course = Column(Text, nullable=False)
    follow_up = Column(Text, nullable=False)
    ai_summary = Column(Text, nullable=True)
    patient_summary = Column(Text, nullable=True)
    risk_score = Column(Integer, nullable=True)
    risk_level = Column(String(50), nullable=True)
    created_by = Column(Integer, ForeignKey("admin_users.id"), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    
    # Relationship to admin user
    creator = relationship("AdminUser", back_populates="created_summaries")
