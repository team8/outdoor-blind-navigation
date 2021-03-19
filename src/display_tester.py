
from display import Display
import cv2
display = Display()

video = cv2.VideoCapture(0)
capture = video.read(0)[1]

counter = 0
obs = [('person', '30.26', (250.02488708496094, 85.19881439208984, 62.963951110839844, 129.86805725097656)), ('traffic light', '34.59', (246.94873046875, 83.70958709716797, 59.21462631225586, 127.32121276855469))]
display.putVideoFeed(capture)
display.putObjects(obs)
display.displayScreen()
