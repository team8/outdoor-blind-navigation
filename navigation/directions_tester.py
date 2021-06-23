import openrouteservice as ors
import json
import constants

client = ors.Client(key=constants.api_key)

coords = [[-122.1305079,37.4349431],[-122.1576698,37.4358156]]
route = client.directions(coordinates=coords,profile='driving-car',format='geojson')

j = open("route.json","w")
json.dump(route, j, indent = 1)

print(route)
j.close()
