import constants
import openrouteservice as ors
import json
import gps_state
import speech_2_text
import directions

client = ors.Client(key=constants.api_key)

coords = [[], []]


# when given an address or place as a string, finds coordinates and other info
def geocode(name, start):  # start = True means you are geocoding for the start location
    if start == False:
        circle_center = coords[0]
        route = client.pelias_search(name, size=1, circle_point=circle_center, circle_radius=5)
    else:
        route = client.pelias_search(name, size=1)

    if (route["features"] == []):
        return None
    return route

start = geocode(gps_state.get_current_address(), True)
coords[0] = start["features"][0]["geometry"]["coordinates"]

destination_speech = speech_2_text.get_speech_to_text()
destination = geocode(destination_speech, False)

if destination == None:
    print("No such location found. Try again.")
else:
    print ("Getting directions...")
    coords[1] = destination["features"][0]["geometry"]["coordinates"]
    directions.get_directions(coords[0], coords[1])
