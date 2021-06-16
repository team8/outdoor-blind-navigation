# Author: Jonathan Woolf jwool003@ucr.edu

This GPS package is compatible with all NMEA 0183 compliant <a href="https://www.amazon.com/HiLetgo-G-Mouse-GLONASS-Receiver-Windows/dp/B01MTU9KTF/ref=sr_1_8?keywords=gps+usb&qid=1560277792&s=gateway&sr=8-8">USB GPS receivers</a>. When called, the gpsData() function connects to the active port, for example "ttyACM0", to read in NMEA sentences and return latitude, longitude, MPH, timestamp in PST, and the date. The function also outputs data to three separate text files. Pos.txt will always store the most recent position of the device, log.txt will maintain a log of position and speed that is updated once per minute, and speed.txt will keep a log that only updates as the device moves.

In the example script, getIPAddress() prints out the IP address of the device, then gpsData(), whithin an infinite loop nested in a try / except block, prints its return statement to terminal. Type 'ctrl c' to guarantee that the port is closed when you end the program.

The final script included is chartPath.py which combines the functionality of gps.py with pygmaps.py to generate an html map which shows the device's journey from point A to point B. Simply run the scipt at your starting location and press 'ctrl c' when you have reached your destination to generate the map.

## Give yourself permanent access to the port:
    # Discover which serial port is in use
    python -m serial.tools.list_ports
    # Navigate to rules.d directory
    cd /etc/udev/rules.d
    # Create a new rule file
    sudo touch my-newrule.rules
    # Open the file
    sudo vim my-newrule.rules
    # Add the following:
    #KERNEL=="ttyACM0", MODE="0666"

## Tutorial:
#### Dependencies
    pip install PYserial
#### Access gpsData()
    import gps
    port = gps.serialPortInit()
    gps.gpsData(port)
