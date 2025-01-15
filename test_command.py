import socket
import json

def send_command(command):
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