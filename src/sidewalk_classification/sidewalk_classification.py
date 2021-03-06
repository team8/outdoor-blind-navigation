import cv2
import tensorflow as tf
import numpy as np
import time
import constants
from utils.circularBuffer import CircularBuffer

class SidewalkClassification:
    def __init__(self):
        self.model = tf.keras.models.load_model(constants.model_path)
        self.readings_buffer = CircularBuffer(constants.readings_buffer_size)

    def get_frame_classification(self, image: np.ndarray) -> str:
       processed_frame = np.expand_dims(cv2.resize(image, constants.image_preprocessing_dimens), 0)
       feedforward_result = self.model.predict(processed_frame).tolist()[0]

       self.readings_buffer.add(None if feedforward_result == None or max(feedforward_result) < constants.detection_threshold else feedforward_result)
       averaged_result = self.readings_buffer.mean()
       return constants.classes[len(constants.classes) - 1] if averaged_result is None else classes[np.argmax(averaged_result)]

