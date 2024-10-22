# Use the official Python 3.12.5 slim image
FROM python:3.12.5-slim

# Install system dependencies, including GObject and GObject introspection
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libgirepository1.0-dev \
    gobject-introspection \
    gir1.2-glib-2.0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /home/ubuntu/Finance-Full-Stack

# Copy the requirements.txt file into the working directory
COPY requirements.txt /home/ubuntu/Finance-Full-Stack/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /home/ubuntu/Finance-Full-Stack/requirements.txt

# Copy all project files into the working directory
COPY . /home/ubuntu/Finance-Full-Stack

# Expose port 8000 for the Django development server
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
