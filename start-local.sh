#!/bin/bash

# Local deployment script for testing
# Combines backend and frontend in development mode

set -e

echo "🚀 Starting Aero Elite (Local Development)"
echo "=========================================="

# Check dependencies
echo "Checking dependencies..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Installing Docker is recommended."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your configuration"
    echo "Press Enter when ready..."
    read
fi

# Start with Docker Compose
echo ""
echo "Starting services with Docker Compose..."
docker-compose up -d

echo ""
echo "✅ Services started!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🗄️  Database: localhost:5432"
echo ""
echo "📋 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop:"
echo "   docker-compose down"
echo ""
echo "⚙️  To restart:"
echo "   docker-compose restart"
echo ""
