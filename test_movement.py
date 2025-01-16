"""
Robot Movement Test Module

This module provides comprehensive testing of the robot's movement capabilities
including motor control, camera servos, and arm servos. It sends HTTP commands
to control various aspects of the robot's motion.

Test Categories:
- Basic robot movement (forward, stop, turn)
- Camera pan/tilt control
- Robotic arm positioning
"""

import requests
import time

def send_command(command):
    """
    Sends a movement command to the robot's control server.
    
    Args:
        command (dict): Movement command dictionary containing:
            - type: Command type (motor/servo)
            - Additional parameters specific to the command type
            
    Prints both the command sent and the server's response.
    """
    try:
        response = requests.post('http://192.168.68.80:2001', json=command)
        print(f"Command: {command}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_movements():
    """
    Executes a series of movement tests for different robot components.
    
    Tests three main systems:
    1. Robot base movement (forward, stop, left turn)
    2. Camera movement (pan and tilt)
    3. Arm movement (base, shoulder, elbow, gripper)
    
    Each movement is followed by a 1-second delay to allow completion.
    """
    # Test robot movement
    movements = [
        {"type": "motor", "direction": "forward", "left": 50, "right": 50},
        {"type": "motor", "direction": "stop", "left": 0, "right": 0},
        {"type": "motor", "direction": "left", "left": 50, "right": 50},
        {"type": "motor", "direction": "stop", "left": 0, "right": 0}
    ]
    
    # Test camera movement
    camera_movements = [
        {"type": "servo", "id": 8, "angle": 45},  # Pan left
        {"type": "servo", "id": 8, "angle": 90},  # Pan center
        {"type": "servo", "id": 7, "angle": 45},  # Tilt up
        {"type": "servo", "id": 7, "angle": 90}   # Tilt center
    ]
    
    # Test arm movement
    arm_movements = [
        {"type": "servo", "id": 1, "angle": 90},  # Base center
        {"type": "servo", "id": 2, "angle": 90},  # Shoulder center
        {"type": "servo", "id": 3, "angle": 90},  # Elbow center
        {"type": "servo", "id": 4, "angle": 90}   # Gripper center
    ]
    
    print("Testing robot movement...")
    for cmd in movements:
        send_command(cmd)
        time.sleep(1)
    
    print("\nTesting camera movement...")
    for cmd in camera_movements:
        send_command(cmd)
        time.sleep(1)
    
    print("\nTesting arm movement...")
    for cmd in arm_movements:
        send_command(cmd)
        time.sleep(1)

if __name__ == "__main__":
    test_movements() 