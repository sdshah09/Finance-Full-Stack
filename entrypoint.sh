#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run the development server
exec "$@"
