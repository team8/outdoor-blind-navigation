#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Uses device location to generate an html google map
GPL 3.0
"""

# Built-in/Generic Imports
import os
# […]

# Own modules
import gps
# […]

# Google's module (provided because pip doesn't have it)
import pygmaps
# […]

__author__ = "Jonathan Woolf"
__credits__ = "Jonathan Woolf, AnkitRai01, Google"
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Jonathan Woolf"
__email__ = "jwool003@ucr.edu"
__status__ = 'alpha'

print("Press 'ctrl c' to generate a map and terminate the script.")

port = gps.serialPortInit()
data = gps.gpsData(port)

latitude = data[0]
longitude = data[1]

path = [(data[0], data[1])]
print(data)

if(os.path.exists('map.html')):
    os.remove("map.html")

# Infinite loop until KeyboardInterrupt is detected
try:
    while True:
        data = gps.gpsData(port)
        if((abs(latitude - data[0]) or abs(longitude - data[1])) >= .0001):
            # list of coordinates
            path.append((data[0], data[1]))
            print("New coordinate registered!")
            print(data)
            latitude = data[0]
            longitude = data[1]
#'ctrl c' will generate the map and close the serial port before exiting the program
except KeyboardInterrupt:
        centerLat = (path[0][0] + latitude) / 2
        centerLong = (path[0][1] + longitude) / 2
        map = pygmaps.pygmaps(centerLat, centerLong, 14)
        map.addpoint(path[0][0], path[0][1], "# FF0000")
        map.addpoint(latitude, longitude, "# FF0000")
        # draw a line in b / w the given coordinates
        # 1st argument is list of coordinates
        # 2nd argument is colour of the line
        map.addpath(path, " 0000FF")
        map.draw('map.html')
        port.close()
        if(port.is_open == False):
            print()
            print(port.name, "is closed!")
