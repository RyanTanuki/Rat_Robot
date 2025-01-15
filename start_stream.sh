#!/bin/bash

# Kill any existing processes using the camera
sudo pkill -f mjpg_streamer
systemctl --user stop pipewire
systemctl --user stop wireplumber

# Wait for processes to stop
sleep 2

# Start the streamer
export LD_LIBRARY_PATH=/usr/local/lib/mjpg-streamer
mjpg_streamer -i "input_uvc.so -r 640x480 -f 15" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www" &

# Wait a moment
sleep 2

# Check if the process is running
if pgrep -f mjpg_streamer > /dev/null; then
    echo "Stream started successfully"
else
    echo "Failed to start stream"
fi

# Restart pipewire
systemctl --user start pipewire
systemctl --user start wireplumber 