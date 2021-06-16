#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example use of gps.py that prints to terminal in a loop until KeyboardInterrupt
GPL 3.0
"""

# Own modules
import gps
# […]

__author__ = "Jonathan Woolf"
__credits__ = "Jonathan Woolf"
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Jonathan Woolf"
__email__ = "jwool003@ucr.edu"
__status__ = 'alpha'

# Initialize port and get the IP address
port = gps.serialPortInit()
ip = gps.getIPAddress()

print(ip)


# Infinite loop until KeyboardInterrupt is detected
try:
    while True:
        data = gps.gpsData(port)
        # Unused - Just an example of how to grab data from the function
        latitude = data[0]
        longitude = data[1]
        MPH = data[2]
        timestamp = data[3]
        print(data)

# 'ctrl c' will close the serial port before exiting the program
except KeyboardInterrupt:
        port.close()
        if(port.is_open == False):
            print()
            print(port.name, "is closed!")
