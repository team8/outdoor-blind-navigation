import cv2
import model_composition
import image_processing as image_proc
import numpy as np
import constants

live_feed = cv2.VideoCapture(constants.video_training_data_path)

model = model_composition.model

while live_feed.isOpened():
    ret, capture = live_feed.read()
    if ret:
        processed_img = image_proc.pre_processing(capture)
        processed_img = np.expand_dims(processed_img, 0)
        prediction = model.predict(processed_img)
        print("Prediction: {}".format(constants.reverse_categories.get(np.array(prediction).argmax())))
        print("Confidence: {}".format(max(prediction)))
        print(prediction)
        cv2.imshow("Live Feed", capture)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
