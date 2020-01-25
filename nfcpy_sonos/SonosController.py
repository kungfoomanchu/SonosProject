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

# TODO Make light show dependent on 'lights' variable
def executeSonosCommand(sonosUri):
    print("Calling '%s'" % sonosUri)

    # Send command
    response = requests.get(sonosUri)
    print(response.json())
    json_response = response.json()
    json_response = str(json_response)
    success = "success"
    # TODO: this is not detecting an error correctly. Not sure why
    if success in json_response:
        print("Success, but no LED in this script")
    else:
        print("Failure, but no LED in this script")
    if(response.status_code == 200):
        return True
    else:
        return False

