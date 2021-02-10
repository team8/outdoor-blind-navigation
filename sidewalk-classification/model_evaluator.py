import cv2
import tensorflow as tf
import numpy as np
from utils.circularBuffer import CircularBuffer

classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk']
model = tf.keras.models.load_model("sidewalk_classification_model.h5")
vid = cv2.VideoCapture("/home/aoberai/Downloads/1080p.mov")
predictions = CircularBuffer(10, [])
while True:
    orig_cap = cv2.flip(vid.read()[1], 1)
    cap = cv2.resize(orig_cap, (100, 100))
    raw_prediction = (model.predict(np.expand_dims(cap, 0))).tolist()[0]
    print(raw_prediction)
    predictions.add(raw_prediction)
    print(classes[np.argmax(predictions.average())])
    cv2.imshow("Test", orig_cap)
    cv2.waitKey(1)
