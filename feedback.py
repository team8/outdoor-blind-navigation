from utils.circularBuffer import CircularBuffer
from feedback import audio_player

def interpret_status(state_classifier_inference, object_localizer_inference):
    status = {"person": False, "stop sign": False, "car": False, "turn left": False, "turn right": False, "shift right": False, "shift left": False, "person collision": False, "car collision": False}
    if state_classifier_inference == "Left of Sidewalk":
        status["shift right"] = True
    elif state_classifier_inference == "Right of Sidewalk":
        status["shift left"] = True
    for obstacle in object_localizer_inference:
        if obstacle["label"] == "stop sign":
            status["stop sign"] = True
        if obstacle["label"] == "person":
            status["person"] = True
            if obstacle["colliding"] == True:
                status["person collision"] = True
        if obstacle["label"] == "car":
            status["car"] = True
            if obstacle["colliding"] == True:
                status["car collision"] = True
    return status

'''
For audio:

Create identifier string using id + label or sidewalk state
Push identifier strings to circular buffer as they come in (making sure only unique identifier strings are on the buffer list
Play each audio queue based on priority queue order and then pop from list
This handles making sure multiple not played at the same time
'''

class AudioFeedback:
    playedAudioClips = [None] * 10
    def update(self, state_classifier_inference, object_localizer_inference):
        for obstacle in object_localizer_inference:
            identifier = obstacle["label"] + " " + obstacle["id"] + " " + obstacle["colliding"]
            if identifier not in self.audioClips.getList():
                self.audioClips.insert(0, identifier)

        if state_classifier_inference == "Left of Sidewalk":
           print("Add shift right to audio queue")
           audio_player.runShiftRight()
        elif state_classifier_inference == "Right of Sidewalk":
           print("Add shift left to audio queue")
           audio_player.runShiftLeft()
        for obstacle in object_localizer_inference:
            if obstacle["label"] == "stop sign":
                audio_player.runStopSignDetected(obstacle["id"])
            if obstacle["label"] == "person":
                if obstacle["colliding"] == True:
                   audio_player.runPersonCollisionDetected(obstacle["id"], obstacle["colliding"])
            if obstacle["label"] == "car":
                if obstacle["colliding"] == True:
                    print("Car collision detected")
                    audio_player.runCarCollisionDetected(obstacle["id"], obstacle["colliding"])


