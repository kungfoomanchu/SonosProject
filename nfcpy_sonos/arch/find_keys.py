# Code and setup from https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html

#import evdev
from evdev import InputDevice, categorize, ecodes

#creates object 'gamepad' to store the data
#you can call it whatever you like
media_buttons = InputDevice('/dev/input/event1')

#prints out device info at start
print(media_buttons)

#evdev takes care of polling the controller in a loop
for event in media_buttons.read_loop():
#    print(categorize(event))
    #filters by event type
    if event.type == ecodes.EV_KEY:
        print(event)