import cv2
from sidewalk_classification import ShiftClassification

classifier = ShiftClassification()
vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk_Compressed.mp4")

state = classifier.get_frame_classification(vid.read()[1])
print(state)

