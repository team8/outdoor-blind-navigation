import cv2
import tensorflow as tf
import time
from utils.circularBuffer import CircularBuffer
from display import Display
import numpy as np
classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk']
model = tf.keras.models.load_model("sidewalk_classification_model_resnet.h5")
# vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk.mp4")
rotate = False
vid = cv2.VideoCapture(0)
time.sleep(3)
capture = vid.read()
print(capture[0])
if vid.read()[0] is False:
    vid = cv2.VideoCapture("/home/aoberai/Downloads/Sidewalk_Final.mp4")
    # vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk.mp4")
    rotate = True
    position_video = 0.4
    vid.set(cv2.CAP_PROP_POS_FRAMES, (position_video * vid.get(cv2.CAP_PROP_FRAME_COUNT)))


cb = CircularBuffer(20, minNumPercent = 0.8)
state = ""
sidewalk_display = Display((480,360))
print(1)
while True:
    start_time = time.time()
    orig_cap = cv2.resize(cv2.rotate(vid.read()[1], cv2.ROTATE_90_COUNTERCLOCKWISE) if rotate == True else vid.read()[1], (480, 360))
    cap = cv2.resize(orig_cap, (100, 100))
    raw_prediction = (model.predict(np.expand_dims(cap, 0))).tolist()[0]
    cb.add(None if max(raw_prediction) < 0.8 else raw_prediction)
    averaged_prediction = cb.mean()
    if averaged_prediction is None:
        state = "Nothing detected"
    else:
        state = classes[np.argmax(averaged_prediction)]
    end_time = time.time()
    confidence =  max(averaged_prediction) * 100 // 1 if averaged_prediction is not None else None
    print("FPS:", 1/ (end_time - start_time), state, "Confidence:", confidence)
    sidewalk_display.update(state, orig_cap)

#runfile("D:/Maxwell/SpecialRobotStuff/blind-navigation/src/sidewalk-classification/model_evaluator.py")