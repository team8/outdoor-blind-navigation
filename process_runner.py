import threading
import cv2
import sidewalk_classification
from sidewalk_classification.sidewalk_classification import SidewalkClassification as StateClassifier
from turn_classification.turn_classification import TurnClassification as TurnClassifier
from display import Display
import capturer
from person_automobile_sign_detection.detector import Detector as ObjectLocalizer
import time
from collision import CollisionDetector

threading.Thread(target=capturer.capturer).start()
time.sleep(1)


sc = StateClassifier()
ol = ObjectLocalizer()
tc = TurnClassifier()
display = Display(dimension=3)
cd = CollisionDetector(display.getViewerSize(), display.getStretchFactor())


counter = 0
while True:
    capture = capturer.getImages().getLast()

    state_classifier_inference = sc.get_inference()
    object_localizer_inference = ol.get_inference()
    turn_classifier_inference = tc.get_inference()
    object_collision_inference = cd.findCollisions(object_localizer_inference)
    print(turn_classifier_inference)
    # print(state_classifier_inference if counter % 2 == 0 else object_localizer_inference)
    # print(object_collision_inference)
    display.putVideoFrame(capture)
    display.putSidewalkState(state_classifier_inference)
    display.putObjects(object_localizer_inference, object_collision_inference) # TODO: Have display take in collision objects and color arrow differently to show possible collision
    display.displayScreen()

    counter += 1
