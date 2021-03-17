import pygame
class Display:
    def __init__(self,size):
        pygame.init()
        self.__image_preprocessing(size)

    def __image_preprocessing(self,size):

        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.textSign = self.font.render('Stop Sign', True, (0, 0, 255), None)
        self.textSignRect = self.textSign.get_rect()
        self.textHuman = self.font.render('Person', True, (0,255,0), None)
        self.textHumanRect = self.textHuman.get_rect()
        self.textCar = self.font.render('Car', True, (255, 0, 0), None)
        self.textCarRect = self.textCar.get_rect()
        self.textBike = self.font.render('Bike', True, (255, 255, 0), None)
        self.textBikeRect = self.textBike.get_rect()
        self.textLight = self.font.render('Traffic Light', True, (255, 0, 255), None)
        self.textLightRect = self.textLight.get_rect()
        self.textHydrant = self.font.render('Fire Hydrant', True, (0, 255, 255), None)
        self.textHydrantRect = self.textHydrant.get_rect()
        self.textBench = self.font.render('Bench', True, (200, 100, 200), None)
        self.textBenchRect = self.textBench.get_rect()
        self.Hashmap = {"Stop Sign" : 1, "Person" : 2, "Car" : 3, "Bike" : 4, "Traffic Light" : 5, "Fire Hydrant": 6, "Bench" : 7}

        self.screen = pygame.display.set_mode((size[0],size[1]))
        self.imgLeft = pygame.image.load("D:/Maxwell/SpecialRobotStuff/blind-navigation/src/display-resources/Right.png")
        self.imgForward = pygame.image.load("D:/Maxwell/SpecialRobotStuff/blind-navigation/src/display-resources/Forward.png")
        self.imgRight = pygame.image.load("D:/Maxwell/SpecialRobotStuff/blind-navigation/src/display-resources/Left.png")
        self.screenSizeXConstant = 1575
        self.screenSizeYConstant = 1000
        self.rectVideo = ((0,0,size[0],size[1]))

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
    def update(self,state, orig_cap, obstacles):
        orig_cap = orig_cap.swapaxes(0, 1)
        orig_cap = orig_cap[:, :, ::-1]
        pygame.surfarray.blit_array(self.screen, orig_cap)
        if state == "Left of Sidewalk":
            self.screen.blit(self.imgLeft, self.rectLeft)
        elif state == "Right of Sidewalk":
            self.screen.blit(self.imgRight, self.rectRight)
        elif state == "Middle of Sidewalk":
            self.screen.blit(self.imgForward, self.rectForward)
        for detection in obstacles:
            self.displayObjects(detection)
        pygame.display.update()
    def displayObjects(self, RectCords):
        #x ave, y ave, w, h
        x, y, w, h = RectCords[2]
        empty_rect = pygame.Rect(x-(w/2), y-(h/2), w, h)
        pygame.Rect()
        centerX = x
        centerY = y+(h/2)+15
        if (centerY + 15 >= 360):
            centerY = y-(h/2)-15
        if (self.Hashmap[RectCords[0]] == 1):
            self.textSignRect.center = (centerX,centerY)
            self.screen.blit(self.textSign, self.textSignRect)
            pygame.draw.rect(self.screen, (0, 0, 255), empty_rect, 3)
        elif (self.Hashmap[RectCords[0]] == 2):
            self.textHumanRect.center = (centerX,centerY)
            self.screen.blit(self.textHuman, self.textHumanRect)
            pygame.draw.rect(self.screen, (0, 255, 0), empty_rect, 3)
        elif (self.Hashmap[RectCords[0]] == 3):
            self.textCarRect.center = (centerX,centerY)
            self.screen.blit(self.textCar, self.textCarRect)
            pygame.draw.rect(self.screen, (255, 0, 0), empty_rect, 3)
        elif (self.Hashmap[RectCords[0]] == 4):
            self.textBikeRect.center = (centerX,centerY)
            self.screen.blit(self.textBike, self.textBikeRect)
            pygame.draw.rect(self.screen, (255, 255, 0), empty_rect, 3)
        elif (self.Hashmap[RectCords[0]] == 5):
            self.textLightRect.center = (centerX,centerY)
            self.screen.blit(self.textLight, self.textLightRect)
            pygame.draw.rect(self.screen, (255, 0, 255), empty_rect, 3)
        elif (self.Hashmap[RectCords[0]] == 6):
            self.textHydrantRect.center = (centerX,centerY)
            self.screen.blit(self.textHydrant, self.textHydrantRect)
            pygame.draw.rect(self.screen, (0, 255, 255), empty_rect, 3)
        else:
            self.textBenchRect.center = (centerX,centerY)
            self.screen.blit(self.textBench, self.textBenchRect)
            pygame.draw.rect(self.screen, (200, 100, 200), empty_rect, 3)

