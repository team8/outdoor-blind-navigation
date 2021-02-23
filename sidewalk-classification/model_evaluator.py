import sys

import cv2
import pygame
import tensorflow as tf
import numpy as np
import time
from utils.circularBuffer import CircularBuffer
from utils.display.sidewalk_display import start_display, initPics

classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk']
model = tf.keras.models.load_model("sidewalk_classification_model100.h5")
vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk.mp4")
cb = CircularBuffer(15)
state = ""
cb.initQueue([0, 0, 0])
pygame.init()
pics = initPics(vid.read()[1])
imgLeft = pics[0]
imgForward = pics[1]
imgRight = pics[2]
screen = pics[3]
while True:
    start_time = time.time()
    orig_cap = vid.read()[1]
    cap = cv2.resize(orig_cap, (100, 100))
    raw_prediction = (model.predict(np.expand_dims(cap, 0))).tolist()[0]
    cb.add(None if max(raw_prediction) < 0.9 else raw_prediction)
    averaged_prediction = cb.mean()
    if averaged_prediction is None:
        state = "Nothing detected"
    else:
        state = classes[np.argmax(averaged_prediction)]
    end_time = time.time()
    confidence =  np.argmax(averaged_prediction) * 100 // 1 if averaged_prediction is not None else None
    print("FPS:", 1/ (end_time - start_time), state, "Confidence:", confidence)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
    orig_cap = orig_cap.swapaxes(0, 1)
    orig_cap = orig_cap[:, :, ::-1]
    img2 = pygame.surfarray.make_surface(orig_cap)
    img2 = img2.convert()
    rect2 = img2.get_rect()
    if (rect2[2] > 1920):
        rect2[3] *= 1920 / rect2[2]
        rect2[2] *= 1920 / rect2[2]
    if (rect2[3] > 1000):
        rect2[2] *= 1000 / rect2[3]
        rect2[3] *= 1000 / rect2[3]
    img2 = pygame.transform.scale(img2, (rect2[2], rect2[3]))
    screen.blit(img2, rect2)
    if state == "Left of Sidewalk":
        screen = start_display(rect2, screen, imgLeft, -1)
    if state == "Right of Sidewalk":
        screen = start_display(rect2, screen, imgRight, 1)
    if state == "Middle of Sidewalk":
        screen = start_display(rect2, screen, imgForward, 0)
    pygame.display.flip()
    pygame.display.update()

