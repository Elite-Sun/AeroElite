#!/bin/bash

# Aero Elite Deployment Script
# Deploys both backend and frontend to Google Cloud Run

set -e

echo "🚀 Aero Elite - Automated Deployment Script"
echo "============================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI not found. Please install: https://cloud.google.com/sdk/docs/install${NC}"
    exit 1
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo -e "${RED}❌ .env file not found. Please create it from .env.example${NC}"
    exit 1
fi

# Check required variables
if [ -z "$GCP_PROJECT_ID" ]; then
    echo -e "${YELLOW}⚠️  GCP_PROJECT_ID not set in .env${NC}"
    read -p "Enter your GCP Project ID: " GCP_PROJECT_ID
fi

# Set project
echo -e "${GREEN}✓ Setting GCP project to: $GCP_PROJECT_ID${NC}"
gcloud config set project $GCP_PROJECT_ID

# Enable required APIs
echo -e "${GREEN}✓ Enabling required APIs...${NC}"
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    storage-api.googleapis.com \
    aiplatform.googleapis.com \
    generativelanguage.googleapis.com

# Create Cloud Storage bucket for CAD models
BUCKET_NAME="${CLOUD_STORAGE_BUCKET:-aeroelite-models-$GCP_PROJECT_ID}"
echo -e "${GREEN}✓ Creating Cloud Storage bucket: $BUCKET_NAME${NC}"
gsutil mb -p $GCP_PROJECT_ID gs://$BUCKET_NAME 2>/dev/null || echo "Bucket already exists"

# Create Cloud SQL instance (PostgreSQL)
DB_INSTANCE="${DB_INSTANCE_NAME:-aeroelite-db}"
echo -e "${GREEN}✓ Creating Cloud SQL instance: $DB_INSTANCE${NC}"
gcloud sql instances create $DB_INSTANCE \
    --database-version=POSTGRES_14 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --network=default \
    --no-backup 2>/dev/null || echo "Database instance already exists"

# Create database
echo -e "${GREEN}✓ Creating database: aeroelite${NC}"
gcloud sql databases create aeroelite --instance=$DB_INSTANCE 2>/dev/null || echo "Database already exists"

# Set database password
read -sp "Enter database password (or press Enter for auto-generate): " DB_PASSWORD
echo
if [ -z "$DB_PASSWORD" ]; then
    DB_PASSWORD=$(openssl rand -base64 32)
    echo -e "${YELLOW}Generated password: $DB_PASSWORD${NC}"
fi

gcloud sql users set-password postgres \
    --instance=$DB_INSTANCE \
    --password=$DB_PASSWORD

# Get database connection name
DB_CONNECTION_NAME=$(gcloud sql instances describe $DB_INSTANCE --format='value(connectionName)')
echo -e "${GREEN}✓ Database connection: $DB_CONNECTION_NAME${NC}"

# Deploy Backend to Cloud Run
echo -e "${GREEN}✓ Deploying Backend to Cloud Run...${NC}"
cd backend

gcloud run deploy aeroelite-backend \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --set-env-vars "GCP_PROJECT_ID=$GCP_PROJECT_ID" \
    --set-env-vars "VERTEX_AI_LOCATION=us-central1" \
    --set-env-vars "GEMINI_API_KEY=$GEMINI_API_KEY" \
    --set-env-vars "CLOUD_STORAGE_BUCKET=$BUCKET_NAME" \
    --set-env-vars "JWT_SECRET=$JWT_SECRET" \
    --set-env-vars "DATABASE_URL=postgresql://postgres:$DB_PASSWORD@/$DB_CONNECTION_NAME/aeroelite" \
    --add-cloudsql-instances $DB_CONNECTION_NAME

BACKEND_URL=$(gcloud run services describe aeroelite-backend --region=us-central1 --format='value(status.url)')
echo -e "${GREEN}✓ Backend deployed at: $BACKEND_URL${NC}"

cd ..

# Deploy Frontend to Cloud Run
echo -e "${GREEN}✓ Deploying Frontend to Cloud Run...${NC}"
cd frontend

# Update frontend env with backend URL
cat > .env.production << EOF
REACT_APP_API_URL=$BACKEND_URL
REACT_APP_GOOGLE_CLIENT_ID=$GOOGLE_OAUTH_CLIENT_ID
EOF

gcloud run deploy aeroelite-frontend \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1

FRONTEND_URL=$(gcloud run services describe aeroelite-frontend --region=us-central1 --format='value(status.url)')
echo -e "${GREEN}✓ Frontend deployed at: $FRONTEND_URL${NC}"

cd ..

# Update CORS in backend
echo -e "${GREEN}✓ Updating CORS configuration...${NC}"
# This would require redeploying backend with updated CORS_ORIGINS

# Display deployment info
echo ""
echo "============================================"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "============================================"
echo ""
echo -e "${GREEN}Frontend URL:${NC} $FRONTEND_URL"
echo -e "${GREEN}Backend URL:${NC} $BACKEND_URL"
echo -e "${GREEN}API Docs:${NC} $BACKEND_URL/docs"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Visit $FRONTEND_URL to access Aero Elite"
echo "2. Update CORS settings if needed"
echo "3. Configure custom domain (optional)"
echo "4. Set up monitoring and alerts"
echo ""
echo -e "${GREEN}Database Info:${NC}"
echo "Instance: $DB_INSTANCE"
echo "Connection: $DB_CONNECTION_NAME"
echo "Database: aeroelite"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "- Save your database password: $DB_PASSWORD"
echo "- Update .env file with deployment URLs"
echo "- Configure Google OAuth redirect URIs"
echo ""
