#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# This script uses the nfcpy library to read and write NFC tags for use with a Sonos system.
# It can be run in three modes:
# 1. Read mode (default): Listens for NFC tags and plays the URI on a Sonos speaker.
# 2. Write mode: Writes a single URI to an NFC tag.
# 3. Loop write mode: Reads data from a Google Sheet and writes it to multiple NFC tags.
#

from datetime import datetime, timedelta
import argparse
import math
import signal
import nfcpy_SonosController
import time
from time import sleep
import nfc
import ndef
from nfc.clf import RemoteTarget
import pause
import configparser

# --- Global Variables ---
continue_reading = True
is_test = False
nfcData_to_write = ""
forcedresponse = ""

# --- Configuration ---
# Load settings from settings.ini
config = configparser.ConfigParser()
config.read('settings.ini')
DEFAULT_DEBOUNCE = config.get('MySonos', 'debounce', fallback='10')
DEFAULT_CARD_TIMEOUT = config.get('MySonos', 'cardTimeout', fallback='0')
DEFAULT_QUIETTIME = config.get('MySonos', 'quietTime', fallback='No')
DEFAULT_LIGHTSONOFF = config.get('MySonos', 'lightsonoff', fallback='off')
DEFAULT_LIGHTTYPE = config.get('MySonos', 'lighttype', fallback='jamhat')

# --- Signal Handler ---
# Gracefully exit on Ctrl+C
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    if 'clf' in globals():
        clf.close()

signal.signal(signal.SIGINT, end_read)

# --- Argument Parser ---
# Setup command-line arguments
parser = argparse.ArgumentParser(description='Read or write NFC tags for Sonos.')
parser.add_argument('-test', type=bool, default=False, help='Run in test mode (no actions performed on Sonos).')
parser.add_argument('-sonosUri', type=str, default=nfcpy_SonosController.SONOS_BASE_URI, help='The Sonos base URI to use.')
parser.add_argument('-sonosRoom', type=str, default=nfcpy_SonosController.SONOS_ROOM, help='The Sonos room to control.')
parser.add_argument('-debounce', type=int, default=DEFAULT_DEBOUNCE, help='Seconds to wait after a scan before reading again.')
parser.add_argument('-cardTimeout', type=int, default=DEFAULT_DEBOUNCE, help='Seconds to wait before re-reading the same card.')
parser.add_argument('-quietTime', type=str, default=DEFAULT_QUIETTIME, help='Enable quiet time from 9 PM to 7 AM ("yes" or "no").')
parser.add_argument('-lightsOnOff', type=str, default=DEFAULT_LIGHTSONOFF, help='Enable lights ("on" or "off").')
parser.add_argument('-lightType', type=str, default=DEFAULT_LIGHTTYPE, help='Type of lights: "jamhat", "blinkstick", or "GPIO".')
parser.add_argument('-write', type=str, default='no', help='Write mode: "yes" for single card, "loop" for multiple from Google Sheet.')
parser.add_argument('-uri', type=str, default='', help='The URI to write to the tag.')
args = parser.parse_args()

# --- Main Variables ---
# Assign arguments to variables
is_test = args.test
we_write = args.write
nfcData_to_write = args.uri
nfcpy_SonosController.SONOS_BASE_URI = args.sonosUri
nfcpy_SonosController.SONOS_ROOM = args.sonosRoom
quietT = args.quietTime
lightsOnOff = args.lightsOnOff
lightType = args.lightType

# Debounce and card timeout settings
last_nfc_uri = ""
last_time = datetime.now() - timedelta(seconds=60)
debounce = timedelta(seconds=args.debounce)
card_timeout = timedelta(seconds=args.cardTimeout)


# ======================================================================
#     READ MODE
# ======================================================================
if we_write == "no":
    print("Starting in READ mode...")
    # Initialize the NFC reader
    try:
        clf = nfc.ContactlessFrontend('usb')
    except IOError:
        print("Could not connect to NFC reader. Please check the connection.")
        exit()

    print("Waiting for NFC tag...")

    while continue_reading:
        # --- Debounce ---
        # Wait a few seconds before trying to read another card
        now = datetime.now()
        if last_time + debounce > now:
            sleep(0.1)
            continue

        # --- Quiet Time ---
        # Don't play music during quiet hours
        if quietT.lower() == 'yes':
            nowtime = datetime.now()
            if not (nowtime.hour >= 21 or nowtime.hour < 7):
                pass
            else:
                print("It's Quiet Time. We'll check again in a minute.")
                time.sleep(60)
                # This will pause until 7 AM
                pause.until(datetime(nowtime.year, nowtime.month, nowtime.day, 7, 0, 0))
                continue

        # --- Read Card ---
        # Look for a card
        target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))

        if target is None:
            sleep(0.5)  # Don't burn the CPU
            continue

        # Connect to the card
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print(f"Card detected: {tag}")

        if not tag.ndef:
            print("No NDEF records found on this card.")
            sleep(5)
            continue

        # --- Process URI ---
        # Extract the URI from the NDEF record
        nfc_uri = tag.ndef.records[0].uri
        print(f"Read URI: {nfc_uri}")

        # If the URI is a command (contains a colon), process it
        if ":" in nfc_uri:
            # --- Card Timeout ---
            # If it's the same card, wait for the timeout
            if last_nfc_uri == nfc_uri and last_time + card_timeout > now:
                print("Same card read again too soon. Ignoring.")
            else:
                last_nfc_uri = nfc_uri
                last_time = now

                # Send the command to Sonos
                if not is_test:
                    print(f"Sending command to Sonos: {nfc_uri}")
                    nfcpy_SonosController.playRoomLights(nfc_uri, lightsOnOff, lightType, forcedresponse)
                else:
                    print("TEST MODE: Command not sent.")
        else:
            # If the URI is not a command, treat it as a play/pause toggle
            print("No ':' in URI, treating as play/pause.")
            if not is_test:
                nfcpy_SonosController.playPause(nfcpy_SonosController.SONOS_ROOM, nfc_uri)
            else:
                print("TEST MODE: Command not sent.")


# ======================================================================
#     LOOP WRITE MODE
# ======================================================================
elif we_write == "loop":
    print("Starting in LOOP WRITE mode...")
    # Initialize the NFC reader
    try:
        clf = nfc.ContactlessFrontend('usb')
    except IOError:
        print("Could not connect to NFC reader. Please check the connection.")
        exit()

    # Import libraries for Google Sheets
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
    except ImportError:
        print("gspread or oauth2client is not installed. Please run: pip install gspread oauth2client")
        exit()

    # Authenticate with Google Sheets
    try:
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open("NFC Cards Database").sheet1
        list_of_sheet_records = sheet.get_all_records()
    except Exception as e:
        print(f"Could not connect to Google Sheets: {e}")
        exit()

    # Function to write a single card
    def write_card(uri_to_write, artist_to_write, album_to_write, year_to_write):
        print("\n---")
        print(f"Artist: {artist_to_write}")
        print(f"Album: {album_to_write} ({year_to_write})")
        print(f"URI to write: {uri_to_write}")

        input("Place a new tag on the reader and press Enter...")

        while True:
            target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
            if target:
                tag = nfc.tag.activate(clf, target)
                print(f"Writing to tag: {tag}")
                if not is_test:
                    tag.ndef.records = [ndef.UriRecord(uri_to_write)]
                    print("Successfully wrote to tag.")
                else:
                    print("TEST MODE: Tag not written.")
                break
            else:
                print("No tag detected. Please place a tag on the reader.")
                sleep(1)

    # Loop through the records from the Google Sheet
    for record in list_of_sheet_records:
        uri_to_write = record.get('Spotify URI (Result)', '')
        artist_to_write = record.get('Artist (Result)', '')
        album_to_write = record.get('Album (Result)', '')
        year_to_write = record.get('Year (Result)', '')
        skip_or_print = record.get('Skip vs Print', '')

        if uri_to_write and uri_to_write != 'No Match' and skip_or_print != 'Skip':
            write_card(uri_to_write, artist_to_write, album_to_write, year_to_write)


# ======================================================================
#     SINGLE WRITE MODE
# ======================================================================
else:
    print("Starting in SINGLE WRITE mode...")
    # Initialize the NFC reader
    try:
        clf = nfc.ContactlessFrontend('usb')
    except IOError:
        print("Could not connect to NFC reader. Please check the connection.")
        exit()

    if not nfcData_to_write:
        nfcData_to_write = input("Enter URI to write: ")

    print(f"URI to be written: {nfcData_to_write}")
    if is_test:
        print("RUNNING IN TEST MODE - NO DATA WILL BE WRITTEN")

    input("Place the card on the reader and press Enter to continue...")

    while continue_reading:
        target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))

        if target is None:
            print("No card detected. Please place a card on the reader.")
            sleep(1)
            continue

        tag = nfc.tag.activate(clf, target)
        print(f"Card detected: {tag}")

        if not is_test:
            tag.ndef.records = [ndef.UriRecord(nfcData_to_write)]
            print("Successfully wrote URI to card.")
        else:
            print("TEST MODE: Card not written.")

        continue_reading = False
