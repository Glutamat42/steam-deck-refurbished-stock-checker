FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Set working directory
WORKDIR /app

# Copy the Python script into the container
COPY checker.py /app/

# Command to run the Python script
CMD ["python3", "/app/checker.py"]
