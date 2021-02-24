import pygame


class Display:
    def __init__(self):
        pygame.init()
        self.pics = self.__image_preprocessing()
        self.imgLeft = self.pics[0] # TODO: dont scale this hear - put in image processing function
        self.rect1 = self.pics[1]
        self.imgLeft = pygame.transform.scale(self.imgLeft, (self.rect1[2], self.rect1[3]))
        self.imgForward = self.pics[2]
        self.rect3 = self.pics[3]
        self.imgForward = pygame.transform.scale(self.imgForward, (self.rect3[2], self.rect3[3]))
        self.imgRight = self.pics[4]
        self.rect4 = self.pics[5]
        self.imgRight = pygame.transform.scale(self.imgRight, (self.rect4[2], self.rect4[3]))
        self.screen = self.pics[6]

    def __image_preprocessing(self):
        screen = pygame.display.set_mode((1920,1000))
        imgLeft = pygame.image.load("../display-resources/Right.png")
        imgForward = pygame.image.load("../display-resources/Forward.png")
        imgRight = pygame.image.load("../display-resources/Left.png")
        varx = 1575
        vary = 1000
        rect2 = ((0,0,480,360))

        screen = pygame.display.set_mode((rect2[2], rect2[3]))

        imgLeft = imgLeft.convert_alpha()
        rect = imgLeft.get_rect()
        rect[2] /= 3
        rect[3] /= 3
        rect[2] *= rect2[2] / varx
        rect[3] *= rect2[3] / vary
        rect = rect.move((rect2[2] / 2 - rect[2] / 2 + rect2[2]/10, 5 / 10 * rect2[3]))
        imgLeft = pygame.transform.scale(imgLeft, (rect[2], rect[3]))

        imgForward = imgForward.convert_alpha()
        rect4 = imgForward.get_rect()
        rect4[2] /= 2
        rect4[3] /= 2
        rect4[2] *= rect2[2] / varx
        rect4[3] *= rect2[3] / vary
        rect4 = rect4.move((rect2[2] / 2 - rect4[2]/2, 5/10 * rect2[3]))
        imgForward = pygame.transform.scale(imgForward, (rect4[2],rect4[3]))

        imgRight = imgRight.convert_alpha()
        rect3 = imgRight.get_rect()
        rect3[2] /= 3
        rect3[3] /= 3
        rect3[2] *= rect2[2] / varx
        rect3[3] *= rect2[3] / vary
        rect3 = rect3.move((rect2[2] / 2 - rect3[2] / 2 - rect2[2]/10, 5 / 10 * rect2[3]))
        imgRight = pygame.transform.scale(imgRight, (rect3[2], rect3[3]))
        return ((imgLeft,rect,imgForward,rect4,imgRight,rect3,screen))

    def update(self,state, orig_cap):
        orig_cap = orig_cap.swapaxes(0, 1)
        orig_cap = orig_cap[:, :, ::-1]
        self.img2 = pygame.surfarray.make_surface(orig_cap)
        self.img2 = self.img2.convert()
        self.rect2 = self.img2.get_rect()
        self.screen.blit(self.img2, self.rect2)
        if state == "Left of Sidewalk":
            self.screen.blit(self.imgLeft, self.rect1)
        elif state == "Right of Sidewalk":
            self.screen.blit(self.imgRight, self.rect4)
        elif state == "Middle of Sidewalk":
            self.screen.blit(self.imgForward, self.rect3)
        # pygame.display.flip()
        pygame.display.update()


