#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Gerd Saurer <gerd.saurer@gmail.com>
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sonos-nfc-read.  If not, see <http://www.gnu.org/licenses/>.
#

import signal
import time
import textwrap
import sys
import argparse
# For NFCPy
import nfc
import ndef
from nfc.clf import RemoteTarget

continue_reading = True
is_test = False
nfcData_to_write = "" 

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    # Finally the contactless frontend should be closed.
    clf.close()
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Establish Reader on USB
# See list of compatible readers at nfcpy.org
clf = nfc.ContactlessFrontend('usb')

# Establish the types of tags we are looking for
target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
print(target) 

# Set Up Args
parser = argparse.ArgumentParser(description='Write NFC tags for sonos.')
parser.add_argument('-test', type=bool, default=False, help='Just test the writing but dont perform the action on the card')
parser.add_argument('-uri', type=str, default='', help='The content that should be written')
args = parser.parse_args()

# Import variaables from args
is_test = args.test
nfcData_to_write= args.uri

# if(not nfcData_to_write):
#     nfcData_to_write = input("Enter URI to write: ")
nfcData_to_write = "spotify:album:65zhpgwMMRxncpa7zHckQ6"

# TODO add notification for URI to be written

print("Add NFC Tag ...")

# TODO - add a checker to see if card is present

if(not is_test):
    # Establish tag
    tag = nfc.tag.activate(clf, target)
    print(tag)

    # Copy URI to the Tag
    # How to write URI via ndeflib documentation https://ndeflib.readthedocs.io/en/stable/records/uri.html
    tag.ndef.records = [ndef.UriRecord(nfcData_to_write)]
    print("URI Successfully Written")
    # Finally the contactless frontend should be closed.
    clf.close()