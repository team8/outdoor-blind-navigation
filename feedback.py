class Feedback:
    def interpret_inference(self, state_classifier_inference, object_localizer_inference):
        if state_classifier_inference == "Left of Sidewalk":
            print("Playing Shift Right Audio Cue")
            print("Updating Left of Sidewalk Status Cue")
        elif state_classifier_inference == "Right of Sidewalk":
            print("Playing Shift Left Audio Cue")
            print("Updating Right of Sidewalk Status Cue")
        for obstacle in object_localizer_inference:
            if obstacle["label"] == "stop sign":
                print("Stop Sign Detected")
            if obstacle["collision"] == True and obstacle["label"] == "person":
                print("Possible person collision incoming")
            if obstacle["collision"] == True and obstacle["label"] == "car":
                print("Possible car collision incoming")
