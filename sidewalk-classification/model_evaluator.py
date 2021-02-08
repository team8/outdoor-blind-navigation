import cv2
import tensorflow as tf
import numpy as np
classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk']
model = tf.keras.models.load_model("sidewalk_classification_model.h5")
vid = cv2.VideoCapture("/home/aoberai/Downloads/1080p.mov")
while True:
    orig_cap = cv2.flip(vid.read()[1], 1)
    cap = cv2.resize(orig_cap, (100, 100))
    print(classes[np.argmax(model.predict(np.expand_dims(cap, 0)))])
    cv2.imshow("Test", orig_cap)
    cv2.waitKey(1)          
