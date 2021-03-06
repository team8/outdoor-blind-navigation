from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
import threading
from utils.circularBuffer import CircularBuffer
class Detector:
    video_path = 0 #webcam
    weights_path = "./yolov4.weights"
    config_path = "./yolov4.cfg"
    data_file_path = "./coco.data"

    video_capture = cv2.VideoCapture(video_path)
    network, class_names, class_colors = darknet.load_network(
                config_path,
                data_file_path,
                weights_path,
                batch_size=1
            )
    detections_queue = []
    images_queue = []
    fps_queue = [0]
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    colors = {"person": [255, 255, 0], "car": [100, 0, 0], "stopsign": [100, 100, 0]}
    detections_average = CircularBuffer(5)

    def capture_processing(self):
        while True:
            try:
                frame = video_capture.read()[1]
                preprocessed_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)
                darknet_image = darknet.make_image(width, height, 3)
                darknet.copy_image_from_bytes(darknet_image, preprocessed_frame.tobytes())
                images_queue.append((darknet_image, preprocessed_frame))
            except Exception as e:
                print(e)

    def display(self):
        while True:
            try:
                last_detection = detections_queue[-1]
                last_image = images_queue[-1][1]
                fps = fps_queue[-1]
                for detection in last_detection:
                    # print(detection)
                    x, y, w, h = detection[2]
                    xmin = int(x - (w / 2))
                    xmax = int(x + (w / 2))
                    ymin = int(y - (h / 2))
                    ymax = int(y + (h / 2))
                    detections_average.add([xmax, ymax, xmin, ymin]) #this is wrong - should only do this for individual objects. this is just merging everything together (very bad)
                    detections_mean = detections_average.mean()

                    print(detection[0] + " FPS: " + str(fps))
                    if detections_mean is not None:
                        display_image = cv2.rectangle(last_image, (int(detections_mean[0]), int(detections_mean[1])), (int(detections_mean[2]), int(detections_mean[3])), colors[detection[0]] if detection[0] in colors else [0, 100, 0], 4)
                cv2.imshow("Stream", display_image)
                cv2.waitKey(1)

                # print("FPS: " + str(1/(time.time() - frame_start_time)))
            except Exception as e:
                    print(e)

    def get_inference(self):
        return {"label": detections_queue[-1][0], "bbox": detections_queue[-1][1]} if len(detections_queue) >= 1 else None

    def detection_updater(self):
        while video_capture.isOpened():
            threading.Thread(target=capture_processing).start()
            threading.Thread(target=display).start()

            while True:
                try:
                    last_darknet_image = images_queue[-1][0]
                    last_time = time.time()
                    detections = darknet.detect_image(network, class_names, last_darknet_image, thresh=0.25)
                    detections_queue.append(detections)

                    fps_queue.append(1/(time.time() - last_time))
                except Exception as e:
                    print(e)

