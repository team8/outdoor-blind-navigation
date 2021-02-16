import simpleaudio as sa

audioClipDictionary = {
    "testAudioPython.wav": 1,
    "bigboonk.wav": 2,
    "clikcy tung.wav": 3,
    "clasppy.wav": 4
}

audioClips = []
wave_object = None
play_object = None
is_playing = False


def add_new_sound(clip_name):
    prio = audioClipDictionary.get(clip_name)
    if len(audioClips) >= 1:
        for i in range(0, len(audioClips)):
            if i == len(audioClips) - 1:
                if prio < audioClipDictionary.get(audioClips[i]):
                    audioClips.insert(i, clip_name)
                else:
                    audioClips.append(clip_name)
                break
            else:
                print(str(prio) + " " + clip_name + " " + str(audioClipDictionary.get(audioClips[i])) + " " + audioClips[i])
                if prio < audioClipDictionary.get(audioClips[i]):
                    audioClips.insert(i, clip_name)
                    break
    else:
        audioClips.append(clip_name)


def play_first_queue_sound():
    global wave_object
    wave_object = sa.WaveObject.from_wave_file(audioClips[0])
    global play_object
    play_object = wave_object.play()
    print(play_object.is_playing())
    print(audioClips)
    audioClips.remove(audioClips[0])

