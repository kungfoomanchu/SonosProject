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
import textwrap
import sys
import NFCHelper
import argparse

is_test = False

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    print("Ctrl+C captured, ending read.")
    GPIO.cleanup()
    sys.exit()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Setup Parser
parser = argparse.ArgumentParser(description='Write a URI to a NFC tag for Sonos.')
parser.add_argument('-uri', type=str, required=True, help='The URI to write to the tag.')
parser.add_argument('-test', type=bool, default=False, help='Run in test mode without writing to the card.')
args = parser.parse_args()

# Get arguments
nfcData = args.uri
is_test = args.test

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

print(f"URI to be written: {nfcData}")
if is_test:
    print("RUNNING IN TEST MODE - NO DATA WILL BE WRITTEN")

input("Place the card on the reader and press Enter to continue...")

# This loop keeps checking for chips.
while True:
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected.")
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            print("Card UID: %s:%s:%s:%s" % (uid[0], uid[1], uid[2], uid[3]))

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Write the data
            sectors = textwrap.wrap(nfcData, 16)
            sectorCount = NFCHelper.SECTOR_DATA_START
            print("Writing data to sectors %s-%s..." % (sectorCount, sectorCount + len(sectors) - 1))

            for sectorContent in sectors:
                if not is_test:
                    NFCHelper.write_Sector(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT, sectorCount, sectorContent)
                # We read the sector back to verify the write
                NFCHelper.read_Sector(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT, sectorCount)
                sectorCount = sectorCount + 1
                if(sectorCount % 4 == 3):
                    sectorCount = sectorCount + 1

            # Write Metadata
            expectedNfcDataSize = len(nfcData)
            print("Writing metadata...")
            if not is_test:
                NFCHelper.write_Metadata(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT, nfcData)
            nfcDataSize = NFCHelper.read_Metadata(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT)

            if(nfcDataSize != expectedNfcDataSize):
                print("Error: Metadata size mismatch. Expected %s, but got %s" % (expectedNfcDataSize, nfcDataSize))
            else:
                print("Successfully wrote URI to card.")

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()
            GPIO.cleanup()
            sys.exit()

    print("No card detected. Please place a card on the reader.")
    time.sleep(1)
