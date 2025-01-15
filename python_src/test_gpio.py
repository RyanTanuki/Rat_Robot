import xr_gpio
import time

print("Starting GPIO tests...")

try:
    print("\nTesting LED flash sequence...")
    xr_gpio.LED_flash()
    print("LED flash completed")
    
    print("\nTesting individual LEDs...")
    # Test each LED individually
    leds = [xr_gpio.LED0, xr_gpio.LED1, xr_gpio.LED2]
    for led in leds:
        print(f"Testing LED on pin {led}")
        xr_gpio.digital_write(led, True)
        time.sleep(0.5)
        xr_gpio.digital_write(led, False)
        time.sleep(0.5)
    print("Individual LED tests completed")
    
except Exception as e:
    print(f"Test failed: {e}") 