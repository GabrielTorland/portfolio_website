# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    # any other dependencies you might need
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies
# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV SMTP_SERVER "smtp.gmail.com"
ENV SMTP_PORT "587"
ENV SMTP_USER "user@example.com" 
ENV SMTP_PASSWORD "password"
ENV SMTP_RECEIVER "otheruser@example.com"
ENV REDIS_URL "redis://redis:6379"
ENV DATABASE_URI "postgresql://postgres:postgres@db:5432/postgres"

# Run app.py when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]