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
    frame = video_capture.read()[1]
    # img_for_detect = darknet.make_image(width, height, 3)
    # darknet.copy_image_from_bytes(img_for_detect, cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR).tobytes())

    preprocessed_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)
    darknet_image = darknet.make_image(width, height, 3)
    darknet.copy_image_from_bytes(darknet_image, preprocessed_frame.tobytes())
    print(darknet_image)
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=0.25)
    for detection in detections:
        print(detection)
        preprocessed_frame = cv2.rectangle(preprocessed_frame, (int(detection[2][0]), int(detection[2][1])), (int(detection[2][2]), int(detection[2][3])), (255, 255, 0), 4)
    cv2.imshow("Stream", preprocessed_frame)
    cv2.waitKey(1)

