#!/bin/bash

# Discharge IQ - Cloud Deployment Script
# For AWS Cloud Hackathon

echo "🚀 Starting Discharge IQ Cloud Deployment..."

# Check if Docker is running
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or running"
    exit 1
fi

# Set variables
BACKEND_IMAGE="patraswaviman1/discharge-iq-backend:latest"
FRONTEND_IMAGE="patraswaviman1/discharge-iq-frontend:latest"

echo "📦 Pulling Docker images..."
docker pull $BACKEND_IMAGE
docker pull $FRONTEND_IMAGE

echo "🗄️ Stopping existing containers..."
docker-compose down 2>/dev/null || true

echo "🚀 Starting services with Docker Compose..."
docker-compose up -d

echo "✅ Deployment complete!"
echo ""
echo "🌐 Access your application:"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo ""
echo "📊 Check logs with:"
echo "docker-compose logs -f"
