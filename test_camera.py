"""
Camera Test Module

This module provides comprehensive testing of the robot's camera functionality.
It handles service management, camera initialization, and frame capture testing.

Features:
- Stops potentially conflicting robot services
- Verifies camera device presence
- Tests frame capture capabilities
- Measures actual FPS performance
- Saves a test frame for visual verification
"""

import cv2
import time
import os
import subprocess

def stop_robot_services():
    """
    Stops any running robot services that might interfere with camera testing.
    
    Attempts to stop:
    - xr_robot systemd service
    - Any running instances of xr_startmain.py
    
    Warnings are logged if services cannot be stopped.
    """
    print("Stopping robot services...")
    try:
        # Stop the robot service
        subprocess.run(['sudo', 'systemctl', 'stop', 'xr_robot'], check=True)
        # Kill any Python processes using the camera
        subprocess.run(['sudo', 'pkill', '-f', 'xr_startmain.py'], check=True)
        time.sleep(2)  # Give time for services to stop
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to stop some services: {e}")

def test_camera():
    """
    Performs a comprehensive test of the camera system.
    
    Test sequence:
    1. Stops potential conflicting services
    2. Verifies camera device presence
    3. Initializes camera and prints properties
    4. Captures 100 frames while measuring performance
    5. Saves first frame as reference
    6. Calculates and reports actual FPS
    7. Restarts robot services after completion
    
    Results are printed to console, including FPS and timing data.
    """
    # Stop other services first
    stop_robot_services()
    
    # Check if camera exists
    if not os.path.exists('/dev/video0'):
        print("Error: Camera device /dev/video0 not found!")
        return
        
    # Try to open camera
    print("Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera!")
        print("Checking processes using camera:")
        os.system('sudo lsof /dev/video0')
        return
    
    # Print camera properties
    print(f"FPS: {cap.get(cv2.CAP_PROP_FPS)}")
    print(f"Resolution: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
    
    # Test frame capture speed
    start_time = time.time()
    frame_count = 0
    
    try:
        while frame_count < 100:  # Capture 100 frames
            ret, frame = cap.read()
            if ret:
                frame_count += 1
                # Save first frame as test
                if frame_count == 1:
                    cv2.imwrite('test_frame.jpg', frame)
                    print("Saved test frame as 'test_frame.jpg'")
                if frame_count % 10 == 0:  # Print every 10 frames
                    print(f"Captured frame {frame_count} at {time.time() - start_time:.2f} seconds")
            else:
                print("Failed to capture frame")
                break
            
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Error during capture: {e}")
    finally:
        cap.release()
        elapsed_time = time.time() - start_time
        print(f"\nResults:")
        print(f"Total frames: {frame_count}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        if frame_count > 0:
            print(f"Average FPS: {frame_count/elapsed_time:.2f}")
        
        print("\nRestarting robot services...")
        subprocess.run(['sudo', 'systemctl', 'restart', 'xr_robot'])

if __name__ == "__main__":
    test_camera() 