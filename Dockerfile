# Base image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /home/financial_backend

# Install dependencies
COPY requirements.txt /home/financial_backend
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /home/financial_backend

# Expose port 8000
EXPOSE 8000

# Command to run Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
