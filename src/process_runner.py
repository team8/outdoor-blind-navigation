import threading
import cv2
import sidewalk_classification
from sidewalk_classification.sidewalk_classification import SidewalkClassification as StateClassifier
from person_automobile_sign_detection.detector import Detector as ObjectLocalizer

sc = StateClassifier()
ol = ObjectLocalizer()
# stream = cv2.VideoCapture(0)
stream = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk_Compressed.mp4")
rotate = True
while True:
    capture = cv2.resize(cv2.rotate(stream.read()[1], cv2.ROTATE_90_COUNTERCLOCKWISE) if rotate == True else stream.read()[1], (480, 360))
    print(sc.get_frame_classification(capture))
    print(ol.get_inference())
    cv2.imshow("Stream", capture)
    # cv2.resize(capture, (416, 416)))
    cv2.waitKey(1)
