#!/bin/bash

# Setup network
/home/pi/work/setup_network.sh

# Wait for network and ensure WiFi is connected
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

# Start the video stream
/home/pi/work/start_stream.sh &

# Start services
sudo systemctl restart xr_robot
sudo systemctl restart robot_control

exit 0