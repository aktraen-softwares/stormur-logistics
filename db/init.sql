-- Stormur Logistics — PostgreSQL init
-- This file runs on first container start only.
-- The Django app handles schema creation via migrations.

-- Ensure the database exists (created by POSTGRES_DB env var)
-- Grant full privileges to the application user
GRANT ALL PRIVILEGES ON DATABASE stormur TO stormur;
