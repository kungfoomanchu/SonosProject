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
import nfcpy_SonosController
from time import sleep
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
nfcData_to_write = ""
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


# Setup Parser
parser = argparse.ArgumentParser(description='Write NFC tags for sonos.')
parser.add_argument('-test', type=bool, default=False, help='Just test the read but dont perform the action on sonos')
parser.add_argument('-sonosUri', type=str, default=nfcpy_SonosController.SONOS_BASE_URI, help='The Sonos base Uri to use')
parser.add_argument('-sonosRoom', type=str, default=nfcpy_SonosController.SONOS_ROOM, help='The Sonos room to play the content at')
parser.add_argument('-debounce', type=int, default=DEFAULT_DEBOUNCE, help='The amount of time to wait after a scan to read again')
parser.add_argument('-cardTimeout', type=int, default=DEFAULT_DEBOUNCE, help='The amount of time to wait before re-reading the same card')
#parser.add_argument('-nfcKey', type=str, default='FF:FF:FF:FF:FF:FF', help='The hex code of the nfc key to writ the content default: FF:FF:FF:FF:FF:FF')
parser.add_argument('-write', type=str, default='no', help='Type yes if you want to write individual cards, "loop" if you want to write multiple cards from google spreasheet')
parser.add_argument('-uri', type=str, default='', help='The content that should be written')
# TODO - Add Quiet Time
args = parser.parse_args()
#

# Import variaables from args
is_test = args.test
we_write = args.write
nfcData_to_write = args.uri
nfcpy_SonosController.SONOS_BASE_URI = args.sonosUri
nfcpy_SonosController.SONOS_ROOM = args.sonosRoom
#

# Debounce and cardTimeout settings
last_nfc_uri = ""
last_time = datetime.now() - timedelta(seconds = 60)
debounce = timedelta(seconds = args.debounce)
card_timeout = timedelta(seconds = args.cardTimeout)
#

# If/else for reading, writing, writing in loop
if we_write == "no":

    # Establish Reader on USB
    # See list of compatible readers at nfcpy.org
    clf = nfc.ContactlessFrontend('usb')
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

        # If we don't find a card, wait
        # TODO figure out how to make this not annoying
        if target is None:
            sleep(1)  # don't burn the CPU
            continue

        # Get tag info
        # tag = nfc.tag.activate(clf, target)
        # print(tag)
        #

        # This is the generally preferred way to discover and activate contactless targets of any supported type
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print(tag)
        #

        # Read NDEF Records
        if not tag.ndef:
            print("No NDEF records found!")
            print("You have 60 seconds to remove card")
            sleep(60)
        else:
            print(ndef.UriRecord)
            # print(tag.ndef.records.uri)
            for record in tag.ndef.records:
                print(f'NFC Record {record}')
                record = tag.ndef.records[0]
                print(f'NFC Record Name {record.name}')
                print(f'NFC URI {record.uri}')
                nfc_uri = record.uri
            #

            # Skip CardTimeout if URI does not contain ":"
            if ":" in nfc_uri:
                # CardTimeout Code
                # If the nfc data is the same as previous, then ignore while we are in the timeout
                # Otherwise send the command.
                if last_nfc_uri == nfc_uri and last_time + card_timeout > now:
                    print("Re-reading the same card too soon, ignoring")
                else:
                    last_nfc_uri = nfc_uri
                    last_time = now

                    # send command to server
                    if(not is_test):
                        nfcpy_SonosController.play(nfc_uri)
                    #
            else:
                # TODO: Prevent endless loop
                # TODO: there was a break here when adding a new card too soon?
                # send command to server
                print("Skipped Card Timeout")
                if(not is_test):
                    nfcpy_SonosController.play(nfc_uri)
                #

elif we_write == "loop":
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    # Establish Reader on USB
    # See list of compatible readers at nfcpy.org
    clf = nfc.ContactlessFrontend('usb')
    #

    # Establish the types of tags we are looking for
    target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
    print(target)

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the righto name here.
    sheet = client.open("Media Database Project Example (For John)").sheet1

    list_of_sheet_records = sheet.get_all_records()
    #print(list_of_sheet_records)

    # Add write_card def
    def write_card(uri_to_write,artist_to_write,album_to_write,year_to_write):

        # Pass variables from def input through
        nfcData_to_write = uri_to_write
        print("Artist: "+artist_to_write+"\n")
        print("Album: "+album_to_write+" ("+str(year_to_write)+")"+"\n")
        print ("URI that will be written: %s" % nfcData_to_write)

        input("Add NFC tag, then press Enter to continue...")

        if(not is_test):
            # Establish tag
            tag = nfc.tag.activate(clf, target)
            print(tag)
            #

            # Copy URI to the Tag
            # How to write URI via ndeflib documentation https://ndeflib.readthedocs.io/en/stable/records/uri.html
            tag.ndef.records = [ndef.UriRecord(nfcData_to_write)]
            print("URI Successfully Written")
            #

# TODO Ctrl+C didn't work as expected

    # Loop to extract info from Google Sheet and then send to 'write card'
    for record in list_of_sheet_records:
        # Assign Google Sheet data to variable
        uri_to_write=record['Spotify URI (Result)']
        artist_to_write=record['Artist (Result)']
        album_to_write=record['Album (Result)']
        year_to_write=record['Year (Result)']
        skip_or_print=record['Skip vs Print']

        # Skip certain records and send info to def
        if uri_to_write!='No Match':
            if skip_or_print!='Skip':
                write_card(uri_to_write,artist_to_write,album_to_write,year_to_write)

else:
    # Establish Reader on USB
    # See list of compatible readers at nfcpy.org
    clf = nfc.ContactlessFrontend('usb')
    #

    # Establish the types of tags we are looking for
    target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
    print(target)

    # If we don't find a card, wait
    # if target is None:
    #     sleep(1)  # don't burn the CPU
    #     continue

    if target is None:
        print("Place card on reader and re-run script")
    else:

        # TODO - this happens twice
        if(not nfcData_to_write):
            nfcData_to_write = input("Enter URI to write: ")
        # nfcData_to_write = "pause"

        #
        print(f'The URI which will be written is: {nfcData_to_write}')
        input("Add NFC tag, then press Enter to continue...")

        if(not is_test):
            # Establish tag
            tag = nfc.tag.activate(clf, target)
            print(tag)
            #

            # Copy URI to the Tag
            # How to write URI via ndeflib documentation https://ndeflib.readthedocs.io/en/stable/records/uri.html
            tag.ndef.records = [ndef.UriRecord(nfcData_to_write)]
            print("URI Successfully Written")
            #

            # Finally the contactless frontend should be closed.
            clf.close()
            #
