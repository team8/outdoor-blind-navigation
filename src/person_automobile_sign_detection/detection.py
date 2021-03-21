"""
Class which represents every object detected that is being tracked.
"""

class Detection:
    object_id = -1 # id associated with the object
    label = ""
    bbox = None # detected object position in image
    kalmannFilter = None # kalmann filter object for motion tracking

    # Lines 13 to 16 should be replaced with circular buffer
    consecutiveNotSeenCount = 0 # num of frames it has been that the object has not been detected
    frames_passed = 0 # number of frames passed since first detected
    countSeen = 0 # number of frames object has been seen
    lastSeen = True


    def __init__(self, object_id, bbox):
        self.bbox = bbox
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
    def seenOrNot(self, is_seen: bool):

        self.frames_passed+=1
        if is_seen:
            self.consecutiveNotSeenCount=0
            self.countSeen+=1
            self.lastSeen = True
        else:
            self.consecutiveNotSeenCount += 1
            self.lastSeen = False
    def evaluateRemove(self) -> bool:
        return True if self.frames_passed > 15 or self.consecutiveNotSeenCount > 4 else False# finish
