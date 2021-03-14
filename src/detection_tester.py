from person_automobile_sign_detection.detector import Detector
import threading
import capturer
import time

threading.Thread(target=capturer.capturer).start()
time.sleep(1)


model_prediction = Detector()
# while True:
    # print(model_prediction.get_inference())
