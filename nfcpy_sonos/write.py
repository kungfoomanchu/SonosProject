import nfc
import ndef
from nfc.clf import RemoteTarget
from time import sleep

# Establish Reader on USB
clf = nfc.ContactlessFrontend('usb')

# try:
while True:
    # Establish the types of tags we are looking for
    target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
    print(target) 
    
    if target is None:
        sleep(2)  # don't burn the CPU
        continue

    # 
    tag = nfc.tag.activate(clf, target)
    print(tag)

    # How to write URI via NFCpy documentation https://nfcpy.readthedocs.io/en/latest/topics/get-started.html#read-and-write-tags
    # uri, title = 'spotify:album:65zhpgwMMRxncpa7zHckQ6','Sunday Service'
    # tag.ndef.records = [ndef.SmartposterRecord(uri, title)]

    # How to write URI via ndeflib documentation https://ndeflib.readthedocs.io/en/stable/records/uri.html
    tag_uri = 'spotify:album:65zhpgwMMRxncpa7zHckQ6'
    tag.ndef.records = [ndef.UriRecord(tag_uri)]

    # Finally the contactless frontend should be closed.
    clf.close()





# except:
#     print("An error occurred or there was no tag")

#     # # BlinkStick
#     # from blinkstick import blinkstick
#     # led = blinkstick.find_first():
#     # led.set_color(name="red")
#     # led.pulse(name="blue")

#     # Finally the contactless frontend should be closed.
#     clf.close()