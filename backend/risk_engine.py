from typing import Dict, Any
from schemas import RiskAssessment

class RiskEngine:
    def __init__(self):
        self.risk_keywords = [
            "elevated glucose",
            "high creatinine",
            "abnormal labs",
            "renal failure",
            "cardiac issues",
            "respiratory distress"
        ]
    
    def calculate_risk_score(self, patient_data: Dict[str, Any]) -> RiskAssessment:
        score = 0
        
        # Age risk
        if patient_data.get('age', 0) > 60:
            score += 1
        
        # Diabetes in diagnosis
        diagnosis_lower = patient_data.get('diagnosis', '').lower()
        if 'diabetes' in diagnosis_lower or 'diabetic' in diagnosis_lower:
            score += 1
        
        # Medications count risk
        medications = patient_data.get('medications', '')
        medication_list = [med.strip() for med in medications.split(',') if med.strip()]
        if len(medication_list) >= 5:
            score += 1
        
        # Lab results keywords
        lab_results_lower = patient_data.get('lab_results', '').lower()
        diagnosis_lower = patient_data.get('diagnosis', '').lower()
        
        for keyword in self.risk_keywords:
            if keyword in lab_results_lower or keyword in diagnosis_lower:
                score += 1
                break  # Only add once for any keyword match
        
        # Determine risk level
        if score <= 1:
            risk_level = "Low"
        elif score <= 3:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return RiskAssessment(score=score, level=risk_level)
