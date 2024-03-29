import audio_player
import math


def create_audio_cue(object_name, object_pixel_x, object_pixel_y, image_width, image_height):
    quadrant_width = image_width/3
    quadrant_height = image_height/3
    pixel_quadrant_x = math.floor((object_pixel_x/image_width) * 3)
    pixel_quadrant_y = math.floor((object_pixel_y/image_height) * 3)
    if pixel_quadrant_x >= 3:
        pixel_quadrant_x = 2
    if pixel_quadrant_y >= 3:
        pixel_quadrant_y = 2
    if pixel_quadrant_x <= 0:
        pixel_quadrant_x = 0
    if pixel_quadrant_y <= 0:
        pixel_quadrant_y = 0

    if object_name == "stop sign":
        if pixel_quadrant_x == 0:
            audio_player.add_new_sound("stopsignleft.wav")
        if pixel_quadrant_x == 1:
            audio_player.add_new_sound("stopsignmiddle.wav")
        if pixel_quadrant_x == 2:
            audio_player.add_new_sound("stopsignright.wav")
    elif object_name == "person":
        if pixel_quadrant_x == 0:
            audio_player.add_new_sound("personleft.wav")
        if pixel_quadrant_x == 1:
            audio_player.add_new_sound("personahead.wav")
        if pixel_quadrant_x == 2:
            audio_player.add_new_sound("personright.wav")

    print(str(pixel_quadrant_x) + " " + str(pixel_quadrant_y))
