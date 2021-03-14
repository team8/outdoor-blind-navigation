import cv2
from utils.circularBuffer import CircularBuffer
import time
stream = cv2.VideoCapture(0)
images_queue = CircularBuffer(3)

def capturer():
    print("Capturing Starting")
    while True:
        if stream.isOpened():
            images_queue.add(stream.read()[1])
            time.sleep(0.01)

def getImages():
    return images_queue


