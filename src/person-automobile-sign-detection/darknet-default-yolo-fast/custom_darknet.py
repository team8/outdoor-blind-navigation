from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
from threading import Thread, enumerate
from queue import Queue

video_path = 0 #webcam
weights_path = "./yolov3.weights"
config_path = "./yolov3.cfg"
data_file_path = "./coco.data"

video_capture = cv2.VideoCapture(video_path)
network, class_names, class_colors = darknet.load_network(
            config_path,
            data_file_path,
            weights_path,
            batch_size=1
        )
width = darknet.network_width(network)
height = darknet.network_height(network)

while video_capture.isOpened():
    frame_start_time = time.time()
    frame = video_capture.read()[1]
    preprocessed_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)
    darknet_image = darknet.make_image(width, height, 3)
    darknet.copy_image_from_bytes(darknet_image, preprocessed_frame.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=0.25)
    for detection in detections:
        print(detection)
        x, y, w, h = detection[2]
        xmin = int(round(x - (w / 2)))
        xmax = int(round(x + (w / 2)))
        ymin = int(round(y - (h / 2)))
        ymax = int(round(y + (h / 2)))
        preprocessed_frame = cv2.rectangle(preprocessed_frame, (xmax, ymax), (xmin, ymin), (255, 255, 0), 4)
    print("FPS: " + str(1/(time.time() - frame_start_time)))
    cv2.imshow("Stream", preprocessed_frame)
    cv2.waitKey(1)

