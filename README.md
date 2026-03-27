# Stormur Logistics — Internal Tracking Platform

Shipment tracking and logistics management platform for Stormur Logistics AS.

## Quick Start

```bash
docker compose up -d
```

The application will be available at `http://track.stormur.com` (port 80).

## Architecture

- **Django 5.1** application with PostgreSQL 16
- Gunicorn WSGI server on port 8000, mapped to port 80
- Static files served by Django (whitenoise-less, collectstatic to disk)

## Services

| Service | Port | Description |
|---------|------|-------------|
| `app` | 80 (ext) / 8000 (int) | Django application |
| `db` | 5432 | PostgreSQL 16 |

## User Accounts

| Email | Role |
|-------|------|
| `auditor@stormur.com` | User |
| `admin@stormur.com` | Administrator |
| `ops@stormur.com` | User |

## Features

- Package tracking by tracking number
- Shipment history
- User profile management
- Admin panel with shipment search
- REST API for shipment queries

## Database

PostgreSQL with the following application tables:

- `auth_user` — Django authentication
- `shipments_shipment` — Shipment records
- `shipments_customer` — Customer records
- `shipments_userprofile` — Extended user profiles
- `django_session` — Session storage

## Development

```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f app

# Run migrations manually
docker compose exec app python manage.py migrate

# Re-seed data
docker compose exec app python manage.py seed
```
