#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Gerd Saurer <gerd.saurer@gmail.com>
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sonos-nfc-read.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import math
import SonosController
import NFCHelper
import argparse

continue_reading = True
is_test = False

## _________LED Setup____________
# Set GPIO to Broadcom chip used in Raspberry Pi
GPIO.setmode(GPIO.BOARD)
## _________End LED Setup____________

## Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    print("GPIO Cleaned")
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

parser = argparse.ArgumentParser(description='Write NFC tags for sonos.')
parser.add_argument('-test', type=bool, default=False, help='Just test the read but dont perform the action on sonos')
parser.add_argument('-sonosUri', type=str, default=SonosController.SONOS_BASE_URI, help='The Sonos base Uri to use')
parser.add_argument('-sonosRoom', type=str, default=SonosController.SONOS_ROOM, help='The Sonos room to play the content at')
#parser.add_argument('-nfcKey', type=str, default='FF:FF:FF:FF:FF:FF', help='The hex code of the nfc key to writ the content default: FF:FF:FF:FF:FF:FF')
args = parser.parse_args()

is_test = args.test
SonosController.SONOS_BASE_URI = args.sonosUri
SonosController.SONOS_ROOM = args.sonosRoom

print("Wait for button press ...")

# Program start
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while continue_reading:
    input_state = GPIO.input(33)
    if input_state == False:
        print('Next Button Pressed')
        nfcData = 'next'
        SonosController.play(nfcData)

