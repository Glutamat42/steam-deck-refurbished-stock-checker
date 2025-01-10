FROM python:3.10

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    curl \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

WORKDIR /app
COPY checker.py /app/

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Make the script executable
RUN chmod +x /app/entrypoint.sh

# Use the entrypoint script to start the job
ENTRYPOINT ["/app/entrypoint.sh"]
