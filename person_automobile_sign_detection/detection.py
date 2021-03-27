from utils.circularBuffer import CircularBuffer
"""
Class which represents every object detected that is being tracked.
"""

class Detection:
    object_id = -1 # id associated with the object
    label = ""
    bbox = None # detected object position in image
    bbox_history_size = 15 
    bbox_history = CircularBuffer(bbox_history_size)
    kalmannFilter = None # kalmann filter object for motion tracking

    # Lines 13 to 16 should be replaced with circular buffer
    consecutiveNotSeenCount = 0 # num of frames it has been that the object has not been detected
    frames_passed = 0 # number of frames passed since first detected
    countSeen = 0 # number of frames object has been seen
    lastSeen = True


    def __init__(self, label, object_id, bbox):
        self.label = label
        self.bbox = bbox
        self.bbox_history.initQueue([None]*self.bbox_history_size)
        self.bbox_history.add(self.bbox)
        self.object_id = object_id
        # self.kalmannFilter = KalmannFilter()

    # def update(self, seen: bool):
    #     self.frames_passed+=1;
    #     self.countSeen = self.countSeen + 1 if seen is True else self.countSeen
    #     if seen is False and self.lastSeen is False:
    #         self.consecutiveNotSeenCount += 1
    #     else:
    #         self.consecutiveNotSeenCount = 0
    #     self.lastSeen = seen
    #
    # def getPosition(self):
        # return kalmannFilter.predict()
    def update(self, bbox):
        if bbox is not None:
            self.bbox = bbox
            self.bbox_history.add(self.bbox)
            is_seen = True
        else:
            is_seen = False

        self.frames_passed+=1
        if is_seen:
            self.consecutiveNotSeenCount=0
            self.countSeen+=1
            self.lastSeen = True
        else:
            self.consecutiveNotSeenCount += 1
            self.lastSeen = False
    def evaluateRemove(self) -> bool:
        return True if self.consecutiveNotSeenCount > 6 else False # finish
