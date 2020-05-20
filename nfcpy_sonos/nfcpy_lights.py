import time
from time import sleep
from datetime import datetime, timedelta

# # For BlinkStick
from blinkstick import blinkstick
# # End Added for Blinkstick

# # For JamHat
# # The import of JamHat had to be moved to mysonos.py
try:
    from gpiozero import JamHat
except:
    print("GPIOZero already loaded")
# # End Added for JamHat

# Added for GPIO LEDs
try:
    import RPi.GPIO as GPIO
except:
    print("RPi.GPIO already loaded")
# End Added for GPIO LEDs


def lightsDef(lightsonoff, lighttype, response):
    # Sending Lights Signal
    if lightsonoff != "off":
        print("lights on")
        # remove case sensitive
        lighttype = lighttype.casefold()
        response = response.casefold()

        if lighttype == "jamhat":
            print("Jamhat Lights Initiated")
            return lightsJamHat(response)
        if lighttype == "blinkstick":
            print("Blinkstick Lights Initiated")
            return lightsBlinkstick(response)
        if lighttype == "gpio":
            print("GPIO Lights Initiated")
            return lightsGPIO(response)
        #TODO - if jamhat and blinkstick
    elif lightsonoff == "off":
        print("playRoomLights says lights off")

# Positive Response

def lightsJamHat(response):
    # sonosUri = SONOS_BASE_URI + "/%s/nfc/%s" % (room, command)

    if response == "success":
        try:
            # # For Jam-HAT
            # Initialise the JamHat object.
            jh = JamHat()
            # # End JamHat
            #
            # i is the counter for the LED row.
            i = 2
            # j is the counter for the LED column.
            j = 2
            # Create counter
            x = 0

            # Setup a try/except block so we can run until CTRL+C is pressed.
            # try:
            for x in range(7):
            #while True:
                # Using modular arithmetic, decrease the light counter.
                # Our lights are in a matrix with rows 0-1 and columns 0-2.
                # Eg. [0][1] is the top yellow LED.
                if(j == 2):
                    # If we're at the end of the column, increment to the next row.
                    i = (i + 1) % 2
                # Increment the column.
                j = (j + 1) % 3
                sleep(0.2)
                # Turn the hat off.
                jh.off()
                # Turn on the LED at i j on the board.
                jh[i][j].on()
                # Turn the hat off.
                #jh.off()
                # Increment by 1
                x = x + 1
            jh.close()
        except:
            print("There was a JamHat Error in nfcpy_SonosController.lightsJamHat")
            try:
                lightsBlinkstick("error")
            except:
                print('Blinkstick had some sort of error in nfcpy_SonosController.lightsJamHat')

    elif response == "error":
        try:
            # # For Jam-HAT
            # Initialise the JamHat object.
            jh = JamHat()
            # # End JamHat
            #
            # Build an array of notes in hertz.
            NOTES = [440.000, 391.995, 349.228, 329.628, 293.665, 261.626]

            # Function to play beep for one second
            def play_buzzer():
                end_time = datetime.now() + timedelta(seconds=0.5)
                while datetime.now() < end_time:
                    jh.buzzer.play(NOTES[1])

            # Run function
            play_buzzer()
            # Close Jam-Hat
            jh.close()
            # # End Jam-HAT
        except:
            print("There was a JamHat error in nfcpy_SonosController")




        # except KeyboardInterrupt:
        #     # If someone presses CTRL+C, close the JamHat, freeing of the Pins for use elsewhere.
        #     jh.close()
        # # End Jam-HAT


def lightsBlinkstick(response):

    if response == "success":
        try:
            # For BlinkStick
            for bstick in blinkstick.find_all():
                bstick.set_color(name="green")
                bstick.pulse(name="blue")
                time.sleep(3)
                bstick.turn_off()
                continue
            # End BlinkStick
        except:
            print('Blinkstick had some sort of error')

    elif response == "error":
        try:
            # For BlinkStick
            for bstick in blinkstick.find_all():
                bstick.set_color(name="red")
                time.sleep(3)
                print("Blinkstick lights command successful")
                bstick.turn_off()
            # End BlinkStick
        except:
            print("blinkstick had some sort of error")



def lightsGPIO(response):

    if response == "success":
        try:
            # Turn On Pin 12 for x Seconds
            GPIO.setup(12, GPIO.OUT)
            GPIO.output(12, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(12, GPIO.LOW)
            # End Turn On Pin 12 for x Seconds
        except:
            print('GPIO LEDs had some sort of error')
    elif response == "error":
        try:
            # # Turn On Pin 31 for x Seconds
            GPIO.setup(31, GPIO.OUT)
            GPIO.output(31, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(31, GPIO.LOW)
            # # End Turn On Pin 31 for x Seconds
        except:
            print("GPIO LEDs had some sort of error")







