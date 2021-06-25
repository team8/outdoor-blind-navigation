import constants
import openrouteservice as ors
import json
# import gps_state
import speech_2_text

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


start = geocode("50 Embarcadero Road, Palo Alto, CA 94301", True)
coords[0] = start["features"][0]["geometry"]["coordinates"]

# start = geocode(gps_state.get_current_address())

destination_speech = speech_2_text.get_speech_to_text()
destination = geocode(destination_speech, False)
# print(start, destination)




if destination == None:
    print("No such location found. Try again.")

else:
    print ("Getting directions...")
    coords[1] = destination["features"][0]["geometry"]["coordinates"]
    route = client.directions(coordinates=coords, profile='foot-walking', format='geojson', language='en')
    j = open("route.json", "w")
    json.dump(route, j, indent=1)
    j.close()
