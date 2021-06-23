import threading
from sidewalk_classification.sidewalk_classification import SidewalkClassification as StateClassifier
from turn_classification.turn_classification import TurnClassification as TurnClassifier
from display import Display
import capturer
from person_automobile_sign_detection.detector import Detector as ObjectLocalizer
import person_automobile_sign_detection.intersection_safety_filter as isf
import time
import feedback.output_feedback as feedback
from feedback.audio_player import AudioPlayer

threading.Thread(target=capturer.capturer).start()
time.sleep(1)

sc = StateClassifier()
ol = ObjectLocalizer()
tc = TurnClassifier()
ap = AudioPlayer()

display = Display(dimension=3)
ol.setup_collision_detector(display.getViewerSize(), display.getStretchFactor())
threading.Thread(target=ap.run).start()

counter = 0
while True:
    capture = capturer.getImages().getLast()

    state_classifier_inference = sc.get_inference()
    object_localizer_inference = ol.get_inference()
    print(object_localizer_inference)
    turn_classifier_inference = tc.get_inference()
    print(turn_classifier_inference)
    print("No Moving Vehicles?:" + str(isf.no_moving_vehicles(object_localizer_inference))) # Only useful when person not in movement
    if turn_classifier_inference == "Left Turn" or turn_classifier_inference == "Right Turn":
        state_classifier_inference = "Middle of Sidewalk"
    display.putVideoFrame(capture)
    display.putSidewalkState(state_classifier_inference, turn_classifier_inference)
    display.putObjects(object_localizer_inference)
    display.putState(feedback.interpret_status(state_classifier_inference, turn_classifier_inference, object_localizer_inference))
    display.displayScreen()
    feedback.updateAudioFeedback(state_classifier_inference, turn_classifier_inference, object_localizer_inference)
    counter += 1
