# Use an official Python runtime as a parent image
#FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Make port 2387 available to the world outside this container
EXPOSE 2387

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:2387", "--log-level", "debug", "app:app"]
