from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
import threading
from utils.circularBuffer import CircularBuffer
import capturer
from queue import Queue
class Detector:
    weights_path = "person_automobile_sign_detection/yolov4-tiny.weights"
    config_path = "person_automobile_sign_detection/yolov4-tiny-original.cfg"
    data_file_path = "person_automobile_sign_detection/coco.data"

    network, class_names, class_colors = darknet.load_network(
                config_path,
                data_file_path,
                weights_path,
                batch_size=1
            )
    detections_queue = CircularBuffer(2)
    images_queue = Queue(maxsize=2)
    # images_queue = Queue()
    # fps_queue = Queue(maxsize=3)
    fps_queue = CircularBuffer(1)
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    colors = {"person": [255, 255, 0], "car": [100, 0, 0], "stop sign": [100, 100, 0]}
    def capture_processing(self):
        while True:
            try:
                frame = capturer.getImages().getLast()
                preprocessed_frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
                darknet_image = darknet.make_image(self.width, self.height, 3)
                darknet.copy_image_from_bytes(darknet_image, preprocessed_frame.tobytes())
                # if self.images_queue.size() > 0:
                # darknet.free_image(self.images_queue.get()[0])
                self.images_queue.put((darknet_image, preprocessed_frame))
                # print(self.class_names)
                # time.sleep(0.3)
            except Exception as e:
                print("Capturing Not Working", e)

    def display(self):
        while True:
            try:
                last_detection = self.detections_queue.getLast()
                last_image = self.images_queue.get()[1]
                fps = self.fps_queue.getLast()
                for detection in last_detection:
                    # print(detection)
                    x, y, w, h = detection[2]
                    xmin = int(x - (w / 2))
                    xmax = int(x + (w / 2))
                    ymin = int(y - (h / 2))
                    ymax = int(y + (h / 2))
                    # detections_average.add([xmax, ymax, xmin, ymin]) #this is wrong - should only do this for individual objects. this is just merging everything together (very bad)
                    # detections_mean = detections_average.mean()

                    # print(detection[0] + " FPS: " + str(fps))
                    display_image = cv2.rectangle(last_image, (xmax, ymax), (xmin, ymin), self.colors[detection[0]] if detection[0] in self.colors else [0, 100, 0], 4)
                cv2.imshow("Stream", display_image)
                cv2.waitKey(1)

                # print("FPS: " + str(1/(time.time() - frame_start_time)))
            except Exception as e:
                    print("Displaying Not Working", e)

    def get_inference(self):
        return self.detections_queue.getLast()
        # return {"label": self.detections_queue.getLast()[0], "bbox": self.detections_queue.getLast()[1]} if self.detections_queue.size() >= 1 and not (None in self.detections_queue.getList()) else None

    def detection_starter(self):
        # threading.Thread(target=self.display).start()
        while True:
            try:
                # while self.images_queue.get()[0] is None: time.sleep(0.1);

                last_darknet_image = self.images_queue.get()[0]
                last_time = time.time()
                detections = darknet.detect_image(self.network, self.class_names, last_darknet_image, thresh=0.25)
                self.detections_queue.add(detections)
                self.fps_queue.add(1/(time.time() - last_time))
                darknet.free_image(last_darknet_image)
            except Exception as e:
                print("Prediction Not Working: Last Image", e)

    def getFPS(self):
        return self.fps_queue.getLast()

    def __init__(self):
        print("Initializing Object Localizer")

        # time.sleep(3)
        threading.Thread(target=self.capture_processing).start()
        time.sleep(3)
        threading.Thread(target=self.detection_starter).start()
