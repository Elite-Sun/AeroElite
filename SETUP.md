# Aero Elite - Setup & Deployment Guide

## Quick Start (Local Development)

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 14+
- Redis (optional)
- Google Cloud Platform account (for AI features)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/AeroElite.git
cd AeroElite
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp ../.env.example .env
# Edit .env with your configuration

# Initialize database
# Make sure PostgreSQL is running
createdb aeroelite

# Run migrations (database tables will be created automatically)
python -m app.main

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
# Edit with your configuration

# Start development server
npm start
```

Frontend will be available at: http://localhost:3000

### 4. Database Setup (PostgreSQL)

```bash
# Install PostgreSQL
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL
# macOS: brew services start postgresql
# Ubuntu: sudo service postgresql start

# Create database
createdb aeroelite

# Create user (optional)
psql postgres
CREATE USER aeroelite WITH PASSWORD 'aeroelite_password';
GRANT ALL PRIVILEGES ON DATABASE aeroelite TO aeroelite;
```

## Google Cloud Platform Setup

### 1. Create GCP Project

1. Go to https://console.cloud.google.com/
2. Create new project: "aeroelite"
3. Enable APIs:
   - Vertex AI API
   - Cloud Storage API
   - Cloud SQL API
   - Generative AI API

### 2. Setup Vertex AI

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Create service account
gcloud iam service-accounts create aeroelite-sa \
    --display-name="Aero Elite Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:aeroelite-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:aeroelite-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Create key
gcloud iam service-accounts keys create gcp-key.json \
    --iam-account=aeroelite-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Move to backend directory
mv gcp-key.json backend/
```

### 3. Setup Gemini API

1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Add to .env file: `GEMINI_API_KEY=your-key-here`

### 4. Setup Cloud Storage

```bash
# Create bucket for CAD models
gsutil mb -p YOUR_PROJECT_ID gs://aeroelite-models

# Set bucket permissions
gsutil iam ch serviceAccount:aeroelite-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com:objectAdmin gs://aeroelite-models
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Copy environment file
cp .env.example .env
# Edit .env with your settings

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Manual Docker Build

```bash
# Backend
cd backend
docker build -t aeroelite-backend .
docker run -p 8000:8000 --env-file .env aeroelite-backend

# Frontend
cd frontend
docker build -t aeroelite-frontend .
docker run -p 3000:80 aeroelite-frontend
```

## Cloud Deployment (GCP)

### Deploy to Cloud Run

```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy backend
cd backend
gcloud run deploy aeroelite-backend \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="$(cat .env | grep -v '^#' | xargs)"

# Deploy frontend
cd frontend
gcloud run deploy aeroelite-frontend \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Deploy to Google Kubernetes Engine (GKE)

```bash
# Create cluster
gcloud container clusters create aeroelite-cluster \
    --num-nodes=3 \
    --zone=us-central1-a

# Get credentials
gcloud container clusters get-credentials aeroelite-cluster --zone=us-central1-a

# Apply Kubernetes configurations
kubectl apply -f k8s/

# Check deployment
kubectl get pods
kubectl get services
```

## Dataset Download

### AircraftVerse

```bash
# Using wget
wget https://zenodo.org/record/6525446/files/aircraftverse.zip
unzip aircraftverse.zip -d backend/datasets/aircraftverse/

# Or use Python script
python backend/scripts/download_datasets.py --dataset aircraftverse
```

### G2Aero Airfoil Database

```bash
# Download from OpenEI
python backend/scripts/download_datasets.py --dataset g2aero
```

### NASA CRM

```bash
# Visit: https://commonresearchmodel.larc.nasa.gov/
# Download CAD files manually
# Place in: backend/datasets/nasa_crm/
```

## Environment Variables

### Backend (.env)

```env
# GCP
GCP_PROJECT_ID=your-project-id
VERTEX_AI_LOCATION=us-central1
GEMINI_API_KEY=your-gemini-api-key
CLOUD_STORAGE_BUCKET=aeroelite-models

# Database
DATABASE_URL=postgresql://aeroelite:password@localhost:5432/aeroelite

# Auth
JWT_SECRET=your-super-secret-key
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend (.env.local)

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check PostgreSQL is running
pg_isready
# Verify credentials in .env
```

**2. GCP Authentication Error**
```bash
# Re-authenticate
gcloud auth application-default login
# Check service account key
export GOOGLE_APPLICATION_CREDENTIALS="path/to/gcp-key.json"
```

**3. CAD Generation Fails**
```bash
# Ensure pythonOCC and CadQuery are installed
pip install --upgrade cadquery pythonOCC-core
```

**4. Frontend Can't Connect to Backend**
```bash
# Check CORS settings in backend/app/core/config.py
# Verify REACT_APP_API_URL in frontend/.env.local
```

## Performance Optimization

### Backend

- Use Redis for caching
- Enable gzip compression
- Use connection pooling for database
- Deploy with gunicorn/uvicorn workers

### Frontend

- Enable production build: `npm run build`
- Use CDN for static assets
- Enable lazy loading for routes
- Optimize Three.js rendering

## Security Checklist

- [ ] Change default JWT_SECRET
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Implement input validation
- [ ] Setup monitoring and logging
- [ ] Regular security updates

## Monitoring

### Cloud Monitoring (GCP)

```bash
# Enable Cloud Monitoring
gcloud services enable monitoring.googleapis.com

# View logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

### Local Monitoring

```bash
# Backend logs
tail -f backend/logs/aeroelite.log

# Frontend logs
# Check browser console
```

## Support

- Documentation: [docs.aeroelite.com](https://docs.aeroelite.com)
- Issues: [GitHub Issues](https://github.com/yourusername/AeroElite/issues)
- Email: support@aeroelite.com

## License

MIT License - see LICENSE file
