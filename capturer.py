import cv2
from utils.circularBuffer import CircularBuffer
import time

try:
    stream = cv2.VideoCapture(0)
    cv2.resize(stream.read()[1], (100, 100)) # throws exception if webcam is not attached
except Exception as e:
    # stream = cv2.VideoCapture('./Sidewalk.mp4')
    # stream = cv2.VideoCapture('/home/aoberai/Downloads/DemoFinalFinal.mp4')
    # stream = cv2.VideoCapture('/home/aoberai/Downloads/betterwork.MOV')
    # stream = cv2.VideoCapture('/home/aoberai/Downloads/Long_Sidewalk_Final.mp4')
    # stream = cv2.VideoCapture('/home/aoberai/Downloads/NewTest.mp4')
    # stream = cv2.VideoCapture('/home/aoberai/Downloads/2ndStopSign.mp4')
    # stream = cv2.VideoCapture('/home/aoberai/Downloads/3rdStopSign.mp4')
    stream = cv2.VideoCapture('/home/aoberai/Downloads/4thStopSign.mp4')
    # stream = cv2.VideoCapture('/home/aoberai/Downloads/ChoreographWalking.mp4')
    # position_video = 0.05 # Position of video to start at
    # stream.set(cv2.CAP_PROP_POS_FRAMES, (position_video * stream.get(cv2.CAP_PROP_FRAME_COUNT)))
    # for presentation video, use newTest and 3rdStopSign
images_queue = CircularBuffer(2)
def capturer():
    firstRun = True
    print("Capturing Starting")
    while True:
        images_queue.add(stream.read()[1])
        if firstRun:
            time.sleep(14)
        else:
            time.sleep(0.07)
            # time.sleep(0.3)
        firstRun = False

def getImages():
    return images_queue


