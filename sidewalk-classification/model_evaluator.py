import cv2
import tensorflow as tf
import numpy as np
from utils.circularBuffer import CircularBuffer

classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk']
model = tf.keras.models.load_model("sidewalk_classification_model.h5")
vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk.mp4")
predictions = CircularBuffer(10, [])
state = ""
while True:
    orig_cap = cv2.resize(cv2.rotate(vid.read()[1], cv2.ROTATE_90_COUNTERCLOCKWISE), (480, 360))
    cap = cv2.resize(orig_cap, (100, 100))
    raw_prediction = (model.predict(np.expand_dims(cap, 0))).tolist()[0]
    predictions.add([None, None, None] if max(raw_prediction) < 0.9 else raw_prediction)
    averaged_prediction = np.argmax(predictions.average())
    if averaged_prediction is None and None not in averaged_prediction:
        state = "Nothing detected"
    else:
        state = classes[np.argmax(predictions.average())]
    cv2.imshow(state, orig_cap)
    cv2.waitKey(1)

