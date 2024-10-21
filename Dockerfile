# Use the official Python 3.12.5 slim image
FROM python:3.12.5-slim

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/

# Collect static files for production (if needed)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
