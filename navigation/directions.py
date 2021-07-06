import openrouteservice as ors
import json
import constants


client = ors.Client(key=constants.api_key)

def get_directions(starting_coords, ending_coords):
    coords = [starting_coords, ending_coords]

    route = client.directions(coordinates=coords, profile='foot-walking', format='geojson')

    j = open("route.json","w")
    json.dump(route, j, indent=1)
    j.close()
    # print(route)
