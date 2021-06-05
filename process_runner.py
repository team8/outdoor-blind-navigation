import threading
from sidewalk_classification.sidewalk_classification import SidewalkClassification as StateClassifier
from display import Display
import capturer
from person_automobile_sign_detection.detector import Detector as ObjectLocalizer
import time
import feedback.output_feedback as feedback
from feedback.audio_player import AudioPlayer

threading.Thread(target=capturer.capturer).start()
time.sleep(1)

sc = StateClassifier()
ol = ObjectLocalizer()
ap = AudioPlayer()
display = Display(dimension=3)
ol.setup_collision_detector(display.getViewerSize(), display.getStretchFactor())
threading.Thread(target=ap.run).start()

counter = 0
while True:
    capture = capturer.getImages().getLast()

    state_classifier_inference = sc.get_inference()
    object_localizer_inference = ol.get_inference()
    # print(state_classifier_inference if counter % 2 == 0 else object_localizer_inference)
    display.putVideoFrame(capture)
    display.putSidewalkState(state_classifier_inference)
    display.putObjects(object_localizer_inference)
    display.putState(feedback.interpret_status(state_classifier_inference, object_localizer_inference))
    display.displayScreen()
    feedback.updateAudioFeedback(state_classifier_inference, object_localizer_inference)
    counter += 1
