from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from typing import Dict, Any

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT
        )
        
        self.risk_style_low = ParagraphStyle(
            'RiskLow',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.green,
            alignment=TA_CENTER
        )
        
        self.risk_style_medium = ParagraphStyle(
            'RiskMedium',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.orange,
            alignment=TA_CENTER
        )
        
        self.risk_style_high = ParagraphStyle(
            'RiskHigh',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.red,
            alignment=TA_CENTER
        )
    
    def generate_discharge_pdf(self, discharge_data: Dict[str, Any]) -> BytesIO:
        """Generate PDF for discharge summary"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        story.append(Paragraph("DISCHARGE SUMMARY", self.title_style))
        story.append(Spacer(1, 12))
        
        # Patient Information Table
        patient_data = [
            ['Patient Name:', discharge_data['patient_name']],
            ['Age:', str(discharge_data['age'])],
            ['Gender:', discharge_data['gender']],
            ['Admission Date:', str(discharge_data['admission_date'])],
            ['Discharge Date:', str(discharge_data['discharge_date'])],
        ]
        
        patient_table = Table(patient_data, colWidths=[2*inch, 3*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 20))
        
        # Risk Level Badge
        risk_level = discharge_data.get('risk_level', 'Unknown')
        risk_score = discharge_data.get('risk_score', 0)
        
        if risk_level == 'Low':
            risk_style = self.risk_style_low
            risk_color = colors.green
        elif risk_level == 'Medium':
            risk_style = self.risk_style_medium
            risk_color = colors.orange
        else:
            risk_style = self.risk_style_high
            risk_color = colors.red
        
        risk_text = f"Risk Level: {risk_level} (Score: {risk_score})"
        story.append(Paragraph(risk_text, risk_style))
        story.append(Spacer(1, 20))
        
        # Diagnosis
        story.append(Paragraph("DIAGNOSIS", self.heading_style))
        story.append(Paragraph(discharge_data['diagnosis'], self.normal_style))
        story.append(Spacer(1, 12))
        
        # Procedures
        story.append(Paragraph("PROCEDURES", self.heading_style))
        story.append(Paragraph(discharge_data['procedures'], self.normal_style))
        story.append(Spacer(1, 12))
        
        # Hospital Course
        story.append(Paragraph("HOSPITAL COURSE", self.heading_style))
        story.append(Paragraph(discharge_data['hospital_course'], self.normal_style))
        story.append(Spacer(1, 12))
        
        # Medications
        story.append(Paragraph("DISCHARGE MEDICATIONS", self.heading_style))
        story.append(Paragraph(discharge_data['medications'], self.normal_style))
        story.append(Spacer(1, 12))
        
        # Follow-up
        story.append(Paragraph("FOLLOW-UP INSTRUCTIONS", self.heading_style))
        story.append(Paragraph(discharge_data['follow_up'], self.normal_style))
        story.append(Spacer(1, 20))
        
        # AI Professional Summary
        if discharge_data.get('ai_summary'):
            story.append(Paragraph("AI-GENERATED PROFESSIONAL SUMMARY", self.heading_style))
            story.append(Paragraph(discharge_data['ai_summary'], self.normal_style))
            story.append(Spacer(1, 20))
        
        # Patient-Friendly Summary
        if discharge_data.get('patient_summary'):
            story.append(Paragraph("PATIENT-FRIENDLY SUMMARY", self.heading_style))
            story.append(Paragraph(discharge_data['patient_summary'], self.normal_style))
            story.append(Spacer(1, 20))
        
        # Footer
        story.append(Paragraph("Generated by Discharge IQ - Smart Discharge Summary Generator", 
                              ParagraphStyle('Footer', parent=self.styles['Normal'], 
                                           fontSize=8, alignment=TA_CENTER, textColor=colors.grey)))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
