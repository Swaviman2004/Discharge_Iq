# 🏥 Discharge IQ - Cloud Deployment

## 🚀 Quick Start

### Prerequisites
- Docker installed
- Docker Compose installed
- Git installed

### One-Command Deployment
```bash
# Clone and deploy
git clone https://github.com/patraswaviman1/discharge-iq.git
cd discharge-iq
chmod +x deploy.sh
./deploy.sh
```

## 🐳 Docker Images Available

### Backend
- **Image**: `patraswaviman1/discharge-iq-backend:latest`
- **Size**: 856MB
- **Features**: FastAPI, SQLAlchemy, AI Integration

### Frontend  
- **Image**: `patraswaviman1/discharge-iq-frontend:latest`
- **Size**: 856MB
- **Features**: React.js, Nginx, Responsive Design

## 🌐 Access Points

After deployment:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📋 Architecture

```
┌─────────────────┐
│   Frontend    │  (React + Nginx)
│   Port 3000    │
├─────────────────┤
│   Backend     │  (FastAPI + Python)
│   Port 8000    │
├─────────────────┤
│   Database     │  (MySQL)
│   Port 3306    │
└─────────────────┘
```

## 🔧 Environment Variables

Create `.env` file with:
```bash
MYSQL_ROOT_PASSWORD=your_secure_password
MYSQL_DATABASE=discharge_iq
MYSQL_USER=discharge_user
MYSQL_PASSWORD=your_secure_password
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
SECRET_KEY=your_jwt_secret
```

## 🚀 Deployment Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Rebuild Images
```bash
docker-compose build --no-cache
docker-compose up -d
```

## 🎯 Hackathon Ready! 🏆

Your Discharge IQ application is now:
- ✅ **Containerized** - Docker ready
- ✅ **Version Controlled** - Git repository setup
- ✅ **Cloud Deployable** - One-command deployment
- ✅ **Scalable** - Production-ready architecture
- ✅ **AI Powered** - Gemini + OpenAI integration

### 🏆 Winning Features for Hackathon:
1. **Complete Docker Setup** - Multi-service architecture
2. **Cloud-Native** - Ready for AWS/Azure/GCP
3. **AI Integration** - Multiple AI providers
4. **Healthcare Focused** - Purpose-built solution
5. **Professional Deployment** - Industry-standard practices

**Ready to win the cloud hackathon!** 🚀
