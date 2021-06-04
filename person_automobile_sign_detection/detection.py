import person_automobile_sign_detection.object_filter_util as ofu
import person_automobile_sign_detection.collision as collision_detector
import display

"""
Class which represents every object detected that is being tracked.
"""

class Detection:
    object_id = -1 # id associated with the object
    label = ""
    bbox = None # detected object position in image
    bbox_history_size = 15
    bbox_history = []
    mdv_history = []
    collision_history = []
    mdv_history_size = 7
    collision_history_size = 3
    kalmannFilter = None # kalmann filter object for motion tracking
    colliding = False
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
        self.mdv_history = [None]*self.mdv_history_size
        self.collision_history = [None]*self.collision_history_size
        self.object_id = object_id

    def update(self, new_bbox):
        self.__updateBBOX(new_bbox)
        self.__updateMDV()
        self.__updateCollision()

    def __updateBBOX(self, bbox):
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

    def __updateMDV(self):
        self.mdv_history.insert(0, ofu.get_direction_vector(self.label, self.bbox_history))
        del self.mdv_history[-1]

    def __updateCollision(self):
        self.collision_history.insert(0, collision_detector.isColliding({"label": self.label, "bbox": self.bbox_history[0], "mdv": self.mdv_history[0]}))
        del self.collision_history[-1]
        if self.colliding == False and self.collision_history.count(True) > len(self.collision_history) * 0.6:
            self.colliding = True
        elif self.colliding == True and self.collision_history.count(True) < len(self.collision_history) * 0.2:
            self.colliding = False

    def evaluateRemove(self) -> bool:
        return True if self.consecutiveNotSeenCount > 4 else False # finish
