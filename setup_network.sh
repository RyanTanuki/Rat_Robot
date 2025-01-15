#!/bin/bash

# Set static IP for wlan0
sudo ip addr add 192.168.68.75/24 dev wlan0

# Bring up wlan0 interface
sudo ip link set wlan0 up

# Add default route
sudo ip route add default via 192.168.68.1 dev wlan0

# Set DNS servers
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null
echo "nameserver 8.8.4.4" | sudo tee -a /etc/resolv.conf > /dev/null

# Restart networking
sudo systemctl restart networking 