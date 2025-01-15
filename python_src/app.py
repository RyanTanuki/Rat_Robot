# Remove the pin factory setting
# import os
# os.environ['GPIOZERO_PIN_FACTORY'] = 'pigpio'  # Remove or comment out this line

from flask import Flask, render_template, request, jsonify
import sys
import os
import logging
import socket
import json
import atexit
import RPi.GPIO as GPIO

# Add python_src to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'python_src'))

# Import GPIO and motor control
import xr_gpio as gpio
from xr_motor import RobotDirection

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/robot_control.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__, 
    template_folder=os.path.dirname(os.path.dirname(__file__)),  # Look in parent directory for templates
    static_folder=os.path.dirname(os.path.dirname(__file__)))    # Look in parent directory for static files

# Default robot settings
ROBOT_IP = "192.168.68.80"
ROBOT_PORT = 2001
STREAM_URL = f"http://{ROBOT_IP}:8080/?action=stream"

# Initialize robot controller
robot = RobotDirection()

def send_command(command_dict):
    """Send command to robot control script via TCP"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 2001))
            s.send(json.dumps(command_dict).encode())
            response = s.recv(1024).decode()
            return json.loads(response)
    except Exception as e:
        logging.error(f"Failed to send command: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.route("/motor", methods=["POST"])
def motor_control():
    try:
        data = request.get_json()
        left = float(data.get('left', 0))
        right = float(data.get('right', 0))
        
        # Convert -1 to 1 range to 0-100 speed range
        left_speed = int(abs(left) * 100)
        right_speed = int(abs(right) * 100)
        
        logging.debug(f"Motor control: left={left_speed}, right={right_speed}")
        
        # Set motor speeds
        robot.set_speed(1, left_speed)  # Left motors
        robot.set_speed(2, right_speed) # Right motors
        
        # Determine direction and control motors
        if left > 0 and right > 0:
            robot.forward()
            direction = "forward"
        elif left < 0 and right < 0:
            robot.back()
            direction = "backward"
        elif left < right:
            robot.left()
            direction = "left"
        elif right < left:
            robot.right()
            direction = "right"
        else:
            robot.stop()
            direction = "stop"
        
        return jsonify({"status": "success", "direction": direction})
    except Exception as e:
        logging.error(f"Motor control error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route("/servo", methods=["POST"])
def servo_control():
    try:
        data = request.get_json()
        servo_id = int(data.get('servo'))
        angle = int(data.get('angle'))
        
        logging.debug(f"Servo control: id={servo_id}, angle={angle}")
        
        if 1 <= servo_id <= 8:
            command = {
                "type": "servo",
                "id": servo_id,
                "angle": angle
            }
            return jsonify(send_command(command))
        else:
            return jsonify({"status": "error", "message": "Invalid servo ID"})
    except Exception as e:
        logging.error(f"Servo control error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route("/", methods=["GET"])
@app.route("/robot_control.html", methods=["GET"])  # Add this route
def index():
    return render_template("robot_control.html",    # Change template name
                         ip=ROBOT_IP, 
                         port=ROBOT_PORT, 
                         stream_url=STREAM_URL)

def cleanup():
    """Cleanup GPIO resources"""
    try:
        GPIO.cleanup()
        logging.info("GPIO resources cleaned up")
    except Exception as e:
        logging.error(f"Cleanup error: {str(e)}")

# Register cleanup function
atexit.register(cleanup)

if __name__ == "__main__":
    try:
        logging.info("Starting Robot Control Web Application")
        app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)
    except Exception as e:
        logging.error(f"Failed to start application: {str(e)}")
        cleanup()
        sys.exit(1) 