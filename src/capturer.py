import cv2
from utils.circularBuffer import CircularBuffer
import time
# stream = cv2.VideoCapture(0)
try:
    stream = cv2.VideoCapture(0)
    cv2.resize(stream.read()[1], (100, 100))
except Exception as e:
    stream = cv2.VideoCapture('/home/aoberai/Downloads/Long_Sidewalk_Final.mp4')
    position_video = 0.2
    stream.set(cv2.CAP_PROP_POS_FRAMES, (position_video * stream.get(cv2.CAP_PROP_FRAME_COUNT)))

images_queue = CircularBuffer(1)

def capturer():
    print("Capturing Starting")
    while True:
        if stream.isOpened():
            images_queue.add(stream.read()[1])
            time.sleep(0.1)

def getImages():
    return images_queue


