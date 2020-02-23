#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Gerd Saurer <gerd.saurer@gmail.com>
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sonos-nfc-read.  If not, see <http://www.gnu.org/licenses/>.

import requests
import json
import configparser
import time
from time import sleep
from datetime import datetime, timedelta

# # Added for GPIO LEDs
# import RPi.GPIO as GPIO
# import time
# # End Added for GPIO LEDs

# # For BlinkStick
from blinkstick import blinkstick
# # End Added for Blinkstick

# # For JamHat
# # The import of JamHat had to be moved to mysonos.py
from gpiozero import JamHat
# # End Added for JamHat



SONOS_BASE_URI = ""
SONOS_ROOM = ""

config = configparser.ConfigParser()
config.read('settings.ini')
SONOS_BASE_URI = config.get('Sonos', 'Server', fallback='http://localhost:5005')
SONOS_ROOM = config.get('Sonos', 'Room', fallback='Kitchen')

def play(command):
    return playRoom(SONOS_ROOM, command)

def playRoom(room, command):
    sonosUri = SONOS_BASE_URI + "/%s/nfc/%s" % (room, command)
    executeSonosCommand(sonosUri)

def playPause(room, command):
    sonosUri = SONOS_BASE_URI + "/%s/%s" % (room, command)
    executeSonosCommand(sonosUri)

def executeSonosCommand(sonosUri):
    print("Calling '%s'" % sonosUri)

    # Send command
    response = requests.get(sonosUri)
    print(response.json())
    json_response = response.json()
    json_response = str(json_response)
    success = "success"

    if success in json_response:
        print("Sending success signal to LED")

        # # For Jam-HAT
        # Initialise the JamHat object.
        jh = JamHat()
        # # End JamHat
        #
        # i is the counter for the LED row.
        i = 2
        # j is the counter for the LED column.
        j = 2
        # Create counter
        x = 0

        # Setup a try/except block so we can run until CTRL+C is pressed.
        # try:
        for x in range(7):
        #while True:
            # Using modular arithmetic, decrease the light counter.
            # Our lights are in a matrix with rows 0-1 and columns 0-2.
            # Eg. [0][1] is the top yellow LED.
            if(j == 2):
                # If we're at the end of the column, increment to the next row.
                i = (i + 1) % 2
            # Increment the column.
            j = (j + 1) % 3
            sleep(0.2)
            # Turn the hat off.
            jh.off()
            # Turn on the LED at i j on the board.
            jh[i][j].on()
            # Turn the hat off.
            #jh.off()
            # Increment by 1
            x = x + 1
        jh.close()

        try:
            # For BlinkStick
            for bstick in blinkstick.find_all():
                bstick.set_color(name="green")
                bstick.pulse(name="blue")
                time.sleep(3)
                bstick.turn_off()
                continue
            # End BlinkStick
        except:
            print('Blinkstick had some sort of error')

        try:
            # Turn On Pin 12 for x Seconds
            GPIO.setup(12, GPIO.OUT)
            GPIO.output(12, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(12, GPIO.LOW)
            # End Turn On Pin 12 for x Seconds
        except:
            print('GPIO LEDs had some sort of error')

        # except KeyboardInterrupt:
        #     # If someone presses CTRL+C, close the JamHat, freeing of the Pins for use elsewhere.
        #     jh.close()
        # # End Jam-HAT
    else:
        print("Sonos Node Server Error")

        # # For Jam-HAT
        # Initialise the JamHat object.
        jh = JamHat()
        # # End JamHat
        #
        # Build an array of notes in hertz.
        NOTES = [440.000, 391.995, 349.228, 329.628, 293.665, 261.626]

        # Function to play beep for one second
        def play_buzzer():
            end_time = datetime.now() + timedelta(seconds=0.5)
            while datetime.now() < end_time:
                jh.buzzer.play(NOTES[1])

        # Run function
        play_buzzer()
        # Close Jam-Hat
        jh.close()
        # # End Jam-HAT

        try:
            # For BlinkStick
            for bstick in blinkstick.find_all():
                bstick.set_color(name="red")
                time.sleep(3)
                print("Blinkstick lights command successful")
                bstick.turn_off()
            # End BlinkStick
        except:
            print("blinkstick had some sort of error")

        try:
            # # Turn On Pin 31 for x Seconds
            GPIO.setup(31, GPIO.OUT)
            GPIO.output(31, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(31, GPIO.LOW)
            # # End Turn On Pin 31 for x Seconds
        except:
            print("GPIO LEDs had some sort of error")

    if(response.status_code == 200):
        return True
    else:
        return False

