import cv2
import tensorflow as tf
import numpy as np
import time
from utils.circularBuffer import CircularBuffer

classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk']
model = tf.keras.models.load_model("sidewalk_classification_model100.h5")
vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk.mp4")
cb = CircularBuffer(15)
state = ""
cb.initQueue([0, 0, 0])
while True:
    start_time = time.time()
    orig_cap = cv2.resize(cv2.rotate(vid.read()[1], cv2.ROTATE_90_COUNTERCLOCKWISE), (480, 360))
    cap = cv2.resize(orig_cap, (100, 100))
    raw_prediction = (model.predict(np.expand_dims(cap, 0))).tolist()[0]
    cb.add(None if max(raw_prediction) < 0.9 else raw_prediction)
    averaged_prediction = cb.mean()
    if averaged_prediction is None:
        state = "Nothing detected"
    else:
        state = classes[np.argmax(averaged_prediction)]
    end_time = time.time()
    
    cv2.imshow("Sidewalk Stream", orig_cap)
    print("FPS:", 1/ (end_time - start_time), state, np.argmax(averaged_prediction))
    cv2.waitKey(1)

