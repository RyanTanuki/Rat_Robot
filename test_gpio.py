"""
GPIO and Motor Control Test Module

This module tests the basic functionality of motor controls using GPIO pins.
It performs a simple test of single motor movement to verify the motor
control system is working correctly.

Dependencies:
    - xr_gpio: Custom GPIO control module
    - xr_motor: Robot direction control module
"""

import sys
import os
import time

# Add python_src to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'python_src'))

# Import GPIO and motor control
import xr_gpio as gpio
from xr_motor import RobotDirection

def test_single_motor():
    """
    Tests single motor functionality by controlling the left motor (M1/M2).
    
    The test sequence:
    1. Initializes the robot direction control
    2. Sets the left motor speed to 50%
    3. Runs the motor forward for 2 seconds
    4. Stops the motor
    
    Exceptions are caught and handled to ensure motors are stopped
    even if the test fails.
    """
    print("Testing single motor movement...")
    try:
        robot = RobotDirection()
        
        # Set only the left motor speed (M1/M2)
        print("\nSetting left motor speed...")
        robot.set_speed(1, 50)  # Set left motor to 50% speed
        
        # Move only M1/M2 motor forward
        print("\nMoving left motor forward...")
        robot.m1m2_forward()
        time.sleep(2)
        
        # Stop the motor
        print("\nStopping motor...")
        robot.m1m2_stop()
        
        print("\nSingle motor test completed successfully")
        
    except Exception as e:
        print(f"Motor test failed: {e}")
    finally:
        # Ensure motors are stopped
        try:
            robot.m1m2_stop()
            robot.set_speed(1, 0)
        except:
            pass

if __name__ == "__main__":
    print("Starting single motor test...")
    test_single_motor() 