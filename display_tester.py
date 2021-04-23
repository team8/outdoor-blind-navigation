
from display import Display
import cv2
display = Display(2)

video = cv2.VideoCapture('./Sidewalk.mp4')

counter = 0
obs = [('car', 0, (550.4058227539062, 30.374237060546875, 76.12239837646484, 40.111534118652344), 1, (-60.89201354980469, 7.749721336364747, 100)), ('car', 0, (473.62353515625, 26.943071365356445, 29.894922256469727, 42.88824462890625), 2, (-60.89201354980469, 7.749721336364747, 100))]

while True:
    capture = video.read(0)[1]
    display.putVideoFrame(capture)
    display.putObjects(obs)
    display.putSidewalkState("Left of Sidewalk")
    display.displayScreen()
