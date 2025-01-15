#!/bin/bash

# Robot Control System Startup Script
# ---------------------------------
# Main startup script that initializes all components of the robot control system.
# This script:
# 1. Sets up the network
# 2. Starts the video stream
# 3. Initializes the robot control services

# Setup network configuration
/home/pi/work/setup_network.sh

# Wait for network connection and verify WiFi
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if ip addr show wlan0 | grep -q "192.168.68.80"; then
        break
    fi
    echo "Waiting for WiFi connection..."
    attempt=$((attempt + 1))
    sleep 2
done

# Start the video streaming service
/home/pi/work/start_stream.sh &

# Start robot control services
# Restart services to ensure clean state
sudo systemctl restart xr_robot        # Robot control service
sudo systemctl restart robot_control   # Web interface service

exit 0