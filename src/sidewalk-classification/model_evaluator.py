import sys

import cv2
import pygame
import tensorflow as tf
import numpy as np
import time
from utils.circularBuffer import CircularBuffer
from utils.display.sidewalk_display import  initPics
class Display:
    def __init__(self):
        pygame.init()
        self.pics = initPics(capture)
        self.imgLeft = self.pics[0]
        self.rect1 = self.pics[1]
        self.imgLeft = pygame.transform.scale(self.imgLeft, (self.rect1[2], self.rect1[3]))
        self.imgForward = self.pics[2]
        self.rect3 = self.pics[3]
        self.imgForward = pygame.transform.scale(self.imgForward, (self.rect3[2], self.rect3[3]))
        self.imgRight = self.pics[4]
        self.rect4 = self.pics[5]
        self.imgRight = pygame.transform.scale(self.imgRight, (self.rect4[2], self.rect4[3]))
        self.screen = self.pics[6]
    def update(self, state,orig_cap):
        orig_cap = orig_cap.swapaxes(0, 1)
        orig_cap = orig_cap[:, :, ::-1]
        self.img2 = pygame.surfarray.make_surface(orig_cap)
        self.img2 = self.img2.convert()
        self.rect2 = self.img2.get_rect()
        self.screen.blit(self.img2, self.rect2)
        if state == "Left of Sidewalk":
            self.screen.blit(self.imgLeft, self.rect1)
        if state == "Right of Sidewalk":
            self.screen.blit(self.imgRight, self.rect4)
        if state == "Middle of Sidewalk":
            self.screen.blit(self.imgForward, self.rect3)
        pygame.display.flip()
        pygame.display.update()

classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk']
model = tf.keras.models.load_model("sidewalk_classification_model_resnet.h5")
# vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk.mp4")
rotate = False
vid = cv2.VideoCapture(0)
sidewalk_display = Display()
time.sleep(3)
capture = vid.read()
print(capture[0])
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
    sidewalk_display.update(state, orig_cap)
