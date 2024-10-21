# Use the official Python 3.12.5 slim image from Docker Hub
FROM python:3.12.5-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/

# Expose port 8000 (Django development server runs on this port)
EXPOSE 8000

# Default command to run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
