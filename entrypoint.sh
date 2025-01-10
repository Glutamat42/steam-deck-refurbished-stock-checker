#!/bin/bash

# Run the Python script every minute
while true; do
    python3 /app/checker.py
    sleep 150  # Sleep for 150 seconds
done
