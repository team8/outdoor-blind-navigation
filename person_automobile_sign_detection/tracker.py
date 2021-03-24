# import tracker_util as tu
# class Tracker:
#     person_detections = []
#     car_detections = []
#     bicycle_detections = []
#     stop_sign_detections = []
#     street_light_detections = []
#     bench_detections = []
#     _idAssignment = 1
#     def __init__(self, detections):
#         print("Tracker Initialized")
#         self.past_detections = self.current_detections = detections
#
#     def update(self, new_detections): # new_detections is list of Detection objects
#         for person in self.person_detections: #TODO: do this for everything
#             person.lastSeen = False
#         # for detection in new_detections:
#         #     if detection.type = "person":
#         #         person_detections.append(detection)
#         #     elif detection.type = "car":
#         #         car_detections.append(detection)
#         #     elif detection.type = "stopsign":
#         #         stop_sign_detections.append(detection)
#         #     elif detection.type = "bicycle":
#         #         bicycle_detections.append(detection)
#         #     elif detection.type = "streetlight":
#         #         street_light_detections.append(detection)
#         # adjacency_list = []
#         # for new_detection in new_detections:
#         #     if new_detection.type == "person:
#         #         for person in person_detections:
#         #             if tu.compute_iou(person.bbox, new_detection.bbox) > 0.5: # change compute_iou to give overlap percentage from original
#         #                 person.bbox = new_detection.bbox
#         #             else:
#         #                 #TODO: create new detection object and add to the list
#         #
#         # person_indexes_delete = []
#         ''' Delete old detections with certain age
#         for person in self.person_detections:
#         for car in self.car_detections:
#         for bicycle in self.bicycle_detections:
#         for stop_sign in self.stop_sign_detections:
#         for street_light in self.street_light_detections:
#         for bench in self.bench_detections:
#         '''
#         # for person in self.person_detections:
#         #     if self.person_detections.lastSeen:
#         #         self.person_detections.countSeen+=1
#         # for new_detection in new_detections:
#         #     for old_detection in past_detections:
#         #         tu.compute_iou(new_detection.bbox, old_detection.bbox)
# past_detections = []
# current_detections = []
