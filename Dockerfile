# Base image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    gcc \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libfreetype6-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    python3-dev \
    build-essential \
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

# Copy entrypoint script and set permissions
COPY entrypoint.sh /home/financial_backend/entrypoint.sh
RUN chmod +x /home/financial_backend/entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Set the entrypoint
# ENTRYPOINT ["/home/financial_backend/entrypoint.sh"]


# Command to run Django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
