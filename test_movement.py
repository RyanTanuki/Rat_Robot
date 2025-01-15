import requests
import time

def send_command(command):
    try:
        response = requests.post('http://192.168.68.80:2001', json=command)
        print(f"Command: {command}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_movements():
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