from utils.circularBuffer import CircularBuffer
"""
Class which represents every object detected that is being tracked.
"""

class Detection:
    object_id = -1 # id associated with the object
    label = ""
    bbox = None # detected object position in image
    bbox_history_size = 15
    bbox_history = []
    kalmannFilter = None # kalmann filter object for motion tracking

    consecutiveNotSeenCount = 0 # num of frames it has been that the object has not been detected
    frames_passed = 0 # number of frames passed since first detected
    countSeen = 0 # number of frames object has been seen
    lastSeen = True


    def __init__(self, label=None, object_id=None, bbox=None):
        self.label = label
        self.bbox = bbox
        self.bbox_history = [None]*self.bbox_history_size
        self.bbox_history.insert(0, self.bbox)
        del self.bbox_history[-1]
        self.object_id = object_id

    def update(self, bbox):
        if bbox is not None:
            self.bbox = bbox
            self.bbox_history.insert(0, self.bbox)
            del self.bbox_history[-1]
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
        return True if self.consecutiveNotSeenCount > 4 else False # finish
