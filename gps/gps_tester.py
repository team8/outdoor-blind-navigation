import json

from gps import *
import time
import openrouteservice as ors


gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
currentLat = 0.0
currentLon = 0.0

try:
    client = ors.Client(key='5b3ce3597851110001cf624893d90c21680948129afaa561366cd798')

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
            tempJson = json.loads(reverse)
            print(tempJson["features"]["properties"]["name"])

            time.sleep(0.1)

except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
    print("Done.\nExiting.")


