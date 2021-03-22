"""import threading
import cv2
import sidewalk_classification
from sidewalk_classification.sidewalk_classification import SidewalkClassification as StateClassifier
from display import Display
import capturer
from person_automobile_sign_detection.detector import Detector as ObjectLocalizer
import time


threading.Thread(target=capturer.capturer).start()
time.sleep(1)

sc = StateClassifier()
ol = ObjectLocalizer()
display = Display()


counter = 0
while True:
    capture = capturer.getImages().getLast()
    capture = cv2.resize(capture, (480, 360))
    #state_classifier_inference = sc.get_inference()
    #object_localizer_inference = ol.get_inference()
    # print(object_localizer_inference)
    #print(state_classifier_inference if counter % 2 == 0 else object_localizer_inference)

    # print("Object Detection FPS", ol.getFPS()

    object_localizer_inference = ("Bike", 301.3, 240, 150, 240,150)
    display.putVideoFeed(capture)
    #display.putSidewalkState(state_classifier_inference)
    display.putObjects(object_localizer_inference)
    display.displayScreen()

    # cv2.imshow("Stream", capture)
    # cv2.waitKey(1)
    counter += 1
"""
import cv2
import time
from display import Display

display = Display((416,416))

capture = cv2.imread("./display_resources/Carl.png")
obs = [('person', '30.26', (250.02488708496094, 85.19881439208984, 62.963951110839844, 129.86805725097656)), ('traffic light', '34.59', (246.94873046875, 83.70958709716797, 59.21462631225586, 127.32121276855469))]
while True:
    display.putVideoFeed(capture)
    display.putObjects(obs)
    display.drawArrow((0, 0), (150, 150))
    display.displayScreen()
    time.sleep(1)