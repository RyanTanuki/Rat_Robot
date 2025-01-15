from gpiozero import LED as GPIO
import time
GPIO = GPIO(19)
while True:
    GPIO.on()
    print(GPIO,"is on")
    time.sleep(2)
    GPIO.off()
    print(GPIO,"is off")
    time.sleep(2)