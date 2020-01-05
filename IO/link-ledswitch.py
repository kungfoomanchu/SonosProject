import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

while True:
    input_state = GPIO.input(13)
    if input_state == False:
        print('Button Pressed')
        # Light on Pin 18
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        # Light on Pin 5
        GPIO.output(5, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(5, GPIO.LOW)
        # Light on Pin 6
        GPIO.output(6, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(6, GPIO.LOW)
        time.sleep(1)