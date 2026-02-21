# Discharge IQ – Smart Discharge Summary Generator

A production-ready, AI-powered healthcare web application that generates intelligent discharge summaries with risk assessment and PDF export capabilities.

## 🎯 Project Overview

Discharge IQ is a comprehensive full-stack application that:
- Accepts structured patient discharge data
- Stores all data in MySQL database
- Generates AI-powered professional discharge summaries
- Creates patient-friendly explanations
- Calculates clinical risk insights
- Exports summaries as downloadable PDFs
- Provides a complete history dashboard

## 🏗 Tech Stack

### Backend
- **FastAPI** (Python) - REST API framework
- **SQLAlchemy ORM** - Database ORM
- **MySQL 8+** - Primary database
- **OpenAI API** - AI summary generation
- **ReportLab** - PDF generation
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI framework
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons
- **Date-fns** - Date handling

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Frontend serving

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd discharge-iq
```

### 2. Environment Configuration
Create a `.env` file in the project root:
```bash
# MySQL Configuration
MYSQL_ROOT_PASSWORD=your_secure_password
MYSQL_DATABASE=discharge_iq
MYSQL_USER=discharge_user
MYSQL_PASSWORD=your_mysql_password

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Start the Application
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📁 Project Structure
```
discharge-iq/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── ai_service.py        # AI summary generation
│   ├── risk_engine.py       # Risk calculation logic
│   ├── pdf_generator.py     # PDF generation
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container
│   └── .env.example        # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.js          # Main application
│   │   └── index.js        # Entry point
│   ├── public/             # Static files
│   ├── package.json        # Node dependencies
│   ├── Dockerfile          # Frontend container
│   └── nginx.conf          # Nginx configuration
├── docker-compose.yml      # Container orchestration
├── init.sql                # Database initialization
└── README.md              # This file
```

## 🗄 Database Schema

### discharge_summaries Table
```sql
CREATE TABLE discharge_summaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255),
    age INT,
    gender VARCHAR(50),
    admission_date DATE,
    discharge_date DATE,
    diagnosis TEXT,
    procedures TEXT,
    lab_results TEXT,
    medications TEXT,
    hospital_course TEXT,
    follow_up TEXT,
    ai_summary LONGTEXT,
    patient_summary LONGTEXT,
    risk_score INT,
    risk_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔌 API Endpoints

### Generate Discharge Summary
```http
POST /generate-summary
Content-Type: application/json

{
  "patient_name": "John Doe",
  "age": 65,
  "gender": "Male",
  "admission_date": "2024-01-15",
  "discharge_date": "2024-01-18",
  "diagnosis": "Community-acquired pneumonia",
  "procedures": "Chest X-ray, Blood cultures",
  "lab_results": "WBC: 15.2 x 10^9/L, CRP: 45 mg/L",
  "medications": "Amoxicillin 500mg TID x 7 days",
  "hospital_course": "Patient improved with antibiotics",
  "follow_up": "Follow up with PCP in 1 week"
}
```

### Get All Records
```http
GET /records
```

### Get Single Record
```http
GET /records/{id}
```

### Download PDF
```http
GET /download-pdf/{id}
```

### Health Check
```http
GET /health
```

## 🧠 Risk Engine Logic

The risk assessment system uses rule-based scoring:

### Risk Factors
- **Age > 60**: +1 point
- **Diabetes in diagnosis**: +1 point
- **5+ medications**: +1 point
- **Lab keywords**: +1 point (elevated glucose, high creatinine, etc.)

### Risk Levels
- **0-1 points**: Low Risk (Green)
- **2-3 points**: Medium Risk (Yellow)
- **4+ points**: High Risk (Red)

## 🎨 Frontend Features

### Patient Form
- Comprehensive patient data input
- Real-time validation
- Responsive design
- Loading states

### Summary Display
- Professional AI-generated summary
- Patient-friendly explanation
- Risk level visualization
- PDF download functionality

### History Dashboard
- Complete record history
- Searchable and sortable
- Risk level indicators
- Quick actions

## ☁️ Cloud Deployment

### AWS Deployment
```bash
# 1. Deploy to EC2
git clone <repository>
cd discharge-iq

# 2. Configure environment
# Edit .env with AWS RDS MySQL credentials

# 3. Deploy with Docker
docker-compose -f docker-compose.prod.yml up -d
```

### Google Cloud Platform
```bash
# 1. Use Cloud Run + Cloud SQL
gcloud builds submit --tag gcr.io/PROJECT_ID/discharge-iq
gcloud run deploy discharge-iq --image gcr.io/PROJECT_ID/discharge-iq
```

### Microsoft Azure
```bash
# 1. Use App Service + Azure MySQL
az webapp up --name discharge-iq --resource-group discharge-iq-rg
```

## 🔧 Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Database Setup (Local)
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE discharge_iq;

# Run initialization script
mysql -u root -p discharge_iq < init.sql
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔒 Security Features

- **Environment Variables**: All secrets stored in .env
- **Input Validation**: Pydantic schemas for all inputs
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **CORS Configuration**: Configurable for production
- **Rate Limiting**: Can be implemented with FastAPI middleware

## 📊 Monitoring & Logging

### Application Logs
```bash
# View container logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mysql
```

### Health Monitoring
- `/health` endpoint for application status
- Docker health checks for container monitoring
- Database connection health checks

## 🚀 Performance Optimization

### Database Indexes
- Patient name index for search
- Created_at index for sorting
- Risk level index for filtering

### Caching
- Redis can be added for session management
- API response caching for frequently accessed data

### Scaling
- Horizontal scaling with load balancers
- Database read replicas for read-heavy workloads

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the [Issues](../../issues) page
2. Review the API documentation at `/docs`
3. Check container logs for debugging

## 🎯 Production Checklist

- [ ] Configure production environment variables
- [ ] Set up SSL certificates
- [ ] Configure backup strategy for MySQL
- [ ] Set up monitoring and alerting
- [ ] Review and tighten CORS settings
- [ ] Implement rate limiting
- [ ] Set up log rotation
- [ ] Configure database backups
- [ ] Test disaster recovery procedures

---

**Built with ❤️ for healthcare professionals**
