import openrouteservice as ors
import json
import constants


client = ors.Client(key=constants.api_key)

def get_directions(starting_coords, ending_coords):
    # coords = [[-122.1305079,37.4349431],[-122.1576698,37.4358156]]
    coords = [starting_coords, ending_coords]

    route = client.directions(coordinates=coords,profile='driving-car',format='geojson')

    j = open("route.json","w")
    json.dump(route, j, indent = 1)
    j.close()
    print(route)
