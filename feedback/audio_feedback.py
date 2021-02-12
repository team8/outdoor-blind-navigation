import simpleaudio as sa
import numpy as np


def play_audio_file(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()

    print("e")


#stick with 44100 for the sample_count, as simpleaudio does not support weird sample counts
#seconds is an integer
def play_audio_tone(frequency, sample_count, seconds):
    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, seconds * sample_count, False)

    # Generate a sine wave of the frequency
    note = np.sin(frequency * t * 2 * np.pi)

    # Ensure that highest value is in 16-bit range
    audio = note * (2 ** 15 - 1) / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    # Start playback
    play_obj = sa.play_buffer(audio, 1, 2, sample_count)

    # Wait for playback to finish before exiting
    play_obj.wait_done()
