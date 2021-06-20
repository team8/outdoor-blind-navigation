from utils.circularBuffer import CircularBuffer
import feedback.audio_player as audio_player

def interpret_status(state_classifier_inference, turn_classifier_inference, object_localizer_inference):
    status = {"person": False, "stop sign": False, "car": False, "turn left": False, "no turn": False, "turn right": False, "shift right": False, "shift left": False, "person collision": False, "car collision": False}
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
    if turn_classifier_inference == "Right Turn":
        status["turn right"] = True
    elif turn_classifier_inference == "Left Turn":
        status["turn left"] = True
    else:
        status["no turn"] = True
    return status

def updateAudioFeedback(state_classifier_inference, turn_classifier_inference, object_localizer_inference):
    if turn_classifier_inference == "Left Turn":
        audio_player.runTurnLeft()
    if turn_classifier_inference == "Right Turn":
        audio_player.runTurnRight()
    if state_classifier_inference == "Left of Sidewalk":
       audio_player.runShiftRight()
    elif state_classifier_inference == "Right of Sidewalk":
       audio_player.runShiftLeft()
    for obstacle in object_localizer_inference:
        if obstacle["label"] == "stop sign":
            audio_player.runStopSignDetected(obstacle["id"])
        if obstacle["label"] == "person":
            if obstacle["colliding"] == True:
               audio_player.runPersonCollisionDetected(obstacle["id"], obstacle["colliding"])
        if obstacle["label"] == "car":
            if obstacle["colliding"] == True:
                audio_player.runCarCollisionDetected(obstacle["id"], obstacle["colliding"])


