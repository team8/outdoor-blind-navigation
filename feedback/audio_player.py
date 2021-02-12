
audioClipDictionary = {
    "testAudioPython.wav": 1,
    "anotheraudioclip.wav": 2,
    "yetAnotherAudioClip.wav": 3
}

audioClips = []


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



