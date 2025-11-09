-- Initialize Aero Elite Database
-- This script is run automatically when the database container starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE aeroelite TO aeroelite;

-- Create initial tables (will be created by SQLAlchemy, this is just for reference)
-- Tables: users, aircraft_designs, components, parameters, assemblies, assembly_components, dataset_entries, airfoil_profiles

-- Insert sample data for testing
-- This will be populated by the application

COMMIT;
