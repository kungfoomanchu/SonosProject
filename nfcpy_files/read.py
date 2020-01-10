import nfc
import ndef
from nfc.clf import RemoteTarget

# Establish Reader on USB
clf = nfc.ContactlessFrontend('usb')

# Establish the types of tags we are looking for
target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
print(target) 

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
        # Finally the contactless frontend should be closed.
        clf.close()

# try:
    # Get Serial Number (this maybe doesn't work?)
    # serial = target.sdd_res.hex()
    # print(serial)
# except:
#     print("An error occurred or there was no tag")
#     # Finally the contactless frontend should be closed.
#     clf.close()











# from time import sleep
# import nfc

# with nfc.ContactlessFrontend('usb') as clf:
#     while True:
#         target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
        
#         if target is None:
#             sleep(0.1)  # don't burn the CPU
#             continue

#         serial = target.sdd_res.hex()
#         tag = nfc.tag.activate(clf, target)
#         if not tag.ndef:
#             print("No NDEF records found!")
#             continue
        
#         for record in tag.ndef.records:
#             print("Found record: " + record)   