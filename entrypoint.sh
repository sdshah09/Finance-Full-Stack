#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Run the development server
exec "$@"
