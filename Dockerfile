# Use a base image with build tools
FROM debian:buster

# Install required dependencies to build Python from source
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    git \
    libgdbm-dev \
    libnss3-dev \
    libgdbm-compat-dev \
    uuid-dev

# Set the working directory
WORKDIR /app

# Download Python 3.13 source code
RUN wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz && \
    tar -xvf Python-3.13.0.tgz

# Build and install Python 3.13 from source
WORKDIR /app/Python-3.13.0
RUN ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall

# Verify the Python installation
RUN python3.13 --version

# Set the default Python version to Python 3.13
RUN ln -s /usr/local/bin/python3.13 /usr/bin/python

# Install pip for Python 3.13
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.13 get-pip.py

# Set the working directory back to /app
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Default command to run Django development server
CMD ["python3.13", "manage.py", "runserver", "0.0.0.0:8000"]
