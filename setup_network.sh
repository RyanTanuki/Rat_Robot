#!/bin/bash

# Robot Network Configuration Script
# -------------------------------
# This script configures the network settings for the robot's web interface.
# It sets up:
# - Static IP address
# - Network interface
# - Default route
# - DNS configuration

# Set static IP for wlan0 interface
# Using 192.168.68.75 with subnet mask /24
sudo ip addr add 192.168.68.75/24 dev wlan0

# Ensure wlan0 interface is active
sudo ip link set wlan0 up

# Configure default gateway
sudo ip route add default via 192.168.68.1 dev wlan0

# Configure DNS servers
# Using Google's public DNS servers (8.8.8.8 and 8.8.4.4)
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null
echo "nameserver 8.8.4.4" | sudo tee -a /etc/resolv.conf > /dev/null

# Restart networking service to apply changes
sudo systemctl restart networking 