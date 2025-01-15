#!/bin/bash

# Robot Video Stream Startup Script
# -------------------------------
# This script initializes the video stream for the robot's web interface.
# It handles:
# - Stopping any existing camera processes
# - Setting up the mjpg-streamer
# - Managing pipewire services
# - Starting the video stream

# Kill any existing processes using the camera
sudo pkill -f mjpg_streamer
systemctl --user stop pipewire      # Stop pipewire to free camera
systemctl --user stop wireplumber   # Stop wireplumber service

# Wait for processes to stop completely
sleep 2

# Set up mjpg-streamer environment
export LD_LIBRARY_PATH=/usr/local/lib/mjpg-streamer

# Start the video stream
# Parameters:
# - input_uvc.so: USB camera input plugin
# - r: Resolution (640x480)
# - f: Framerate (15 fps)
# - output_http.so: HTTP streaming output plugin
# - p: Port (8080)
# - w: Web server root directory
mjpg_streamer -i "input_uvc.so -r 640x480 -f 15" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www" &

# Wait for stream to initialize
sleep 2

# Verify stream is running
if pgrep -f mjpg_streamer > /dev/null; then
    echo "Stream started successfully"
else
    echo "Failed to start stream"
fi

# Restart pipewire services
systemctl --user start pipewire
systemctl --user start wireplumber 