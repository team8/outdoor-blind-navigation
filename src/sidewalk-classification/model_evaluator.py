import sys

import cv2
import pygame
import tensorflow as tf
import numpy as np
import time
from utils.circularBuffer import CircularBuffer

classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk']
model = tf.keras.models.load_model("sidewalk_classification_model_resnet.h5")
# vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk.mp4")
rotate = False
vid = cv2.VideoCapture(0)
time.sleep(3)
print(vid.read()[0])
if vid.read()[0] is False:
    vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk.mp4")
    rotate = True
    position_video = 0.2
    vid.set(cv2.CAP_PROP_POS_FRAMES, (position_video * vid.get(cv2.CAP_PROP_FRAME_COUNT)))


cb = CircularBuffer(15)
state = ""
cb.initQueue([0, 0, 0])
while True:
    start_time = time.time()
    orig_cap = cv2.resize(cv2.rotate(vid.read()[1], cv2.ROTATE_90_COUNTERCLOCKWISE) if rotate == True else vid.read()[1], (480, 360))
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
    cv2.waitKey(1)
    pygame.init()
    screen = pygame.display.set_mode((1920, 1050))
    varx = 1575
    vary = 1000
    events = pygame.event.get()
    direction = 0
    if state == "Nothing detected":
        direction = -1
    if state == "Left of Sidewalk":
        direction = 1
    if state == "Middle of Sidewalk":
        direction = 2
    if state == "Right of Sidewalk":
        direction = 0
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                direction = 1
            if event.key == pygame.K_a:
                direction = 0
            if event.key == pygame.K_w:
                direction = 2
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
    screen = pygame.display.set_mode((rect2[2], rect2[3]))
    screen.blit(img2, rect2)
    if direction == 0:
        img = pygame.image.load("../../utils/display/Right6.png")
        img = img.convert_alpha()
        rect = img.get_rect()
        rect[2] /= 3
        rect[3] /= 3
        rect[2] *= rect2[2] / varx
        rect[3] *= rect2[3] / vary
        img = pygame.transform.scale(img, (rect[2], rect[3]))
        rect = rect.move((rect2[2] / 2 - rect[2] / 2, 5 / 10 * rect2[3]))
        screen.blit(img, rect)
    if direction == 1:
        img = pygame.image.load("../../utils/display/Right5.png")
        img = img.convert_alpha()
        rect = img.get_rect()
        rect[2] /= 3
        rect[3] /= 3
        rect[2] *= rect2[2] / varx
        rect[3] *= rect2[3] / vary
        img = pygame.transform.scale(img, (rect[2], rect[3]))
        rect = rect.move((rect2[2] / 2 - rect[2] / 2, 5 / 10 * rect2[3]))
        screen.blit(img, rect)
    if direction == 2:
        img = pygame.image.load("../../utils/display/UpMe2.png")
        img = img.convert_alpha()
        rect = img.get_rect()
        rect[2] /= 2
        rect[3] /= 2
        rect[2] *= rect2[2] / varx
        rect[3] *= rect2[3] / vary
        img = pygame.transform.scale(img, (rect[2], rect[3]))
        rect = rect.move((rect2[2] / 2 - rect[2] / 2, 5 / 10 * rect2[3]))
        screen.blit(img, rect)
    pygame.display.flip()
    cv2.waitKey(1)
