# syntax=docker/dockerfile:1
FROM python:3.12-alpine

# Disable Python .pyc files and enable real-time logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (e.g., build tools, pip requirements)
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Run the main script
CMD ["python", "main.py"]
