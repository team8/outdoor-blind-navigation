import audio_player
import audio_interpreter

has_started = False

while True:
    if not has_started:
        #all audio cues implemented - stop sign and people, middle, right, left, all prioritized.
        audio_interpreter.create_audio_cue("stop sign", 0, 1, 100, 100)
        audio_interpreter.create_audio_cue("stop sign", 50, 1, 100, 100)
        audio_interpreter.create_audio_cue("stop sign", 100, 1, 100, 100)
        audio_interpreter.create_audio_cue("person", 0, 1, 100, 100)
        audio_interpreter.create_audio_cue("person", 50, 1, 100, 100)
        audio_interpreter.create_audio_cue("person", 100, 1, 100, 100)
        has_started = True
        print(audio_player.audioClips)
    if len(audio_player.audioClips) > 0 and not audio_player.is_playing:
        audio_player.play_first_queue_sound()
    if audio_player.play_object is not None and audio_player.play_object.is_playing():
        audio_player.is_playing = True
    else:
        audio_player.is_playing = False
