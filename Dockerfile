# Use the official Python image as the parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the necessary files to the Docker image
COPY storyteller.py config.py requirements.txt ./

# Install FFmpeg and other system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to execute the `storyteller.py` script
CMD ["python", "storyteller.py"]