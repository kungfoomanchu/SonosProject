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

import nfcpy_lights


# Clear variables. Not sure if this is necessary
SONOS_BASE_URI = ""
SONOS_ROOM = ""

# Import Variables form settings.ini file
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

def playRoomLights(command, lightsonoff, lighttype, forcedresponse):
    sonosUri = SONOS_BASE_URI + f'/{SONOS_ROOM}/nfc/{command}'
    executeSonosCommandLights(sonosUri, lightsonoff, lighttype, forcedresponse)


def executeSonosCommandLights(sonosUri, lightsonoff, lighttype, forcedresponse):
    print("Calling '%s'" % sonosUri)

    # Send command
    response = requests.get(sonosUri)
    print(response.json())
    json_response = response.json()
    json_response = str(json_response)
    success = "success"

    if success in json_response:
        print("Sending success signal to LED from executeSonosCommandLights")
        forcedresponse = "success"
        # Send lights command
        nfcpy_lights.lightsDef(lightsonoff, lighttype, forcedresponse)

    else:
        print("Sonos Node Server Error")
        forcedresponse = "error"
        # Send lights command
        nfcpy_lights.lightsDef(lightsonoff, lighttype, forcedresponse)

    if(response.status_code == 200):
        return True
    else:
        return False


def executeSonosCommand(sonosUri):
    print("Calling '%s'" % sonosUri)

    # Send command
    response = requests.get(sonosUri)
    print(response.json())
    json_response = response.json()
    json_response = str(json_response)
    success = "success"

    if(response.status_code == 200):
        return True
    else:
        return False

