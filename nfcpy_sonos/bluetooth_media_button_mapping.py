# Code and setup from https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html
# Make sure to install 'keyboard' with sudo because it has to run in sudo
# Find your bluetooth device by running this: python /usr/local/lib/python2.7/dist-packages/evdev/evtest.py

#import evdev
from evdev import InputDevice, categorize, ecodes
# Keyboard - https://github.com/boppreh/keyboard
import keyboard
import SonosController

# TODO Figure out how to not make the script break if satechi media buttons aren't powered on
# [Satechi Media Button]#  Device DC:2C:26:F1:C8:55

continue_reading = True

while continue_reading:
    #creates object 'media_buttons' to store the data
    #you can call it whatever you like
    media_buttons = InputDevice('/dev/input/event1')

    # Hold if media button is not powered on
    # TODO this failsafe to prevent script from running if buttons not powered on doesn't currently work
    if media_buttons is None:
        sleep(10)  # don't burn the CPU
        continue

    #prints out device info if bluetooth device is found
    print(media_buttons)

    #button code variables (change to suit your device)
    KEY_VOLUMEDOWN = 114
    KEY_VOLUMEUP = 115
    KEY_NEXTSONG = 163
    KEY_PREVIOUSSONG = 165
    KEY_PLAYPAUSE = 164

    # TODO figure out workaround for playpause not working
    # TODO Note that this currently controlls both media playing on the Pi and the Sonos
    #loop and filter by event code and print the mapped label
    for event in media_buttons.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.value == 1:
                if event.code == KEY_VOLUMEDOWN:
                    keyboard.press_and_release(114)
                    print("Volume Down")
                    SonosController.playPause("groupVolume/-10")
                    print("Successfully sent to Sonos")
                elif event.code == KEY_VOLUMEUP:
                    keyboard.press_and_release(115)
                    print("Volume Up")
                    SonosController.playPause("groupVolume/+10")
                    print("Successfully sent to Sonos")
                elif event.code == KEY_NEXTSONG:
                    keyboard.press_and_release(163)
                    print("Next Track")
                    SonosController.play("next")
                    print("Successfully sent to Sonos")
                elif event.code == KEY_PREVIOUSSONG:
                    keyboard.press_and_release(165)
                    print("Previous Track")
                    SonosController.play("previous")
                    print("Successfully sent to Sonos")
                elif event.code == KEY_PLAYPAUSE:
                    keyboard.press_and_release(164)
                    print("Pause")
                    SonosController.play("pause")
                    print("Successfully sent to Sonos")
