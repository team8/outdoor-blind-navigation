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
from person_automobile_sign_detection.detection import Detection
import person_automobile_sign_detection.object_filter_util as ofu

class Detector:
    weights_path = "person_automobile_sign_detection/yolov4.weights"
    # weights_path = "person_automobile_sign_detection/yolov4.weights"
    config_path = "person_automobile_sign_detection/yolov4-original.cfg"
    # config_path = "person_automobile_sign_detection/yolov4-original.cfg"
    data_file_path = "person_automobile_sign_detection/coco_original.data"
    # data_file_path = "person_automobile_sign_detection/coco.data"

    network, class_names, class_colors = darknet.load_network(
                config_path,
                data_file_path,
                weights_path,
                batch_size=1
            )
    running_detections = []
    images_queue = Queue(maxsize=2)
    # images_queue = Queue()
    # fps_queue = Queue(maxsize=3)
    fps_queue = CircularBuffer(1)
    width = darknet.network_width(network)
    min_confidence = 25
    min_iou = 25 # min iou percentage for id'ing
    min_box_area = 300
    id_index = 0 # keeps raising per new object identified
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

    #     while True:
    #         try:
    #             last_image = self.images_queue.get()[1]
    #             fps = self.fps_queue.getLast()
    #             for detection in last_detection:
    #                 # print(detection)
    #                 x, y, w, h = detection[2]
    #                 xmin = int(x - (w / 2))
    #                 xmax = int(x + (w / 2))
    #                 ymin = int(y - (h / 2))
    #                 ymax = int(y + (h / 2))
    #                 # detections_average.add([xmax, ymax, xmin, ymin]) #this is wrong - should only do this for individual objects. this is just merging everything together (very bad)
    #                 # detections_mean = detections_average.mean()
    #
    #                 # print(detection[0] + " FPS: " + str(fps))
    #                 display_image = cv2.rectangle(last_image, (xmax, ymax), (xmin, ymin), self.colors[detection[0]] if detection[0] in self.colors else [0, 100, 0], 4)
    #             cv2.imshow("Stream", display_image)
    #             cv2.waitKey(1)
    #
    #             # print("FPS: " + str(1/(time.time() - frame_start_time)))
    #         except Exception as e:
    #                 print("Displaying Not Working", e)
    #
    def get_inference(self):
        inference = []

        for detection in self.running_detections:
            if detection.countSeen >= 7:
                inference.append((detection.label, 0, detection.bbox, ofu.get_direction_vector(detection.bbox_history.getList())))
                # inference.append((detection.label, 0, detection.bbox, detection.object_id))
                # print(detection.bbox.getLast())
        '''
        Each element in the list is a separate detection
        (label, confidence[notneeded], bbox, direction_vector, object_id)
        '''
        # print(inference)
        return inference

        # return self.detections_queue.getLast()

    def detection_starter(self):
        # threading.Thread(target=self.display).start()
        while True:
            # try:
                # while self.images_queue.get()[0] is None: time.sleep(0.1);

            last_darknet_image = self.images_queue.get()[0]
            last_time = time.time()
            detections = darknet.detect_image(self.network, self.class_names, last_darknet_image, thresh=0.35)

            self.update_running_detections(detections)
            self.fps_queue.add(1/(time.time() - last_time))
            darknet.free_image(last_darknet_image)
            # except Exception as e:
                # print("Prediction Not Working: Last Image", e)


    def update_running_detections(self, raw_detections_list):
        idSeen = []
        for raw_detection in raw_detections_list:
            # print(raw_detection)
            if float(raw_detection[1]) > self.min_confidence and raw_detection[2][2] * raw_detection[2][3] > self.min_box_area:
                found_match = False
                largest_iou_ID = -1
                largest_iou = self.min_iou

                print("Number of running detections:", str(len(self.running_detections)))
                for detection_index in range(0, len(self.running_detections)):
                    print(self.running_detections[detection_index].toString())
                    print(ofu.compute_iou(self.running_detections[detection_index].bbox, raw_detection[2]))
                    if raw_detection[0] == self.running_detections[detection_index].label:
                        # print(raw_detection[2])
                        # print(self.running_detections[detection_index].bbox.getLast())
                        # exit()
                        iou = ofu.compute_iou(self.running_detections[detection_index].bbox.getLast(), raw_detection[2])
                        print("iou", iou)
                        if iou > largest_iou:
                            largest_iou_ID = detection_index
                            largest_iou = iou
                            found_match = True
                print("Done cycling through all running detections")
                if found_match is True:
                    print("Largest iou", largest_iou, "largest iou intersection check", ofu.compute_iou(self.running_detections[largest_iou_ID].bbox, raw_detection[2]))
                    self.running_detections[largest_iou_ID].update(raw_detection[2])
                    idSeen.append(largest_iou)
                    print("Associated BB", raw_detection[0], "ID: ", self.running_detections[largest_iou_ID].object_id)
                else:
                    # print("Adding new detection", raw_detection[0])
                    self.id_index += 1
                    self.running_detections.append(Detection(raw_detection[0], self.id_index, raw_detection[2]))

        indexToDelete = []
        # for detection in self.running_detections:
        for i in range(0, len(self.running_detections)):
            # print("Seen", self.running_detections[i].label, self.running_detections[i].countSeen, "times")
            if self.running_detections[i].object_id not in idSeen:
                self.running_detections[i].update(None)
            if self.running_detections[i].evaluateRemove():
                indexToDelete.append(i)
        print("Index Count", len(indexToDelete))
        print("Indexes to Delete", indexToDelete)
        print("Running Detections size", len(self.running_detections))
        self.running_detections = [i for j, i in enumerate(self.running_detections) if j not in indexToDelete]
        # for i in indexToDelete:
            # del self.running_detections[i]
        # print(self.running_detections)
        # input("press enter to continue")


    def getFPS(self):
        return self.fps_queue.getLast()
    def __init__(self):
        print("Initializing Object Localizer")

        # time.sleep(3)
        threading.Thread(target=self.capture_processing).start()
        time.sleep(3)
        threading.Thread(target=self.detection_starter).start()
