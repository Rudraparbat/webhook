#!/bin/sh

set -e  


echo "Running makemigrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate


echo "Starting Django server..."

python manage.py runserver 0.0.0.0:8000

exec "$@"