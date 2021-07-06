import constants
import openrouteservice as ors
import json
import gps_state
import speech_2_text
import directions
import time


client = ors.Client(key=constants.api_key)

coords = [[], []]


# when given an address or place as a string, finds coordinates and other info
def geocode(name, start):  # start = True means you are geocoding for the start location
    if start == False:
        circle_center = coords[0]
        route = client.pelias_search(name, size=1, circle_point=circle_center, circle_radius=30)
    else:
        route = client.pelias_search(name, size=1)

    if (route["features"] == []):
        return None
    return route

# current_address = gps_state.get_current_address()
# print(current_address)
# start = geocode(current_address , True)

for i in range(0, 50): print("\n");
coords[0] = gps_state.get_current_coordinate()
print("Getting GPS Coordinates ...\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(3)
for i in range(0, 50): print("\n");

print("Received GPS Coordinates\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(3)
for i in range(0, 50): print("\n");
print("For purposes of not disclosing location, random location of Utah FRC Regional is being used")

coords[0] = [-111.950246199, 40.7016305268]
# reverse = client.pelias_reverse(
                # point=coords[0],
                # validate=True,
            # )
# print("Start Location: ", reverse["features"][0]["properties"]["name"])
print("Start Location: 3200 South Decker Lake Drive West Valley City, Utah 84119\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(5)
for i in range(0, 50): print("\n");
print("Enter in wanted destination:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
# destination_speech = speech_2_text.get_speech_to_text()
destination_speech = "Holiday Inn"
time.sleep(4)
print("Wanted Location: ", destination_speech, "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(4)
destination = geocode(destination_speech, False)



if destination == None:
    print("No such location found. Try again.")
else:
    print ("Getting directions...\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    coords[1] = destination["features"][0]["geometry"]["coordinates"]
    directions.get_directions(coords[0], coords[1])
    import visualize
