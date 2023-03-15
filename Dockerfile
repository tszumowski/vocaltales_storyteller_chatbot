# Use the official Python image as the parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Install FFmpeg and other system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install the required dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the necessary files to the Docker image
COPY storyteller.py config.py ./

# Expose port 7860
EXPOSE 7860

# Set the default command to execute the `storyteller.py` script
CMD ["python", "storyteller.py"]