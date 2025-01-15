import sys
import os
import time

# Add python_src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try gpiozero cleanup
    from gpiozero import Device
    from gpiozero.pins.native import NativeFactory
    Device.pin_factory = NativeFactory()
    Device.pin_factory.reset()
    print("GPIO pins reset using gpiozero")
except:
    pass

try:
    # Also try RPi.GPIO cleanup
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    print("GPIO pins cleaned up using RPi.GPIO")
except:
    pass

# Give system time to release pins
time.sleep(1) 