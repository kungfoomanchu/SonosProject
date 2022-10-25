# Raspberry Pi + NFC + Sonos + Mopidy Project
## What it does

This library can be leveraged in combination with [node-sonos-http-api](https://github.com/gsaurer/node-sonos-http-api) to control the sonos service over RFID cards. This allows you to build a very flexible service for your children or to digitize your library but still interact with it via physical media (an NFC card).

Inspired by Montessori teachings that emphasize tactile learning and encourage kids to have a level of independence. Cards can be created to play songs, albums, audiobooks, and podcasts to let kids choose what they want to listen to.

Attributions
* This is originally a fork of [gsaurer's python-sonos-nfc](https://github.com/gsaurer/python-sonos-nfc) project

Requirements:
* Raspberry Pi Zero W or Raspberry Pi 3B+, Raspberry Pi 4
* Python 3
* Node
* A Sonos speaker!
* An NFC reader
	* Recommended USB NFC Reader: [Sony RC-S380](https://www.amazon.com/gp/product/B00VR1WARC/). With this, you can use any almost NTAG NFC cards
	* If you aren't using a USB NFC reader, then you must use this one: **Mifare RC522 RFID**. You can find it on Amazon. And it will ***only*** work with **MIFARE Classic 1K cards**
* All dependencies below
* Optional
	* [Print your own NFC cards](https://magicard.com/id-printers/pronto/)
	* [JAM HAT](https://thepihut.com/products/jam-hat)
		* Highly recommended, but only works with the USB NFC reader

Supported Services
* Local Sonos playlist
* Spotify
* Apple Music
* Amazon Music
* Tunein

## There is much to install for this project, so please follow these instructions carefully
First step is obviously to set up your Raspberry Pi. 
Then install this git repository. Do that by running this command:
```git clone https://github.com/kungfoomanchu/SonosProject.git```
Note that the rest of the installation will work best if you clone this repository directly to your ``home`` directory on the pi. This will create a directory named ``SonosProject`` 

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
-   Check If Everything Is Installed Correctly
``node -v `` 
``npm -v``

### node-sonos-http-api
There are two ways to get node-sonos-http-api up and running

 1. You can use the version included in *SonosProject*. This version is guaranteed to work, however it won't be the most up to date
 2. Clone the node-sonos-http-api Repository:
```git clone https://github.com/jishi/node-sonos-http-api.git```
If you go this route, you will have to add ``nfc.js`` which is located in **Extra_Files** to this directory ``node-sonos-http-api/lib/actions``

Install the node server:
* Start by fixing your dependencies. Invoke the following command from the `node-sonos-http-api` folder:
`npm install --production`
This will download the necessary dependencies if possible.
* start the server by running
`npm start`
* Further information about usage is located here: [https://github.com/jishi/node-sonos-http-api](https://github.com/jishi/node-sonos-http-api)


## Installations for Various Lights and Python Packages
Blinkstick
* These are slightly modified instructions from this page: [https://www.blinkstick.com/help/raspberry-pi-integration](https://www.blinkstick.com/help/raspberry-pi-integration)
* This is likely already installed on your Pi
	* First you will need to install required packages. Pip lets you manage Python packages easier and Python development headers are required to install the websocket-client package:
``sudo apt-get install -y python-pip``
* Install Python BlinkStick package (make sure to install it with ``sudo``):
``sudo pip3 install blinkstick``
* Run the control script check if Raspberry Pi has detected BlinkStick correctly:
``sudo blinkstick --info``
* You can find details about more examples in the  [readme](https://github.com/arvydas/blinkstick-python/blob/master/README.md).
* This is supposed to work, but I don't think it does
	* If you don't want to sudo each time you want to access BlinkStick, then run the following command (this may not work properly for Python 3):
``echo "SUBSYSTEM==\"usb\", ATTR{idVendor}==\"20a0\", ATTR{idProduct}==\"41e5\", MODE:=\"0666\" | sudo tee /etc/udev/rules.d/85-blinkstick.rules"``
* More resources for BlinkStick
     * [https://github.com/arvydas/blinkstick-python/wiki/Command-line-tool-options](https://github.com/arvydas/blinkstick-python/wiki/Command-line-tool-options)
    - [https://github.com/arvydas/blinkstick-python](https://github.com/arvydas/blinkstick-python)

JamHat
* For more information: https://github.com/modmypi/Jam-HAT
* You shouldn't need to install anything, but just in case, you can run this:
```
sudo apt-get update
sudo apt-get install python3-gpiozero python-gpiozero
```

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
-- the device is owned by 'root' but you are 'pi'  
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

### Run the Program
-   Navigate to the ``SonosProject/nfcpy_sonos`` directory and run: 
``sudo python3 mysonos.py -sonosUri http://localhost:5005 -sonosRoom kitchen``
    
### Options
Example
`sudo python3 sonos-nfc-read.py -sonosURI [node-sonos-http-api endpoint] -sonosRoom [Room Name] -lightsOnOff on -cardTimeout [seconds] -debounce [seconds]`

The program will wait until you represent a card that was written with the service before. It will take the URI and send it to the sonos controller that can run on the same machine or on a server if you you like to leverage a central endpoint for other actions as well.
*  `cardTimeout` is an optional parameter for the number of seconds to wait when the same card is read multiple times in a row. default=0
*  `debounce` is an optional parameter for the number of seconds to wait after a card is read before listening for more cards. default=3
* ``sonosRoom`` - default is ``kitchen``
* ``sonosURI`` - default is ``localhost:5005``. 
* ``write`` - the default is ``no``, thus default mode is read mode. Type ``yes`` if you want to write individual cards, ``loop`` if you want to write multiple cards from google spreadsheet'. You can figure out what those do yourself
	* ``uri`` optional parameter to use in addition to ``write``. This will use the uri you input and write it to the card
* ``-lightsOnOff`` - the default is off. Type ``on`` to turn on the lights
* ``-lightType`` - options are ``jamhat``, ``blinkstick`` and ``GPIO``
* ``test`` - default is off. Use this to run all code except for NFC read or writes
* ``quietTime`` - default is off. Type ``yes`` to enable quiet time from 9 PM to 7 AM. You can edit the times in the code. 
	* ***This currently only works for the USB NFC reader*** 


# Installations for RC522 NFC Reader
### SPI-Py
Clone the repository:
``` git clone https://github.com/lthiery/SPI-Py.git```
Install it: 
1.  Clone or download this repository, navigate to the SPI-Py directory, and install the library using the following command. (Must be installed in Python 3).
```sudo python3 setup.py install```

3.  Make sure the SPI interface is enabled for your Raspberry Pi. This can be done using the raspi-config utility. For more information on this, please find via Google.
```sudo raspi-config```

### MFRC522py
* MFRC522.py from the [repository](https://github.com/mxgxw/MFRC522-python) is included in this project and changed to support python v3

### Mifare RC522
Connect your Mifare RC522
- You'll have to figure out how to do this. Here is a [video tutorial how to connect](https://www.youtube.com/watch?v=IeuQNXSNzxA) and here is a [written one](https://pimylifeup.com/raspberry-pi-rfid-rc522/)

### Run the Program
-   Navigate to the ``SonosProject/python-sonos-nfc`` directory and run: 
``sudo python3 sonos-nfc-read.py -sonosUri http://localhost:5005 -sonosRoom kitchen``
-   Make sure to alter ``sonosRoom`` as necessary


# Installations for Mopidy and USB NFC Reader
* You'll have to figure that one out yourself as well depending on your Mopidy setup. It is verified to work with this device: [https://shop.pimoroni.com/products/pirate-radio-pi-zero-w-project-kit](https://shop.pimoroni.com/products/pirate-radio-pi-zero-w-project-kit) and with this installer: [https://github.com/pimoroni/phat-beat#full-install-recommended](https://github.com/pimoroni/phat-beat#full-install-recommended)
* Install NFCPy as well. See NFCPy installation instructions above

# Bluetooth Media Buttons
You'll have to figure that one out yourself, but there is code to make it work with the Sonos node server. It is verified to work with this bluetooth remote: [https://www.amazon.com/gp/product/B00RM75NL0/](https://www.amazon.com/gp/product/B00RM75NL0/)

# Customization
Node Sonos Server
-   Customize the Sonos HTTP API for your speaker system
    -   Edit ``example.json`` in the ``!Extra_Files/presets`` folder then move this folder to ``node-sonos-http-api``
-  Customize other settings for ``node-sonos-http-api`` 
	- If you have Spotify or your desired music service set up on the Sonos app, you don't have to perform further customization here.
	- An example ``settings.json`` file is located in ``!Extra_Files`` and you can edit it then move it to ``node-sonos-http-api``


# Add Startup Scripts
-   Get Python-Sonos-NFC to run at startup
	- To do this, you'll have to edit the ``rc.local`` file. Get to it by navigating to the root directory of the Pi by entering ``cd ..`` a number of times until you are there. Then run the following command
``sudo nano /etc/rc.local``
	-   Now add the code below to this file. You'll have to edit some of the lines to make sure they are pointed to the correct file and the settings are as you want them.  to this text file (**change kitchen**)
	- Make sure to save the file correctly. Google how to do this
```
# Start Sonos HTTP API
su pi -c 'node /home/pi/SonosProject/node-sonos-http-api/server.js < /dev/null &'

# Start RC522 NFC Reader
# su pi -c 'python3 /home/pi/SonosProject/python-sonos-nfc/sonos-nfc-read.py -sonosUri http://localhost:5005 -sonosRoom Kitchen > /home/pi/SonosProject/python-sonos-nfc/log.txt &'

# Start NFCPy USB NFC Reader
su pi -c 'python3 /home/pi/SonosProject/nfcpy_sonos/mysonos.py -sonosUri http://localhost:5005 -sonosRoom Kitchen -lightsOnOff on &'

# Start JamHat buttons
su pi -c 'python3 /home/pi/SonosProject/nfcpy_sonos/jamhat_buttons.py &'

# Start Bluetooth Controller
su pi -c 'python3 /home/pi/SonosProject/nfcpy_sonos/bluetooth_media_button_mapping_to_sonos.py &'

# Restart Each Night at 3 AM
su pi -c 'shutdown -r 03:00 &'

# Start Buttons for GPIO Breadboard
# su pi -c 'python3 /home/pi/SonosProject/python-sonos-nfc/sonos-nfc-button1.py &'
# su pi -c 'python3 /home/pi/SonosProject/python-sonos-nfc/sonos-nfc-button2.py &'
# su pi -c 'python3 /home/pi/SonosProject/python-sonos-nfc/sonos-nfc-button3.py &'
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
 If you test these URLs on a computer other than the Pi where the node server is running, make sure to substitute ``localhost`` with the IP address for the device on which the Node server is running
-   [http://localhost:5005/kitchen/nfc/say/Hello%20Frank/en-us/80](http://localhost:5005/kitchen/nfc/say/Hello%20Frank/en-us/80)
-   [http://localhost:5005/kitchen/nfc/spotify:album:3NFNNMIWnByvVPvCf7LsRU](http://localhost:5005/kitchen/nfc/spotify:album:3NFNNMIWnByvVPvCf7LsRU)
-   [http://localhost:5005/kitchen/pause](http://localhost:5005/kitchen/pause)
-   [http://localhost:5005/kitchen/clip/sample_clip.mp3](http://localhost:5005/kitchen/clip/sample_clip.mp3) - This will play a sound clip in the folder ``node-sonos-http-api/static/clips``
-   [http://localhost:5005/kitchen/volume/36](http://localhost:5005/kitchen/volume/36) - This sets the volume to 36
-   [http://localhost:5005/Kitchen/playlist/test](http://localhost:5005/Kitchen/playlist/test) - This will play the Sonos playlist named 'test'. Substitute 'test' for your own playlist
-   For more functionality, see [https://github.com/jishi/node-sonos-http-api](https://github.com/jishi/node-sonos-http-api). Most of it should work, but you might have to experiment

### Stuff to Do
* Upgrade the old NFC MFRC522 code
	* Add quietTime to MFRC522 code
* See if it makes sense to integrate this: https://nfcpy.readthedocs.io/en/latest/examples/tagtool.html to mysonos.py
* Explain ``settings.ini`` in ``nfcpy_sonos`` folder
