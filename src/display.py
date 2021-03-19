import pygame
import cv2
class Display:
    def __init__(self, videoSize=(416,416)):
        pygame.init()
        self.size = (680, 420)
        self.videoSize = videoSize
        self.__image_preprocessing()

    def __image_preprocessing(self):

        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.textSign = self.font.render('stop sign', True, pygame.Color(0, 0, 0), None)
        self.textSignRect = self.textSign.get_rect()
        self.textHuman = self.font.render('person', True,  pygame.Color(0, 0, 0), None)
        self.textHumanRect = self.textHuman.get_rect()
        self.textCar = self.font.render('car', True,  pygame.Color(0, 0, 0),  None)
        self.textCarRect = self.textCar.get_rect()
        self.textBike = self.font.render('bicycle', True,  pygame.Color(0, 0, 0), None)
        self.textBikeRect = self.textBike.get_rect()
        self.textLight = self.font.render('traffic light', True,  pygame.Color(0, 0, 0),  None)
        self.textLightRect = self.textLight.get_rect()
        self.textHydrant = self.font.render('fire hydrant', True,  pygame.Color(0, 0, 0),  None)
        self.textHydrantRect = self.textHydrant.get_rect()
        self.textBench = self.font.render('bench', True,  pygame.Color(0, 0, 0),  None)
        self.textBenchRect = self.textBench.get_rect()
        self.stretchXValue = self.size[0]/self.videoSize[0]
        self.shrinkYValue = self.size[1]/self.videoSize[1]
        self.labelToColor = {"stop sign": ((0, 0, 255),self.textSign, self.textSignRect), "person": ((0,255,0),self.textHuman, self.textHumanRect), "car": ((255, 0, 0),self.textCar, self.textCarRect), "bicycle": ((255, 255, 0),self.textBike, self.textBikeRect), "traffic light": ((255, 0, 255),self.textLight, self.textLightRect), "fire hydrant": ((0, 255, 255),self.textHydrant, self.textHydrantRect), "bench" : ((200, 100, 200),self.textBench, self.textBenchRect)}

        self.screen = pygame.display.set_mode((self.size[0],self.size[1]))
        self.imgLeft = pygame.image.load("./display_resources/Right.png")
        self.imgForward = pygame.image.load("./display_resources/Forward.png")
        self.imgRight = pygame.image.load("./display_resources/Left.png")
        self.screenSizeXConstant = 1575
        self.screenSizeYConstant = 1000
        self.rectVideo = ((0,0,self.size[0],self.size[1]))

        self.imgLeft = self.imgLeft.convert_alpha()
        self.rectLeft = self.imgLeft.get_rect()
        self.rectLeft[2] /= 3
        self.rectLeft[3] /= 3
        self.rectLeft[2] *= self.rectVideo[2] / self.screenSizeXConstant
        self.rectLeft[3] *= self.rectVideo[3] / self.screenSizeYConstant
        self.rectLeft = self.rectLeft.move((self.rectVideo[2] / 2 - self.rectLeft[2] / 2 + self.rectVideo[2]/10, 5 / 10 * self.rectVideo[3]))
        self.imgLeft = pygame.transform.scale(self.imgLeft, (self.rectLeft[2], self.rectLeft[3]))

        self.imgForward = self.imgForward.convert_alpha()
        self.rectForward = self.imgForward.get_rect()
        self.rectForward[2] /= 2
        self.rectForward[3] /= 2
        self.rectForward[2] *= self.rectVideo[2] / self.screenSizeXConstant
        self.rectForward[3] *= self.rectVideo[3] / self.screenSizeYConstant
        self.rectForward = self.rectForward.move((self.rectVideo[2] / 2 - self.rectForward[2]/2, 5/10 * self.rectVideo[3]))
        self.imgForward = pygame.transform.scale(self.imgForward, (self.rectForward[2],self.rectForward[3]))

        self.imgRight = self.imgRight.convert_alpha()
        self.rectRight = self.imgRight.get_rect()
        self.rectRight[2] /= 3
        self.rectRight[3] /= 3
        self.rectRight[2] *= self.rectVideo[2] / self.screenSizeXConstant
        self.rectRight[3] *= self.rectVideo[3] / self.screenSizeYConstant
        self.rectRight = self.rectRight.move((self.rectVideo[2] / 2 - self.rectRight[2] / 2 - self.rectVideo[2]/10, 5 / 10 * self.rectVideo[3]))
        self.imgRight = pygame.transform.scale(self.imgRight, (self.rectRight[2], self.rectRight[3]))
    def putVideoFeed(self,orig_cap):
        orig_cap = cv2.resize(orig_cap, self.size)
        orig_cap = orig_cap.swapaxes(0, 1)
        orig_cap = orig_cap[:, :, ::-1]
        pygame.surfarray.blit_array(self.screen, orig_cap)
    def putSidewalkState(self, state):
        if state == "Left of Sidewalk":
            self.screen.blit(self.imgLeft, self.rectLeft)
        elif state == "Right of Sidewalk":
            self.screen.blit(self.imgRight, self.rectRight)
        elif state == "Middle of Sidewalk":
            self.screen.blit(self.imgForward, self.rectForward)
    def putObjects(self, obstacles):
        if obstacles is None:
            return
        for detection in obstacles:
            #TODO Very temporary - do thresholding within object localizer
            if int(float(detection[1])) >= 25:
                self.__displayObjects(detection)
    def displayScreen(self):
        pygame.display.update();
    def __displayObjects(self, objectInfo):
        x, y, w, h = objectInfo[2]
        x *= self.stretchXValue
        y *= self.shrinkYValue
        w *= self.stretchXValue
        h *= self.shrinkYValue
        empty_rect = pygame.Rect(x-(w/2), y-(h/2), w, h)
        centerX = x
        centerY = y+(h/2)+15
        if (centerY + 15 >= self.size[1]):
            centerY = y-(h/2)-15
        print(self.labelToColor[objectInfo[0]][2])
        textRect = self.labelToColor[objectInfo[0]][2]
        textRect.center = (centerX,centerY)
        self.screen.blit(self.labelToColor[objectInfo[0]][1], textRect)
        pygame.draw.rect(self.screen,self.labelToColor[objectInfo[0]][0], empty_rect, 3)

