import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import textwrap
import sys
import NFCHelper

def write_card(uri_to_write,artist_to_write,album_to_write,year_to_write):
    continue_reading = True
    nfcData = "" 

    # Capture SIGINT for cleanup when the script is aborted
    #def end_read(signal,frame):
        #global continue_reading
        #print("Ctrl+C captured, ending read.")
        #continue_reading = False
        #GPIO.cleanup()
    # Hook the SIGINT
    #signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    if(not nfcData):
        nfcData = uri_to_write
    print("Artist: "+artist_to_write+"\n")
    print("Album: "+album_to_write+" ("+str(year_to_write)+")"+"\n")
    print ("URI that will be written: %s" % nfcData)

    print("Add NFC Tag ...")

    # Program start
    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:

        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print("Card detected")

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print("Card UID: %s:%s:%s:%s" % (uid[0], uid[1], uid[2], uid[3]))

                # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Write the data
            sectors = textwrap.wrap(nfcData, 16)
            sectorCount = NFCHelper.SECTOR_DATA_START
            print("Sector [%s-%s] need to be written with data." % (sectorCount, sectorCount + len(sectors) - 1))

            for sectorContent in sectors:
                NFCHelper.write_Sector(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT, sectorCount, sectorContent)
                NFCHelper.read_Sector(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT, sectorCount)
                sectorCount = sectorCount + 1
                if(sectorCount % 4 == 3):
                    sectorCount = sectorCount + 1

            # write Metadata
            expectedNfcDataSize = len(nfcData)


            NFCHelper.write_Metadata(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT, nfcData)
            nfcDataSize = NFCHelper.read_Metadata(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT)

            if(nfcDataSize != expectedNfcDataSize):
                print("Metadata wrong. Is %s should be %s" % (nfcDataSize, expectedNfcDataSize))

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()
            print("Card UID: %s:%s:%s:%s finished." % (uid[0], uid[1], uid[2], uid[3]))
            #time.sleep(3)
            GPIO.cleanup()
            continue_reading = False
