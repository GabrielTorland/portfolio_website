# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Prevent Python from writing pyc files to disc and from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Run the application as a non-root user for security
RUN useradd -m myuser
USER myuser

# Make port 2387 available to the world outside this container
EXPOSE 2387

# Healthcheck to ensure service is running
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:2387/ || exit 1

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:2387", "--timeout", "90", "app:app"]
