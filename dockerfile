FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    curl \
    nano \
    cron
RUN rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY checker.py /app/
COPY requirements.txt /app/

# Install dependencies using pip as root (default user)
RUN pip install -r /app/requirements.txt

# Create a script to generate crontab from environment variable
RUN echo '#!/bin/bash\n\
CRON_SCHEDULE=${CRON_SCHEDULE:-"*/5 * * * *"}\n\
# Export environment variables to cron environment\n\
printenv | grep -E "^(DISCORD_WEBHOOK_URL|PRODUCT_TITLES|DEBUG|PAGE_URL)=" > /etc/environment\n\
echo "$CRON_SCHEDULE root . /etc/environment; PATH=/usr/local/bin:$PATH python3 /app/checker.py > /proc/1/fd/1 2>&1" > /etc/cron.d/steamdeck_checker\n\
echo "" >> /etc/cron.d/steamdeck_checker\n\
chmod 644 /etc/cron.d/steamdeck_checker\n\
exec cron -f' > /app/start.sh && chmod +x /app/start.sh

# Run the start script
ENTRYPOINT ["/app/start.sh"]
