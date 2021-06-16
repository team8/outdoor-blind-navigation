#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to interact w/ NMEA 0183 compatible USB GPS receivers
GPL 3.0
"""

# Built-in/Generic Imports
import os
import socket
import serial.tools.list_ports
# […]

__author__ = "Jonathan Woolf"
__credits__ = "Jonathan Woolf"
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Jonathan Woolf"
__email__ = "jwool003@ucr.edu"
__status__ = 'alpha'

# Global scope
startTime = -1
# […]

# Pass in UTC string, output PT string
def utcToPT(utc):
    # PT is 17hours ahead of UTC
    # Remove the next 3 lines to keep UTC otherwise adjust 170000 as needed
    PT = 170000 + int(float(utc))
    if(PT >= 240000):
        PT = PT - 240000
    PT = str(PT)
    while(len(PT) < 6):
        PT = '0' + PT
    hour = PT[0] + PT[1]
    min = PT[2] + PT[3]
    sec = PT[4] + PT[5]
    timestamp = hour + ':' + min + ':' + sec
    return(timestamp, sec)

# Pass in DMS and direction, output DD
def decimalDegrees(dms, direction):
    DD = int(float(dms)/100)
    SS = float(dms) - DD * 100

    DD = round(DD + SS/60, 7)
    tmp1 = len(str(int(DD)))
    tmp2 = len(str(DD))

    # Rounds DD (decimal degrees) for more consistent values
    if((tmp1 == 1 and tmp2 < 9) or (tmp1 == 2 and tmp2 < 10) or (tmp1 == 3 and tmp2 < 11)):
        DD = round(DD +  .0000001, 7)
    # If South latitude is negative / If West longitude is negative
    if(direction == "S" or direction == "W"):
        DD = DD * -1
    return(DD)

# Obtain the IP address of the device
def getIPAddress():
    # Create a new socket using the default socket address (AF_INET)
    # The socket type SOCK_DGRAM is used over the more robust SOCK_STREAM to reduce computer and network stress
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Try to print the IP address and write it to the backup file
    try:
        s.connect(("8.8.8.8", 80))
        return(s.getsockname()[0])
        with open("ip.txt", "w") as ip:
            ip.write(s.getsockname()[0])
            s.close()
    # If the connection fails, read the IP from backup or print IP address not found
    except:
        if(os.path.exists('ip.txt')):
            with open("ip.txt", "r") as ip:
                return(ip.read())
        else:
            return("IP address not found!")

# Opens port and resets log and speed text files
def serialPortInit():
    # create a list of accessible ports
    port = ([comport.device for comport in serial.tools.list_ports.comports()])

    # If no ports are accessible exit
    if(len(port) == 0):
        print("Error: GPS unit not found!")
        exit()

    # Open port
    port = serial.Serial(port[0], baudrate = 9600)

    # Verify port is open
    if(port.is_open):
        print(port.name, "is open!")
        # Reset log and speed files every time the python script starts
        with open("log.txt", "w") as log:
            log.write("latitude, longitude, timestamp\n")
        with open("speed.txt", "w") as spd:
            spd.close()
        return(port)

# Pass in active serial port, output: latitude, longitude, MPH, and timestamp
def gpsData(GPS):
    global startTime
    data = [-1] * 3
    timestamp = "-1"
    sec = -1
    while(data[0] != "$GPGGA"):
        line = GPS.readline()
        data = line.decode().split(",")

    if(data[0] == "$GPGGA"):
        # Fix quality: 0 = invalid
        if(data[6] != "0"):
            # data[1] returns time in UTC, convert it to PT and create a timestamp
            PT = utcToPT(data[1])
            sec = PT[1]
            timestamp = PT[0]
            if(startTime == -1):
                startTime = int(sec)

    while(data[0] != "$GPRMC"):
        line = GPS.readline()
        data = line.decode().split(",")

    if(data[0] == "$GPRMC"):
        # Status A=active or V=Void
        if(data[2] == "A"):
            # Convert from DMS (degrees, minutes, seconds) to DD (decimal degrees)
            # Removing decimalDegrees, data[4], and data[6] will immediately revert gpsData to returning DMS
            latitude = decimalDegrees(data[3], data[4])
            longitude = decimalDegrees(data[5], data[6])

            # Get date
            day = data[9][0] + data[9][1]
            month = data[9][2] + data[9][3]
            year = data[9][4] + data[9][5]
            date = day + "/" + month + "/" + year

            #1 knot = 1.15078 miles per hour
            mph = round(1.15078 * float(int(float(data[7]))), 1)

            # write MPH and timestamp to speed.txt file whenever MPH >= 0.1
            if(float(mph) >= 0.1):
                with open("speed.txt", "a") as spd:
                    spd.write("MPH: " + str(mph) + ", Timestamp: " + timestamp + "\n")
            # write latitude, longitude to .txt file
            with open("pos.txt", "w") as pos:
                pos.write("latitude, longitude, timestamp\n" + str(latitude)
                + ", " + str(longitude) +  ", " + timestamp + date + "\n")
            # write latitude, longitude, and timestamp to log.txt file every 60 seconds
            if(abs(int(sec) - startTime) == 0):
                with open("log.txt", "a") as log:
                    log.write(str(latitude) + ", " + str(longitude) + ", " + timestamp + date + "\n")
            # return latitude, longitude, and timestamp
            return(latitude, longitude, mph, timestamp, date)
        # If status is active attempt to return last documented location
        else:
            if(os.path.exists('pos.txt')):
                print("Error: satellites not found. Dislplaying last known coordinates:")
                with open("pos.txt", "r") as pos:
                    backup = pos.read().split('\n')
                    backup = backup[1].split(", ")
                    return(float(backup[0]), float(backup[1]), 'N/A', backup[2], backup[3])
            else:
                print("Error: satellites not found.")
