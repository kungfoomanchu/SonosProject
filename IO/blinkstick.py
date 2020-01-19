from blinkstick import blinkstick

for bstick in blinkstick.find_all():
    bstick.set_random_color()