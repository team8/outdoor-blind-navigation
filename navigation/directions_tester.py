import openrouteservice as ors
import json
import constants
import directions
import webbrowser

coords = [[-122.1305079,37.4349431],[-122.1576698,37.4358156]]
directions.get_directions(coords[0], coords[1])
webbrowser.open("https://github.com/team8/outdoor-blind-navigation/blob/navigation/navigation/route.json")

