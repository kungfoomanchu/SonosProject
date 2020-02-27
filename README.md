# Raspberry Pi + NFC + Sonos + Mopidy Project
## What it does
** Add this**
This library can be leveraged in combination with [node-sonos-http-api](https://github.com/gsaurer/node-sonos-http-api) to controll the sonos service over RFID cards. This allows you to build a very flexible service for you children or to digitalize your libary by still looking at CD's.

Attributions
* gsaurer

Supported Services
* Local Sonos playlist
* Spotify
* Apple Music
* Amazon Music
* Tunein
## There is much to install for this project, so please follow these instructions carefully
First step is obviously to install this git repository. Do that by running this command from the directory where you want to place the repository
```git clone https://github.com/kungfoomanchu/SonosProject.git```
## Preparing Other Required Git Repositories
### Node
Install Node
* The following is a summary of more detailed instructions  [here](https://www.instructables.com/id/Install-Nodejs-and-Npm-on-Raspberry-Pi/)
*   Detect the version of node that you need by running the following command:
``uname -m``
*   If the response starts with armv6 than that's the version that you will need. For example,  you will need ARMv6 for the raspberry pi zero W. 
    * For ARMv6, please use this link: [https://nodejs.org/download/release/v11.13.0/node-v11.13.0-linux-armv6l.tar.gz](https://nodejs.org/download/release/v11.13.0/node-v11.13.0-linux-armv6l.tar.gz)
    * For other versions, find the download link here: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)
* Navigate to the directory where you want to download Node and do the following: Type wget, paste the link copied before and make sure the extension is .tar.gz. If it's something else change it to this and it should be ok. For example I will need ARMv6 and I will type this in my terminal:
``wget https://[GET LINK].tar.gz``
-   Extract the Archive
``tar -xzf node-v[THE VERSION NUMBER].tar.gz``
-   Copy Node to /usr/local
``cd [TO FOLDER]  ``
``sudo cp -R * /usr/local/``
-   Check If Everything Is Installed Ok
``node -v `` 
``npm -v``


Clone the node-sonos-http-api Repository:
* This repository is included in **SonosProject**, however you can also get the most up to date version by cloning the original repository here: 
```git clone https://github.com/jishi/node-sonos-http-api.git```
You will have to add ``nfc.py`` to the **FOLDER** however

Install it:
* Start by fixing your dependencies. Invoke the following command from the `node-sonos-http-api` folder:
`npm install --production`
This will download the necessary dependencies if possible.
* start the server by running
`npm start`
* Further information about usage is located here: [https://github.com/jishi/node-sonos-http-api](https://github.com/jishi/node-sonos-http-api)

### SPI-Py
Clone the repository:
``` git clone https://github.com/lthiery/SPI-Py.git```
Install it: 
1.  Clone or download this repository, navigate to the SPI-Py directory, and install the library using the following command. (Must be installed in Python 3).

```sudo python3 setup.py install```

2.  Make sure the SPI interface is enabled for your Raspberry Pi. This can be done using the raspi-config utility.

```sudo raspi-config```

## Installations for Various Lights and Python Packages
Blinkstick
* These are slightly modified instructions from this page: [https://www.blinkstick.com/help/raspberry-pi-integration](https://www.blinkstick.com/help/raspberry-pi-integration)
* First you will need to install required packages. Pip lets you manage Python packages easier and Python development headers are required to install the websocket-client package:
``sudo apt-get install -y python-pip``
* Install Python BlinkStick package (make sure to install it with ``sudo``:
``sudo pip3 install blinkstick``
* Run the control script check if Raspberry Pi has detected BlinkStick correctly:
``sudo blinkstick --info``
* You can find details about more examples in the  [readme](https://github.com/arvydas/blinkstick-python/blob/master/README.md).
* If you don't want to sudo each time you want to access BlinkStick, then run the following command (this may not work properly for Python 3):
``echo "SUBSYSTEM==\"usb\", ATTR{idVendor}==\"20a0\", ATTR{idProduct}==\"41e5\", MODE:=\"0666\" | sudo tee /etc/udev/rules.d/85-blinkstick.rules"``
* More resources for BlinkStick
     * [https://github.com/arvydas/blinkstick-python/wiki/Command-line-tool-options](https://github.com/arvydas/blinkstick-python/wiki/Command-line-tool-options)
    - [https://github.com/arvydas/blinkstick-python](https://github.com/arvydas/blinkstick-python) 

JamHat
* **What to install**
* https://github.com/modmypi/Jam-HAT

MFRC522
* MFRC522.py from the [repository](https://github.com/mxgxw/MFRC522-python) is included in this project and changed to support python v3

Python Packages
- Install both of these:
     - ``sudo pip3 install gspread`` 
     - ``sudo pip3 install oauth2client`` 

# Installations for USB NFC Reader

-   Install NFCPy
``sudo pip3 install -U nfcpy``
-   Verify
``python3 -m nfc``

-   You will most likely see an error message like this first:
``I'm now searching your system for contactless devices  
** found usb:04e6:5591 at usb:002:025 but access is denied  
-- the device is owned by 'root' but you are 'stephen'  
-- also members of the 'root' group would be permitted  
-- you could use 'sudo' but this is not recommended  
-- it's better to add the device to the 'plugdev' group  
sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"04e6\", ATTRS{idProduct}==\"5591\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'  
sudo udevadm control -R # then re-attach device  
I'm not trying serial devices because you haven't told me  
-- add the option '--search-tty' to have me looking  
-- but beware that this may break other serial devs  
Sorry, but I couldn't find any contactless device``
     * Follow the instructions in the error message that you get and then reboot the Raspberry Pi
     * Run  ``python3 -m nfc`` again and this time you should get a message like this: 
        * ``I'm now searching your system for contactless devices  
** found SCM Micro SCL3711-NFC&RW PN533v2.7 at usb:002:024  
I'm not trying serial devices because you haven't told me  
-- add the option '--search-tty' to have me looking  
-- but beware that this may break existing connections``
    * If you do, then you're good to go!
    * ** FIX THIS (get the right error messages)**

### Run the Program
-   From **directory**, run: 
``sudo python3 mysonos.py -sonosUri http://localhost:5005 -sonosRoom kitchen``
    
### Options
Example
`sudo python3 sonos-nfc-read.py -sonosURI [node-sonos-http-api endpoint] -sonosRoom [Room Name] -cardTimeout [seconds] -debounce [seconds]`

The programm will wait until you represent a card that was written with the service before. It will take the URI and send it to the sonos controller that can run on the same machine or on a server if you you like to leverage a central endpoint for other actions as well.
*  `cardTimeout` is an optional parameter for the number of seconds to wait when the same card is read multiple times in a row. default=0
*  `debounce` is an optional parameter for the number of seconds to wait after a card is read before listening for more cards. default=3
* ``sonosRoom`` 
* ``sonosURI`` - default is ``localhost:5005``. 
* ``write``
    * ``yes``
    * ``loop`` 
* ``uri``
* ``test``


# Installations for RC522 NFC Reader
**Connect your Mifare RC522**
- [Tutorial how to connect](https://www.youtube.com/watch?v=IeuQNXSNzxA)
-   Test Python-Sonos-NFC
-   From directory where python-sonos-nfc is downloaded
``sudo python3 sonos-nfc-read.py -sonosUri http://localhost:5005 -sonosRoom kitchen``
-   Make sure to alter default sonosRoom as necessary


# Installations for Mopidy and USB NFC Reader
* **Add MOPIDY**
* See NFCPy installation instructions above

# Customization
Node Sonos Server
-   Customize the Sonos HTTP API for your speaker system
    -   Edit example.json in the Presets folder
-  Customize the Sonos HTTP API for your Spotify Account
	-  Turns out this isn’t actually required if you set up Spotify on your Sonos speakers



# Add Startup Scripts
-   Get Python-Sonos-NFC to run at startup
``sudo nano /etc/rc.local``

-   Add **this code** to this text file (**change kitchen**)
```
#Start Sonos-Node  
su pi -c 'node /home/pi/SonosProject/node-sonos-http-api/server.js < /dev/null &'  
#Start Sonos-NFC-Read  
su pi -c 'python3 /home/pi/SonosProject/python-sonos-nfc/sonos-nfc-read.py -sonosUri http://localhost:5005 -sonosRoom kitchen > /home/pi/SonosProject/python-sonos-nfc/log.txt &'
```

Write Cards
----------

`python sonos-nfc-write.py -uri [URI]` 

will write a card with an URI that the sonos controller can play. 

Supported formats are: 
* Local Playlist: 
	* Format: playlist:[Playlist Name] 
	* Example: _playlist:Test 1_
* Spotify: 
	* Format: [Spotify URI] )
	* Example: _spotify:album:12gOUR61KU69vYMaKZOPHV_
* Apple Music: 
	* Format: applemusic:[song|album]:[id] 
	* Example: _applemusic:song:55364259_ or _applemusic:album:355363490_
* Amazon Music: 
	* Format: amazonmusic:[song|album]:[id] 
	* Example: _amazonmusic:song:B009C7ZG38_ or _amazonmusic:album:B00720Z8PS_
* TuneIn: 
	* Format: tunein:[id] 
	* Example: _tunein:8007_

# Test Some URLs
 Make sure to substitute the IP address for the device on which the Node server is running
-   [http://localhost:5005/kitchen/nfc/say/Hello%20Frank](http://localhost:5005/kitchen/nfc/say/Hello%20Frank)
-   [http://192.168.1.198:5005/kitchen/nfc/spotify:album:3NFNNMIWnByvVPvCf7LsRU](http://192.168.1.198:5005/kitchen/nfc/spotify:album:3NFNNMIWnByvVPvCf7LsRU)
-   [http://192.168.1.198:5005/kitchen/pause](http://192.168.1.198:5005/kitchen/pause)

### Stuff to Do
* Upgrade the old NFC MFRC522 code
* Setup Mopidy
* Setup Bluetooth
* See if it makes sense to integrate this: https://nfcpy.readthedocs.io/en/latest/examples/tagtool.html to mysonos.py
