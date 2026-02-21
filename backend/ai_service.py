import os
from typing import Dict, Any, Tuple
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        # Try OpenAI first
        if self.openai_api_key and self.openai_api_key.startswith("sk-") and len(self.openai_api_key) > 20:
            try:
                self.openai_client = OpenAI(api_key=self.openai_api_key)
                self.ai_provider = "openai"
                print("DEBUG: OpenAI client initialized successfully")
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self.openai_client = None
                self.ai_provider = None
        else:
            self.openai_client = None
            self.ai_provider = None
        
        # Try Gemini as fallback or primary
        if self.gemini_api_key and len(self.gemini_api_key) > 10:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                self.ai_provider = "gemini"
                print("DEBUG: Gemini client initialized successfully")
            except Exception as e:
                print(f"Error initializing Gemini client: {e}")
                self.gemini_model = None
                self.ai_provider = None
        else:
            self.gemini_model = None
            self.ai_provider = None
    
    def generate_summaries(self, patient_data: Dict[str, Any]) -> Tuple[str, str]:
        """Generate both professional and patient-friendly summaries"""
        
        print(f"DEBUG: AI Provider: {self.ai_provider}")
        
        # Use Gemini if available, otherwise try OpenAI, then fallback
        if self.ai_provider == "gemini":
            try:
                print("DEBUG: Attempting to generate summaries with Gemini...")
                # Generate professional summary with Gemini
                professional_prompt = f"""
You are a clinical documentation assistant. Generate a professional discharge summary using the following structured patient data:

Patient Name: {patient_data['patient_name']}
Age: {patient_data['age']}
Gender: {patient_data['gender']}
Admission Date: {patient_data['admission_date']}
Discharge Date: {patient_data['discharge_date']}
Diagnosis: {patient_data['diagnosis']}
Procedures: {patient_data['procedures']}
Lab Results: {patient_data['lab_results']}
Medications: {patient_data['medications']}
Hospital Course: {patient_data['hospital_course']}
Follow-up: {patient_data['follow_up']}

Generate a comprehensive, professional discharge summary following proper medical formatting. Include:
1. Brief patient identification
2. Admission diagnosis and procedures
3. Hospital course summary
4. Discharge medications
5. Follow-up instructions
6. Disposition

Keep the tone professional and clinical. Use appropriate medical terminology.
"""

                print(f"DEBUG: Sending to Gemini: {professional_prompt[:200]}...")
                professional_response = self.gemini_model.generate_content(professional_prompt)
                professional_summary = professional_response.text.strip()
                print(f"DEBUG: Gemini professional response: {professional_summary[:200]}...")
                print("DEBUG: Professional summary generated successfully with Gemini")

                # Generate patient-friendly summary with Gemini
                patient_prompt = f"""
Rewrite the following discharge summary in simple, easy-to-understand language suitable for a patient:

[PROFESSIONAL SUMMARY WILL BE GENERATED ABOVE]

Create a patient-friendly version that:
1. Uses simple, everyday language
2. Explains medical terms in plain English
3. Focuses on what the patient needs to know
4. Is encouraging and clear
5. Highlights important next steps for the patient

Structure it with clear headings like:
- What Happened During Your Hospital Stay
- Your Medications
- What You Need to Do Next
- When to Call Your Doctor

Make it warm, reassuring, and easy to follow.
"""

                print(f"DEBUG: Sending patient prompt to Gemini: {patient_prompt[:200]}...")
                patient_response = self.gemini_model.generate_content(patient_prompt)
                patient_summary = patient_response.text.strip()
                print(f"DEBUG: Gemini patient response: {patient_summary[:200]}...")
                print("DEBUG: Patient summary generated successfully with Gemini")

                return professional_summary, patient_summary

            except Exception as e:
                print(f"DEBUG: Gemini API call failed: {e}")
                print(f"DEBUG: Exception type: {type(e).__name__}")
                print(f"DEBUG: Exception details: {str(e)}")
                # Fallback summaries if AI fails
                professional_summary = self._generate_fallback_professional_summary(patient_data)
                patient_summary = self._generate_fallback_patient_summary(patient_data)
                return professional_summary, patient_summary
        
        elif self.ai_provider == "openai":
            try:
                print("DEBUG: Attempting to generate summaries with OpenAI...")
                # Generate professional summary
                professional_response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a clinical documentation assistant."},
                        {"role": "user", "content": professional_prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.3
                )
                professional_summary = professional_response.choices[0].message.content.strip()
                print("DEBUG: Professional summary generated successfully")

                print("DEBUG: Attempting to generate patient summary...")
                # Generate patient-friendly summary
                patient_response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a patient education specialist."},
                        {"role": "user", "content": f"Professional summary: {professional_summary}\n\n{patient_prompt}"}
                    ],
                    max_tokens=1000,
                    temperature=0.5
                )
                patient_summary = patient_response.choices[0].message.content.strip()
                print("DEBUG: Patient summary generated successfully")

                return professional_summary, patient_summary

            except Exception as e:
                print(f"DEBUG: OpenAI API call failed: {e}")
                # Fallback summaries if AI fails
                professional_summary = self._generate_fallback_professional_summary(patient_data)
                patient_summary = self._generate_fallback_patient_summary(patient_data)
                return professional_summary, patient_summary

        else:
            print("DEBUG: Using fallback summaries - no AI client")
            professional_summary = self._generate_fallback_professional_summary(patient_data)
            patient_summary = self._generate_fallback_patient_summary(patient_data)
            return professional_summary, patient_summary
    
    def _generate_fallback_professional_summary(self, patient_data: Dict[str, Any]) -> str:
        """Fallback professional summary if AI service fails"""
        return f"""
DISCHARGE SUMMARY

Patient: {patient_data['patient_name']}, {patient_data['age']}-year-old {patient_data['gender']}
Admission: {patient_data['admission_date']} - Discharge: {patient_data['discharge_date']}

DIAGNOSIS:
{patient_data['diagnosis']}

PROCEDURES:
{patient_data['procedures']}

HOSPITAL COURSE:
{patient_data['hospital_course']}

DISCHARGE MEDICATIONS:
{patient_data['medications']}

FOLLOW-UP:
{patient_data['follow_up']}

DISPOSITION: Patient discharged to home in stable condition.
"""

    def _generate_fallback_patient_summary(self, patient_data: Dict[str, Any]) -> str:
        """Fallback patient summary if AI service fails"""
        return f"""
What Happened During Your Hospital Stay

Dear {patient_data['patient_name']},

You were in the hospital from {patient_data['admission_date']} to {patient_data['discharge_date']}. 
During your stay, we treated you for: {patient_data['diagnosis']}

Your Medications
{patient_data['medications']}

What You Need to Do Next
{patient_data['follow_up']}

When to Call Your Doctor
- If you have any new symptoms
- If your medications cause side effects
- If you have questions about your care

You are doing well and ready to go home. Take care of yourself!
"""
