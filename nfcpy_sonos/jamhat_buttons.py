# Import the necessary libraries.
# gpiozero contains our JamHat object.
from gpiozero import JamHat # pylint: disable=unresolved-import
from time import sleep
import nfcpy_SonosController

# Initialise the JamHat object.
jh = JamHat()



# Setup a try/except block so we can run until CTRL+C is pressed.
try:
    # Initialise counter
    counter = 0
    while True:
        if jh.button_1.is_pressed or jh.button_2.is_pressed:
            if jh.button_1.is_pressed:
                jh.button_1.wait_for_release()
                print('Next Button Pressed')
                nfcData = 'next'
                nfcpy_SonosController.play(nfcData)
            if jh.button_2.is_pressed:
                counter += 1
                jh.button_2.wait_for_release()
                if (counter % 2) == 0:
                    print('Play Button Pressed')
                    nfcData = 'play'
                    nfcpy_SonosController.play(nfcData)
                else:
                    print('Pause Button Pressed')
                    nfcData = 'pause'
                    nfcpy_SonosController.play(nfcData)
        sleep(0.1)
except KeyboardInterrupt:
    # If someone presses CTRL+C, close the JamHat, freeing of the Pins for use elsewhere.
    jh.close()
