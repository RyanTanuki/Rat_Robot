"""
Robot Command Test Module

This module tests the robot's command interface by sending test commands
over a TCP socket connection. It verifies both motor movement and servo
control functionality.

The test sends JSON-formatted commands to control:
- Forward movement of the robot
- Servo position adjustment
"""

import socket
import json

def send_command(command):
    """
    Sends a JSON command to the robot control server.
    
    Args:
        command (dict): Command dictionary to be sent to the robot
                       Expected format varies by command type
                       
    Prints the command being sent and the response received.
    Handles connection errors gracefully.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 2001))
        print(f"Sending command: {command}")
        sock.send(json.dumps(command).encode())
        response = sock.recv(1024).decode()
        print(f"Response: {response}")
        sock.close()
    except Exception as e:
        print(f"Error: {e}")

# Test forward movement
forward_command = {
    "type": "motor",
    "direction": "forward",
    "left": 50,
    "right": 50
}

# Test servo movement
servo_command = {
    "type": "servo",
    "id": 1,
    "angle": 90
}

print("Testing forward movement...")
send_command(forward_command)

print("\nTesting servo movement...")
send_command(servo_command) 