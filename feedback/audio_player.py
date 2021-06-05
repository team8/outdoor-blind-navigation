import simpleaudio as sa
from utils.circularBuffer import CircularBuffer

clipPriority = {"ShiftRight": 0, "ShiftLeft": 1, "Stop": 2, "Person": 3, "Car": 4} # lower value -> higher priority
wantedAudioClips = []

def runShiftRight():
    wantedAudioClips.append("ShiftRight")
def runShiftLeft():
    wantedAudioClips.append("ShiftLeft")
def runStopSignDetected(numid):
    wantedAudioClips.append("Stop" + " " + str(numid))
def runPersonCollisionDetected(numid, colliding): #TODO: Make separate for collision from left and right side
    wantedAudioClips.append("Person" + " " + str(numid) + " " + str(colliding))
def runCarCollisionDetected(numid, colliding):
    wantedAudioClips.append("Car" + " " + str(numid) + " " + str(colliding))

class AudioPlayer:
    playedAudioClips = CircularBuffer(15)
    def update(self):
        global wantedAudioClips
        highestPriorityString = None
        highestPriorityIndex = None
        # Find clip with the highest priority
        for clip in wantedAudioClips:
            currentClipPriority = clipPriority[clip.split()[0]]
            if (highestPriorityIndex is None or currentClipPriority < highestPriorityIndex) and highestPriorityString not in self.playedAudioClips.getList():
                highestPriorityIndex = currentClipPriority
                highestPriorityString = clip
        if highestPriorityString is not None:
            self.playedAudioClips.add(highestPriorityString)
            self.__play(highestPriorityString)

    def __play(self, audio_string):
        # Play audio string based on identifier string
        print("Playing " + audio_string)
        wave_obj = None
        audio_params = audio_string.split()
        if audio_params[0] == "ShiftLeft":
            wave_obj = sa.WaveObject.from_wave_file("../assets/ShiftLeftAudio.wav")
        elif audio_params[0] == "ShiftRight":
            wave_obj = sa.WaveObject.from_wave_file("../assets/ShiftRightAudio.wav")
        elif audio_params[0] == "Stop":
            wave_obj = sa.WaveObject.from_wave_file("../assets/StopSignAudio.wav")
        elif audio_params[0] == "Person" and audio_params[2] == "True":
            wave_obj = sa.WaveObject.from_wave_file("../assets/PersonCollisionDetectedAudio.wav")
        elif audio_params[0] == "Car" and audio_params[2] == "True":
            wave_obj = sa.WaveObject.from_wave_file("../assets/CarCollisionDetectedAudio.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()

        # Exit once full audio clip has been played






































# audioClipDictionary = {
#     "personahead.wav": 1,
#     "personleft.wav": 2,
#     "personright.wav": 3,
#     "stopsignmiddle.wav": 4,
#     "stopsignleft.wav": 5,
#     "stopsignright.wav": 6,
# }
#
# audioClips = []
# wave_object = None
# play_object = None
# is_playing = False
#
#
# def add_new_sound(clip_name):
#     prio = audioClipDictionary.get(clip_name)
#     if len(audioClips) >= 1:
#         for i in range(0, len(audioClips)):
#             if i == len(audioClips) - 1:
#                 if prio < audioClipDictionary.get(audioClips[i]):
#                     audioClips.insert(i, clip_name)
#                 else:
#                     audioClips.append(clip_name)
#                 break
#             else:
#                 print(str(prio) + " " + clip_name + " " + str(audioClipDictionary.get(audioClips[i])) + " " + audioClips[i])
#                 if prio < audioClipDictionary.get(audioClips[i]):
#                     audioClips.insert(i, clip_name)
#                     break
#     else:
#         audioClips.append(clip_name)
#
#
# def play_first_queue_sound():
#     global wave_object
#     wave_object = sa.WaveObject.from_wave_file(audioClips[0])
#     global play_object
#     play_object = wave_object.play()
#     print(play_object.is_playing())
#     print(audioClips)
#     audioClips.remove(audioClips[0])
#
