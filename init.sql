-- Database initialization script
-- This script runs when the PostgreSQL container starts for the first time

-- Create application database if it doesn't exist
CREATE DATABASE IF NOT EXISTS flask_app;

-- Create application user if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'flask_user') THEN
        CREATE USER flask_user WITH PASSWORD 'flask_password';
    END IF;
END
$$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE flask_app TO flask_user;

-- Connect to the application database
\c flask_app;

-- Create sample tables (optional - for future use)
CREATE TABLE IF NOT EXISTS app_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    level VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    endpoint VARCHAR(100),
    ip_address INET
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_app_logs_timestamp ON app_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_app_logs_level ON app_logs(level);

-- Grant table permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flask_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO flask_user;
