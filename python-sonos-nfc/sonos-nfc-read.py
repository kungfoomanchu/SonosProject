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
from time import sleep
import math
import SonosController
import NFCHelper
import argparse
from datetime import datetime, timedelta
import pause

continue_reading = True
is_test = False

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Setup Parser
parser = argparse.ArgumentParser(description='Read NFC tags for Sonos.')
parser.add_argument('-test', type=bool, default=False, help='Just test the read but dont perform the action on sonos')
parser.add_argument('-sonosUri', type=str, default=SonosController.SONOS_BASE_URI, help='The Sonos base Uri to use')
parser.add_argument('-sonosRoom', type=str, default=SonosController.SONOS_ROOM, help='The Sonos room to play the content at')
parser.add_argument('-debounce', type=int, default=3, help='The amount of time to wait after a scan to read again')
parser.add_argument('-cardTimeout', type=int, default=0, help='The amount of time to wait before re-reading the same card')
parser.add_argument('-quietTime', type=str, default="no", help='Type "yes" to enable quiet time from 9 PM to 7 AM')
args = parser.parse_args()

# Import variables from args
is_test = args.test
SonosController.SONOS_BASE_URI = args.sonosUri
SonosController.SONOS_ROOM = args.sonosRoom
quietT = args.quietTime

# Debounce and cardTimeout settings
last_nfc_data = ""
last_time = datetime.now() - timedelta(seconds=60)
debounce = timedelta(seconds=args.debounce)
card_timeout = timedelta(seconds=args.cardTimeout)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

print("Add NFC Tag ...")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Debounce card reader
    now = datetime.now()
    if last_time + debounce > now:
        sleep(0.1)
        continue

    # Start Quiet Time
    if quietT == 'yes':
        nowtime = datetime.now()
        if not (nowtime.hour >= 21 or nowtime.hour < 7):
            pass
        else:
            print("It's Quiet Time. We'll check again in a minute")
            time.sleep(60)
            # This will pause until 7 AM
            pause.until(datetime(nowtime.year, nowtime.month, nowtime.day, 7, 0, 0))
            continue

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print("Card detected - UID: %s:%s:%s:%s" % (uid[0], uid[1], uid[2], uid[3]))

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            dataSize = NFCHelper.read_Metadata(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT)

            # Startsector
            sectorCount = NFCHelper.SECTOR_DATA_START
            # number of sectors
            numberOfSectorsToRead = math.ceil(dataSize / 16)

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

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()

            # CardTimeout Code
            # If the nfc data is the same as previous, then ignore while we are in the timeout
            # Otherwise send the command.
            if last_nfc_data == nfcData and last_time + card_timeout > now:
                print("Re-reading the same card too soon, ignoring")
            else:
                last_nfc_data = nfcData
                last_time = now

                print("NFC Data: '%s'" % nfcData)
                #send command to server
                if(not is_test):
                    SonosController.play(nfcData)

            # Wait for card to be removed
            time.sleep(1)