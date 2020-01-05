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
# Added for LEDs
import RPi.GPIO as GPIO
import time
# End Added for LEDs

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


def playPause(room):
    sonosUri = SONOS_BASE_URI + "/%s/playpause" % (room)
    executeSonosCommand(sonosUri)


def executeSonosCommand(sonosUri):
    print("Calling '%s'" % sonosUri)

    # Send command
    response = requests.get(sonosUri)
    print(response.json())
    json_response = response.json()
    json_response = str(json_response)
    if json_response == "{'status': 'success'}":
        print("Sending success signal to LED")
        # Turn On Pin 12 for x Seconds
        GPIO.setup(12, GPIO.OUT)
        GPIO.output(12, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(12, GPIO.LOW)
        # End Turn On Pin 12 for x Seconds
    else:
        print("Sonos Node Server Error")
        # Turn On Pin 31 for x Seconds
        GPIO.setup(31, GPIO.OUT)
        GPIO.output(31, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(31, GPIO.LOW)
        # End Turn On Pin 31 for x Seconds

    if(response.status_code == 200):
        return True
    else:
        return False

