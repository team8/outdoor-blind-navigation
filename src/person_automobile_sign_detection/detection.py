"""
Class which represents every object detected that is being tracked.
"""

class Detection:
    id = -1 # id associated with the object
    bbox = None # detected object position in image
    kalmannFilter = None # kalmann filter object for motion tracking

    # Lines 13 to 16 should be replaced with circular buffer
    consecutiveNotSeenCount = 0 # num of frames it has been that the object has not been detected
    frames_passed = 0 # number of frames passed since first detected
    countSeen = 0 # number of frames object has been seen
    lastSeen = True


    def __init__(self, id, bbox):
        self.bbox = bbox
        self.id = id
        # self.kalmannFilter = KalmannFilter()

    def update(self, seen: bool):
        self.frames_passed+=1;
        self.countSeen = self.countSeen + 1 if seen is True else self.countSeen
        if seen is False and self.lastSeen is False:
            self.consecutiveNotSeenCount += 1
        else:
            self.consecutiveNotSeenCount = 0
        self.lastSeen = seen

    # def getPosition(self):
        # return kalmannFilter.predict()

    def evaluateStatus(self) -> bool:
        return True if self.frames_passed > 7 or self.consecutiveNotSeenCount > 8 # finish
