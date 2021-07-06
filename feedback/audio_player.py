import simpleaudio as sa
import time
from utils.circularBuffer import CircularBuffer

clipPriority = {"TurnRight": 0, "TurnLeft": 1, "ShiftRight": 2, "ShiftLeft": 3, "Stop": 4, "Person": 5, "Car": 6} # lower value -> higher priority
wantedAudioClips = [] # Have certain clips expire after certain amount of time? 

def runTurnRight():
    if "TurnRight" not in wantedAudioClips:
        wantedAudioClips.append("TurnRight")
        if "ShiftRight" in wantedAudioClips: wantedAudioClips.remove("ShiftRight")
        if "ShiftLeft" in wantedAudioClips: wantedAudioClips.remove("ShiftLeft")

def runTurnLeft():
    if "TurnLeft" not in wantedAudioClips:
        wantedAudioClips.append("TurnLeft")
        if "ShiftRight" in wantedAudioClips: wantedAudioClips.remove("ShiftRight")
        if "ShiftLeft" in wantedAudioClips: wantedAudioClips.remove("ShiftLeft")
def runShiftRight():
    if "ShiftRight" not in wantedAudioClips:
        wantedAudioClips.append("ShiftRight")
def runShiftLeft():
    if "ShiftLeft" not in wantedAudioClips:
        wantedAudioClips.append("ShiftLeft")
def runStopSignDetected(numid):
    if ("Stop" + " " + str(numid)) not in wantedAudioClips:
        wantedAudioClips.append("Stop" + " " + str(numid))
def runPersonCollisionDetected(numid, colliding): #TODO: Make separate for collision from left and right side
    print("Possible Person Collision Detected")
    # if ("Person" + " " + str(numid) + " " + str(colliding)) not in wantedAudioClips:
        # wantedAudioClips.append("Person" + " " + str(numid) + " " + str(colliding))
def runCarCollisionDetected(numid, colliding):
    print("Possible Car Collision Detected")
    # if ("Car" + " " + str(numid) + " " + str(colliding)) not in wantedAudioClips:
        # wantedAudioClips.append("Car" + " " + str(numid) + " " + str(colliding))

class AudioPlayer:
    def run(self):
        playedAudioClipsSize = 5
        playedAudioClips = CircularBuffer(playedAudioClipsSize)
        timeTillPlayedAudioClipDelete = 10  # x seconds till a played audio clip is removed off of do-not-play list
        while True:
            try:
                # print("Running AudioPlayer")
                global wantedAudioClips
                # print("Wanted " + str(wantedAudioClips))
                print(playedAudioClips.getList())
                highestPriorityString = None
                highestPriorityIndex = None
                # Find clip with the highest priority
                for clip in wantedAudioClips:
                    currentClipPriority = clipPriority[clip.split()[0]]
                    playedAudioClipsList = list(filter(None, playedAudioClips.getList()))
                    if (highestPriorityIndex is None or currentClipPriority < highestPriorityIndex) and sum(map(lambda obstacle : obstacle[0] == clip, playedAudioClipsList)) == 0:
                        highestPriorityIndex = currentClipPriority
                        highestPriorityString = clip
                if highestPriorityString is not None:
                    playedAudioClips.add((highestPriorityString,int(time.time())))
                    wantedAudioClips.remove(highestPriorityString)
                    self.__play(highestPriorityString)
                time.sleep(1)
                currentTime = int(time.time())
                for clip_index in range(0, len(playedAudioClips.getList())):
                    if playedAudioClips.getList()[clip_index] != None:
                        if (currentTime - playedAudioClips.getList()[clip_index][1]) > timeTillPlayedAudioClipDelete:
                            playedAudioClips.replace_index(None, clip_index)
            except Exception as e:
                print(e)

    def __play(self, audio_string):
        # Play audio string based on identifier string
        print("Playing " + audio_string)
        wave_obj = None
        audio_params = audio_string.split()


        if audio_params[0] == "TurnLeft":
            wave_obj = sa.WaveObject.from_wave_file("assets/LeftTurnAudio.wav")
        elif audio_params[0] == "TurnRight":
            wave_obj = sa.WaveObject.from_wave_file("assets/RightTurnAudio.wav")
        elif audio_params[0] == "ShiftLeft":
            wave_obj = sa.WaveObject.from_wave_file("assets/ShiftLeftAudio.wav")
        elif audio_params[0] == "ShiftRight":
            wave_obj = sa.WaveObject.from_wave_file("assets/ShiftRightAudio.wav")
        elif audio_params[0] == "Stop":
            wave_obj = sa.WaveObject.from_wave_file("assets/StopSignAudio.wav")
        elif audio_params[0] == "Person" and audio_params[2] == "True":
            wave_obj = sa.WaveObject.from_wave_file("assets/PersonCollisionDetectedAudio.wav")
        elif audio_params[0] == "Car" and audio_params[2] == "True":
            wave_obj = sa.WaveObject.from_wave_file("assets/CarCollisionDetectedAudio.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()
        # Exit once full audio clip has been played


