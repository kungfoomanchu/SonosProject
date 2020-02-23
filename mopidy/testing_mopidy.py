from mpd import MPDClient

# For Blinkstick
from blinkstick import blinkstick
from time import sleep
#

# For NFCPy
import nfc
import ndef
from nfc.clf import RemoteTarget
#
import signal # For aborting the script?

client = MPDClient()               # create client object
client.timeout = 10                # network timeout in seconds (floats allowed), default: None
client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
client.connect("localhost", 6600)  # connect to localhost:6600
print(client.mpd_version)          # print the MPD version
# print(client.find("any", "house")) # print result of the command "find any house"
# client.close()                     # send the close command
# client.disconnect()                # disconnect from the server

# client.clear()
# # core.add(uri=uri)
# # client.add("test.mp3")
# client.add("spotify:track:1OQ7omBmuqUXNmrgcg7xiN")
# # # client.play()
# client.play()
# client.playlist()
# client.pause()

# Set up Variables
continue_reading = True
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
clf = nfc.ContactlessFrontend('usb')

while continue_reading:



    # Establish the types of tags we are looking for
    target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
    print(target) 

    # If we don't find a card, wait
    # TODO figure out how to make this not annoying
    if target is None:
        sleep(1)  # don't burn the CPU
        continue

    #
    tag = nfc.tag.activate(clf, target)
    print(tag)

    # This is the generally preferred way to discover and activate contactless targets of any supported type
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    print(tag)

    # Read NDEF Records
    if not tag.ndef:
        print("No NDEF records found!")
        # Finally the contactless frontend should be closed.
        clf.close()
    else:
        for record in tag.ndef.records:
            print(record) 
            record = tag.ndef.records[0]
            print(record.name)
            print(record.uri)
            client.clear()
            client.add(record.uri)
            client.play()
            # # Finally the contactless frontend should be closed.
            # clf.close()

            print(client.status())
            client_status = client.status()
            client_status = str(client_status)
            play_success = "'state': 'play'"
            if play_success in client_status:

                for bstick in blinkstick.find_all():
                    # For BlinkStick
                    led = blinkstick.find_first()
                    led.set_color(name="green")
                    led.pulse(name="blue")
                    time.sleep(3)
                    bstick.turn_off()
                    # End BlinkStick