import cv2
import threading
import tensorflow as tf
import numpy as np
import time
import capturer
from utils.circularBuffer import CircularBuffer

labels = ['Left Turn', 'No Turn', 'Right Turn']
model_path = "./turn_classification/turn_classification_model_final_v1.h5"
readings_buffer_size = 20
image_preprocessing_dimens = (100, 100)
detection_threshold = 0.5

class TurnClassification:

    def __init__(self):
        self.model = tf.keras.models.load_model(model_path)
        self.readings_buffer = CircularBuffer(readings_buffer_size, noneOverridePercent=0.5)
        self.images_queue = CircularBuffer(1)
        self.classifier_queue = CircularBuffer(1)
        threading.Thread(target=self.classification_starter).start()

    def capture_processing(self):
        while True:
            try:
                frame = capturer.get_images().get_last()
                if frame is not None:
                    preprocessed_frame = cv2.resize(frame, image_preprocessing_dimens, interpolation=cv2.INTER_LINEAR)
                    self.images_queue.add(np.expand_dims(preprocessed_frame, 0))
            except Exception as e:
                print("Capturing Not Working", e)

    def classification_starter(self):
        threading.Thread(target=self.capture_processing).start()
        while True:
            try:
                self.perform_inference(self.images_queue.get_last())
            except Exception as e:
                print("Classification Not Working", e)


    def perform_inference(self, image):
        feedforward_result = self.model.predict(image).tolist()[0]
        self.readings_buffer.add(None if feedforward_result == None or max(feedforward_result) < detection_threshold else feedforward_result)
        averaged_result = self.readings_buffer.mean()
        # print(averaged_result)
        self.classifier_queue.add("No Turn" if averaged_result is None else labels[np.argmax(averaged_result)])

    def get_inference(self):
        return self.classifier_queue.get_last()
