import cv2
import tensorflow as tf
import numpy as np
import time
from utils.circularBuffer import CircularBuffer

classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk', 'Nothing Detected']
model_path = "./sidewalk_classification/sidewalk_classification_model_resnet.h5"
readings_buffer_size = 10
image_preprocessing_dimens = (100, 100)
detection_threshold = 0.85

class SidewalkClassification:
    def __init__(self):
        self.model = tf.keras.models.load_model(model_path)
        self.readings_buffer = CircularBuffer(readings_buffer_size)

    def get_frame_classification(self, image: np.ndarray) -> str:
       processed_frame = np.expand_dims(cv2.resize(image, image_preprocessing_dimens), 0)
       feedforward_result = self.model.predict(processed_frame).tolist()[0]

       self.readings_buffer.add(None if feedforward_result == None or max(feedforward_result) < detection_threshold else feedforward_result)
       averaged_result = self.readings_buffer.mean()
       return classes[len(classes) - 1] if averaged_result is None else classes[np.argmax(averaged_result)]

