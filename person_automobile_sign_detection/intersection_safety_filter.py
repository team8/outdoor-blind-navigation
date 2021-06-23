import math

def no_moving_vehicles(object_localizer_inference) -> bool:
    no_movement_mdv_max_length = 3
    for obstacle in object_localizer_inference:
        if obstacle["label"] == "car" or obstacle["label"] == "bicycle":
            mdv_length = math.sqrt(obstacle["mdv"][0]**2 + obstacle["mdv"][1]**2 + obstacle["mdv"][2]**2)
            if mdv_length > no_movement_mdv_max_length:
                return False
    return True # if cars mdv is less than threshold, than no movement or little movement
