#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Gerd Saurer <gerd.saurer@gmail.com>
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sonos-nfc-read.  If not, see <http://www.gnu.org/licenses/>.
#

from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import MFRC522
import argparse
import math
import NFCHelper
import signal
import SonosController
# time added for LEDs
import time

## _________LED Setup____________
# Set GPIO to Broadcom chip used in Raspberry Pi
GPIO.setmode(GPIO.BOARD)
## _________End LED Setup____________

continue_reading = True
is_test = False

## Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

DEFAULT_DEBOUNCE = 10
DEFAULT_CARD_TIMEOUT = 0

parser = argparse.ArgumentParser(description='Write NFC tags for sonos.')
parser.add_argument('-test', type=bool, default=False, help='Just test the read but dont perform the action on sonos')
parser.add_argument('-sonosUri', type=str, default=SonosController.SONOS_BASE_URI, help='The Sonos base Uri to use')
parser.add_argument('-sonosRoom', type=str, default=SonosController.SONOS_ROOM, help='The Sonos room to play the content at')
parser.add_argument('-debounce', type=int, default=DEFAULT_DEBOUNCE, help='The amount of time to wait after a scan to read again')
parser.add_argument('-cardTimeout', type=int, default=DEFAULT_DEBOUNCE, help='The amount of time to wait before re-reading the same card')
#parser.add_argument('-nfcKey', type=str, default='FF:FF:FF:FF:FF:FF', help='The hex code of the nfc key to writ the content default: FF:FF:FF:FF:FF:FF')
args = parser.parse_args()

is_test = args.test
SonosController.SONOS_BASE_URI = args.sonosUri
SonosController.SONOS_ROOM = args.sonosRoom

last_nfc_uri = ""
last_time = datetime.now() - timedelta(seconds = 60)
debounce = timedelta(seconds = args.debounce)
card_timeout = timedelta(seconds = args.cardTimeout)

MIFAREReader = MFRC522.MFRC522()

## _________LED Test____________
# Turn On IO 29 for x Seconds
GPIO.setup(29, GPIO.OUT)
GPIO.output(29, GPIO.HIGH)
time.sleep(1)
GPIO.output(29, GPIO.LOW)
# End Turn On Pin 29 for x Seconds
## _________End LED Test____________

print("Add NFC Tag ...")

# Program start
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    now = datetime.now()

    # Debounce card reader
    if last_time + debounce > now:
        continue

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        # Turn On IO 12 for x Seconds
        # GPIO.setup(12, GPIO.OUT)
        # GPIO.output(12, GPIO.HIGH)
        # time.sleep(2)
        # GPIO.output(12, GPIO.LOW)
        # End Turn On IO 12 for x Seconds
        print("Card detected")


    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print("Card UID: %s:%s:%s:%s" % (uid[0], uid[1], uid[2], uid[3]))

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        dataSize = NFCHelper.read_Metadata(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT)

        #Startsector
        sectorCount = NFCHelper.SECTOR_DATA_START
        #number of sectors
        numberOfSectorsToRead = math.ceil(dataSize / 16)

        print("Sector [%s-%s] need to be read." % (sectorCount, sectorCount + numberOfSectorsToRead))

        # read the data
        nfcData = ""
        numberOfSectorsReadCount = 0
        while numberOfSectorsReadCount < numberOfSectorsToRead and continue_reading:
            nfcData = nfcData + NFCHelper.read_Sector(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT, sectorCount)
            sectorCount = sectorCount + 1
            if(sectorCount % 4 == 3):
                sectorCount = sectorCount + 1
            numberOfSectorsReadCount = numberOfSectorsReadCount + 1

        nfcData = nfcData[:dataSize]

        print("NFC Data: '%s'" % nfcData)

        # Done reading from card reader
        MIFAREReader.MFRC522_StopCrypto1()

        # If the nfc data is the same as previous, then ignore while we are in the timeout
        # Otherwise send the command.
        # TODO: filter out play,pause,next,previous etc from the timeout
        if last_nfc_uri == nfcData and last_time + card_timeout > now:
            print("Re-reading the same card too soon, ignoring")
        else:
            last_nfc_uri = nfcData
            last_time = now

            # send command to server
            if(not is_test):
                SonosController.play(nfcData)