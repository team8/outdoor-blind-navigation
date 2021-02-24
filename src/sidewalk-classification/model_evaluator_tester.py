import sys
import cv2
import pygame

from utils.display.sidewalk_display import  initPics
class Display:
    def __init__(self):
        self.a =1
    def initiallize(self, capture):
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
        if (self.rect2[2] > 1920):
            self.rect2[3] *= 1920 / self.rect2[2]
            self.rect2[2] *= 1920 / self.rect2[2]
        if (self.rect2[3] > 1000):
            self.rect2[2] *= 1000 / self.rect2[3]
            self.rect2[3] *= 1000 / self.rect2[3]
        self.img2 = pygame.transform.scale(self.img2, (self.rect2[2], self.rect2[3]))
        self.screen.blit(self.img2, self.rect2)
        if state == "Left of Sidewalk":
            self.screen.blit(self.imgLeft, self.rect1)
        if state == "Right of Sidewalk":
            self.screen.blit(self.imgRight, self.rect4)
        if state == "Middle of Sidewalk":
            self.screen.blit(self.imgForward, self.rect3)
        pygame.display.flip()
        pygame.display.update()
my_display = Display()
classes = ['Left of Sidewalk', 'Middle of Sidewalk', 'Right of Sidewalk']
vid = cv2.VideoCapture(0)
capture = vid.read()[1]
my_display.initiallize(capture)
state = ""
while True:
    orig_cap = vid.read()[1]
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_d):
                state = "Right of Sidewalk"
            if (event.key == pygame.K_a):
                state = "Left of Sidewalk"
            if (event.key == pygame.K_w):
                state = "Middle of Sidewalk"
    my_display.update(state,orig_cap)
