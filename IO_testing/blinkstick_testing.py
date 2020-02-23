from blinkstick import blinkstick
import time
from time import sleep

# for bstick in blinkstick.find_all():
#     bstick.set_random_color()

# For BlinkStick
for bstick in blinkstick.find_all():
    bstick.set_color(name="green")
    bstick.pulse(name="blue")
    time.sleep(3)
    bstick.turn_off()
# End BlinkStick