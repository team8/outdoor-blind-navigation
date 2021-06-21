#! /usr/bin/python

from gps import *
import time
import openrouteservice as ors


gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
currentLat = 0.0
currentLon = 0.0

try:
    #please initialize this with the api key
    client = ors.Client(key='')

    while True:
        report = gpsd.next()  #
        if report['class'] == 'TPV':
            currentLat = getattr(report, 'lat', 0.0)
            currentLon = getattr(report, 'lon', 0.0)
            print(currentLat, "\t", currentLon)
            coordinate = [currentLat, currentLon]
            reverse = client.pelias_reverse(
                point=coordinate,
                validate=True,
            )
            print(reverse.raw)

        time.sleep(0.1)

except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
    print("Done.\nExiting.")
