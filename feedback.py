def interpret_status(state_classifier_inference, object_localizer_inference):
    status = {
        "person": False,
        "stop sign": False,
        "car": False,
        "turn left": False,
        "turn right": False,
        "shift right": False,
        "shift left": False,
        "person collision": False,
        "car collision": False}
    if state_classifier_inference == "Left of Sidewalk":
        status["shift right"] = True
    elif state_classifier_inference == "Right of Sidewalk":
        status["shift left"] = True
    for obstacle in object_localizer_inference:
        if obstacle["label"] == "stop sign":
            status["stop sign"] = True
        if obstacle["label"] == "person":
            status["person"] = True
            if obstacle["colliding"]:
                status["person collision"] = True
        if obstacle["label"] == "car":
            status["car"] = True
            if obstacle["colliding"]:
                status["car collision"] = True
    return status
