import threading
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
counter = 0
display = Display()
while True:
    capture = capturer.getImages().getLast()
    capture = cv2.resize(capture, (480, 360))
    state_classifier_inference = sc.get_inference()
    object_localizer_inference = ol.get_inference()
    # print(object_localizer_inference)
    print(state_classifier_inference if counter % 2 == 0 else object_localizer_inference)
    print("Object Detection FPS", ol.getFPS())
    cv2.imshow("Stream", capture)
    cv2.waitKey(1)
    display.update(state, orig_cap, obs)
    counter += 1
