# Dockerfile

# Use an official Python 3.10 image from Docker Hub
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


# Copy the full project
COPY . .


# Expose FastAPI port (default is 8000)
EXPOSE 8000

# Start FastAPI using Uvicorn (recommended for production)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
