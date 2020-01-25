# Import the necessary libraries.
# gpiozero contains our JamHat object.
from gpiozero import JamHat
from time import sleep
from datetime import datetime, timedelta

# Initialise the JamHat object.
jh = JamHat()

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