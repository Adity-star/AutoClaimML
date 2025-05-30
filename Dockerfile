# Dockerfile

# Use an official Python 3.10 image from Docker Hub
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install dependencies without using the cache
RUN pip install --no-cache-dir -r requirements.txt


# Copy the full project
COPY . .


# Expose FastAPI port 
EXPOSE 5000

# Start FastAPI using Uvicorn (recommended for production)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
