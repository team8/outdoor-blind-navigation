import constants
import openrouteservice as ors
import speech_recognition as sr
import json
import gps_state


client = ors.Client(key=constants.api_key)

# when given an address or place as a string, finds coordinates and other info
def geocode(name):
    route = client.pelias_search(name, size=1)
    return route


start = geocode(gps_state.get_current_address())
destination = geocode("Starbucks, Mountain View, CA 94043") # use speech to text
print(start, destination)
# j = open("start.json", "w")
# json.dump(start, j, indent=1)
# j.close()
#
# j = open("destination.json", "w")
# json.dump(destination, j, indent=1)
# j.close()

coords = [[], []]
coords[0] = start["features"][0]["geometry"]["coordinates"]
coords[1] = destination["features"][0]["geometry"]["coordinates"]

route = client.directions(coordinates=coords, profile='driving-car', format='geojson', language='en')

j = open("route.json", "w")
json.dump(route, j, indent=1)
j.close()
