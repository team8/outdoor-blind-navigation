import audio_player

has_started = False

while True:
    if not has_started:
        audio_player.add_new_sound("testAudioPython.wav")
        audio_player.add_new_sound("anotheraudioclip.wav")
        audio_player.add_new_sound("yetAnotherAudioClip.wav")
        audio_player.add_new_sound("anotheraudioclip.wav")
        audio_player.add_new_sound("testAudioPython.wav")
        has_started = True
        print(audio_player.audioClips)