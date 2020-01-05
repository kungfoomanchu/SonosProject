# Wiring Setup

# Wire #1 = ground
# On Breadboard:
# Connect 1K ohm resistor from ground to negative (shorter) side of LED
# Connect Wire #2 to the positive (longer) side of the LED and whichever IO # you want (first we use 18)
# Overall path -> Pi Ground -> Breadboard -> 1k ohm resistor -> negative (shorter) LED wire -> positive (longer) LED wire -> Breadboard for the IO # you chose (#18 first) -> #18 on Pi

# If you don't already have RPi.GPIO, do this in terminal: $ sudo apt-get install python-rpi.gpio

import RPi.GPIO as GPIO
import time

# Set GPIO to Board
GPIO.setmode(GPIO.BOARD)

# Set Up the GPIO Pins
GPIO.setup(12, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)

# Turn On Pin 12 for 3x Seconds
GPIO.output(12, GPIO.HIGH)
time.sleep(1)
GPIO.output(12, GPIO.LOW)
# End Turn On Pin 12 for x Seconds

# Turn On Pin 29 for x Seconds
GPIO.output(29, GPIO.HIGH)
time.sleep(1)
GPIO.output(29, GPIO.LOW)
# End Turn On Pin 29 for x Seconds

# Turn On IO 31 for x Seconds
GPIO.output(31, GPIO.HIGH)
time.sleep(1)
GPIO.output(31, GPIO.LOW)
# End Turn On Pin 31 for x Seconds

# GPIO Cleanup
GPIO.cleanup()