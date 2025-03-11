# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container to the backend directory
WORKDIR /app/backend

# Copy all files from the local machine into the container's /app/backend directory
COPY . /app/backend

# Install only missing or outdated dependencies
RUN pip install --no-cache-dir --upgrade --no-deps -r /app/backend/requirements.txt

# Expose the application port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]



