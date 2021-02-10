import cv2
import tensorflow as tf
import numpy as np
classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk']
model = tf.keras.models.load_model("sidewalk_classification_model.h5")
# vid = cv2.VideoCapture("/home/aoberai/Downloads/1080p.mov")
vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk.mp4")
i = 0
while True:
    orig_cap = cv2.resize(cv2.rotate(vid.read()[1], cv2.ROTATE_90_COUNTERCLOCKWISE), (640, 480))
    if i % 3:
        cap = cv2.resize(orig_cap, (100, 100))
        prediction = model.predict(np.expand_dims(cap, 0))
        if prediction.max() > 0.9:
            print(classes[np.argmax(prediction)] + " Confidence:" + str(prediction.max()))
    cv2.imshow("Test", orig_cap)
    cv2.waitKey(1)
    i+=1
