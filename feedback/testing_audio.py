import audio_player

has_started = False

while True:
    if not has_started:
        audio_player.add_new_sound("testAudioPython.wav")
        audio_player.add_new_sound("clasppy.wav")
        audio_player.add_new_sound("clikcy tung.wav")
        audio_player.add_new_sound("bigboonk.wav")
        audio_player.add_new_sound("clasppy.wav")
        audio_player.add_new_sound("testAudioPython.wav")
        has_started = True
        print(audio_player.audioClips)
    if len(audio_player.audioClips) > 0 and not audio_player.is_playing:
        audio_player.play_first_queue_sound()
    if audio_player.play_object.is_playing():
        audio_player.is_playing = True
    else:
        audio_player.is_playing = False
