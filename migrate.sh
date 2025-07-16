#!/bin/bash
set -e

echo "Waiting for database to be ready..."
sleep 5

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Migrations completed successfully!"