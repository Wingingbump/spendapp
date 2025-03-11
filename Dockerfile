# Use a base image with Python and necessary dependencies
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /workspace

# Copy requirements.txt and install dependencies
COPY backend/requirements.txt /workspace/
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# Install Git
RUN apt-get update && apt-get install -y git

FROM debian:latest
RUN apt-get update && \
    apt-get install -y bash --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-c"]

# Expose any ports the app might need (for example, for Flask)
EXPOSE 5000

# Command to start the app (replace with your actual app entry point)
CMD ["python", "app.py"]
