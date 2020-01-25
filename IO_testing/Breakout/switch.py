# Wiring Setup
# No resistor needed. Just attach an IO# and a ground

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(19)
    if input_state == False:
        print('Button Pressed')
        time.sleep(1)
        
# GPIO Cleanup
GPIO.cleanup()
print('GPIO Cleaned Up')