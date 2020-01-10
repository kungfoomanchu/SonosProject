#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sonos-nfc-read.  If not, see <http://www.gnu.org/licenses/>.
#


from datetime import datetime, timedelta
import argparse
import math
import signal # For aborting the script?
import SonosController
# For NFCPy
import nfc
import ndef
from nfc.clf import RemoteTarget
#


# Set up Variables
continue_reading = True
is_test = False
DEFAULT_DEBOUNCE = 10
DEFAULT_CARD_TIMEOUT = 0
#

## Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    # Finally the contactless frontend should be closed.
    clf.close()
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
#

# Establish Reader on USB
# See list of compatible readers at nfcpy.org
clf = nfc.ContactlessFrontend('usb')

# Setup Parser
parser = argparse.ArgumentParser(description='Write NFC tags for sonos.')
parser.add_argument('-test', type=bool, default=False, help='Just test the read but dont perform the action on sonos')
parser.add_argument('-sonosUri', type=str, default=SonosController.SONOS_BASE_URI, help='The Sonos base Uri to use')
parser.add_argument('-sonosRoom', type=str, default=SonosController.SONOS_ROOM, help='The Sonos room to play the content at')
parser.add_argument('-debounce', type=int, default=DEFAULT_DEBOUNCE, help='The amount of time to wait after a scan to read again')
parser.add_argument('-cardTimeout', type=int, default=DEFAULT_DEBOUNCE, help='The amount of time to wait before re-reading the same card')
#parser.add_argument('-nfcKey', type=str, default='FF:FF:FF:FF:FF:FF', help='The hex code of the nfc key to writ the content default: FF:FF:FF:FF:FF:FF')
args = parser.parse_args()
#

# Import variaables from args
is_test = args.test
SonosController.SONOS_BASE_URI = args.sonosUri
SonosController.SONOS_ROOM = args.sonosRoom
#

# Debounce and cardTimeout settings
last_nfc_uri = ""
last_time = datetime.now() - timedelta(seconds = 60)
debounce = timedelta(seconds = args.debounce)
card_timeout = timedelta(seconds = args.cardTimeout)
#



print("Add NFC Tag ...")

# Program start
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    now = datetime.now()

    # Debounce card reader
    if last_time + debounce > now:
        continue
    
    # Establish the types of tags we are looking for
    target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
    print(target) 
    #

    # Get tag info
    tag = nfc.tag.activate(clf, target)
    print(tag)
    #

    # This is the generally preferred way to discover and activate contactless targets of any supported type
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    print(tag)  

    # Read NDEF Records
    if not tag.ndef:
        print("No NDEF records found!")
        # Finally the contactless frontend should be closed.
        clf.close()
    else:
        print(ndef.UriRecord)
        # print(tag.ndef.records.uri)
        for record in tag.ndef.records:
            print(record) 
            record = tag.ndef.records[0]
            print(record.name)
            print(record.uri)
            nfc_uri = record.uri
        # 

        # If the nfc data is the same as previous, then ignore while we are in the timeout
        # Otherwise send the command.
        # TODO: filter out play,pause,next,previous etc from the timeout
        if last_nfc_uri == nfc_uri and last_time + card_timeout > now:
            print("Re-reading the same card too soon, ignoring")
        else:
            last_nfc_uri = nfc_uri
            last_time = now

            # send command to server
            if(not is_test):
                SonosController.play(nfc_uri)

