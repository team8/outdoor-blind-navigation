import webbrowser
import os
import time

# Sketch but works

os.system("git add route.json")
os.system("git commit -m \"new route generated\"")
os.system("git push")
time.sleep(5)
webbrowser.open("https://github.com/team8/outdoor-blind-navigation/blob/navigation/navigation/route.json")
