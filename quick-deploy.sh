#!/bin/bash

# Quick Deploy Script - Simplified deployment for Cloud Run

set -e

echo "🚀 Aero Elite - Quick Deploy to Cloud Run"
echo "=========================================="

# Check if user is logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "Please login to Google Cloud:"
    gcloud auth login
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)

if [ -z "$PROJECT_ID" ]; then
    echo "No project set. Please select or create a project:"
    gcloud projects list
    read -p "Enter Project ID: " PROJECT_ID
    gcloud config set project $PROJECT_ID
fi

echo "Using project: $PROJECT_ID"

# Enable APIs
echo "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# Deploy backend
echo ""
echo "📦 Deploying Backend..."
cd backend

gcloud run deploy aeroelite-backend \
    --source . \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated \
    --memory=2Gi \
    --timeout=300 \
    --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID,VERTEX_AI_LOCATION=us-central1"

BACKEND_URL=$(gcloud run services describe aeroelite-backend --region=us-central1 --format='value(status.url)')

echo "✅ Backend deployed: $BACKEND_URL"

cd ..

# Deploy frontend
echo ""
echo "🎨 Deploying Frontend..."
cd frontend

# Create production env
cat > .env.production << EOF
REACT_APP_API_URL=$BACKEND_URL
EOF

gcloud run deploy aeroelite-frontend \
    --source . \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated \
    --memory=512Mi

FRONTEND_URL=$(gcloud run services describe aeroelite-frontend --region=us-central1 --format='value(status.url)')

echo "✅ Frontend deployed: $FRONTEND_URL"

cd ..

# Summary
echo ""
echo "============================================"
echo "🎉 Deployment Complete!"
echo "============================================"
echo ""
echo "🌐 Application URL: $FRONTEND_URL"
echo "🔌 API URL: $BACKEND_URL"
echo "📚 API Docs: $BACKEND_URL/docs"
echo ""
echo "⚠️  Note: For full functionality, you need to:"
echo "1. Set up environment variables in Cloud Run console"
echo "2. Add Gemini API key"
echo "3. Configure database (optional)"
echo ""
echo "Visit: https://console.cloud.google.com/run"
echo ""
