# Wiring Setup

# Wire #1 = ground
# On Breadboard:
# Connect 1K ohm resistor from ground to negative (shorter) side of LED
# Connect Wire #2 to the positive (longer) side of the LED and whichever IO # you want (first we use 18)
# Overall path -> Pi Ground -> Breadboard -> 1k ohm resistor -> negative (shorter) LED wire -> positive (longer) LED wire -> Breadboard for the IO # you chose (#18 first) -> #18 on Pi

# If you don't already have RPi.GPIO, do this in terminal: $ sudo apt-get install python-rpi.gpio

import RPi.GPIO as GPIO
import time

# Set GPIO to Broadcom chip used in Raspberry Pi
GPIO.setmode(GPIO.BCM)

# Set Up the GPIO Pins
GPIO.setup(18, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

# Turn On IO 18 for 3 Seconds
GPIO.output(18, GPIO.HIGH)

time.sleep(3)

GPIO.output(18, GPIO.LOW)
# End Turn On IO 18 for 3 Seconds

# Turn On IO 5 for 3 Seconds
GPIO.output(5, GPIO.HIGH)

time.sleep(3)

GPIO.output(5, GPIO.LOW)
# End Turn On IO 5 for 3 Seconds

# Turn On IO 6 for 3 Seconds
GPIO.output(6, GPIO.HIGH)

time.sleep(3)

GPIO.output(6, GPIO.LOW)
# End Turn On IO 6 for 3 Seconds

# GPIO Cleanup
GPIO.cleanup()