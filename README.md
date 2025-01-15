# Robot Control Web Application

A web-based control interface for the XiaoRGEEK robot, featuring dual joystick controls, servo sliders, and live video feed.

## Overview

This application provides a web interface to control a robot with:
- Movement control via left joystick or WASD keys
- Camera pan/tilt control via right joystick or arrow keys
- Robotic arm control through 4 servo sliders
- Live video feed from the robot's camera

## System Architecture

The application consists of three main components that need to be running:

1. **Web Server (serve_webpage.py)**
   - Serves the static web interface
   - Handles HTTP requests
   - Runs on port 8001

2. **Flask Backend (python_src/app.py)**
   - Processes control commands
   - Manages GPIO and motor control
   - Runs on port 5000

3. **Robot Control Service (python_src/xr_startmain.py)**
   - Handles low-level robot operations
   - Manages camera stream
   - Controls servos and motors

## Setup and Running

1. Start the video stream:
```
bash
./start_stream.sh
```
2. Start the Flask backend:
```
bash
python3 python_src/app.py
```
3. Start the web server:
```
bash
python3 serve_webpage.py
```


The web interface will be available at:
- Local: `http://localhost:8001/robot_control.html`
- Network: `http://192.168.68.80:8001/robot_control.html`

## Controls

### Movement (Left Joystick or WASD Keys)
- Forward: W or joystick up
- Backward: S or joystick down
- Left: A or joystick left
- Right: D or joystick right
- Stop: Release key/joystick

### Camera (Right Joystick or Arrow Keys)
- Pan Left/Right: Left/Right arrows or joystick left/right
- Tilt Up/Down: Up/Down arrows or joystick up/down

### Servo Controls
- Servo 1-4: Sliders (0-180 degrees)
- Camera Pan: Servo 8 (controlled by right joystick)
- Camera Tilt: Servo 7 (controlled by right joystick)

## API Endpoints

### Motor Control
```
POST /motor
Content-Type: application/json
{
"left": float (-1 to 1),
"right": float (-1 to 1)
}
```
### Servo Control
```
POST /servo
Content-Type: application/json
{
"servo": int (1-8),
"angle": int (0-180)
}
```


## Network Configuration

The robot uses a static IP configuration:
- IP Address: 192.168.68.80
- Video Stream Port: 8080
- Web Server Port: 8001
- Flask Backend Port: 5000

## Files Structure
```
├── robot_control.html # Main web interface
├── serve_webpage.py # Web server
├── python_src/
│ ├── app.py # Flask backend
│ ├── xr_startmain.py # Robot control service
│ └── xr_gpio.py # GPIO management
├── start.sh # Startup script
├── setup_network.sh # Network configuration
└── start_stream.sh # Video stream startup
```

## Troubleshooting

1. **Video Stream Not Working**
   - Check if mjpg-streamer is running
   - Verify camera connection
   - Ensure port 8080 is accessible

2. **Controls Not Responding**
   - Check if Flask backend is running
   - Verify GPIO permissions
   - Check network connectivity

3. **Network Issues**
   - Run setup_network.sh
   - Verify static IP configuration
   - Check network interface status

## Dependencies

- Python 3.7+
- Flask
- RPi.GPIO
- mjpg-streamer
- nipplejs (included via CDN)

## License

This code is provided for educational purposes. Commercial use is prohibited without permission.

## Credits

Developed by XiaoRGEEK Technology (深圳市小二极客科技有限公司)
