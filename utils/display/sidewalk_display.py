import pygame
def initPics():
    screen = pygame.display.set_mode((1920,1000))
    imgLeft = pygame.image.load("/src/display-resources/Right5.png")
    imgForward = pygame.image.load("/src/display-resources/Forward.png")
    imgRight = pygame.image.load("/src/display-resources/Left.png")
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
    rect = rect.move((rect2[2] / 2 - rect[2] / 2 - rect2[2]/10, 5 / 10 * rect2[3]))
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
    rect3 = rect3.move((rect2[2] / 2 - rect3[2] / 2 + rect2[2]/10, 5 / 10 * rect2[3]))
    imgRight = pygame.transform.scale(imgRight, (rect3[2], rect3[3]))

    return ((imgLeft,rect,imgForward,rect4,imgRight,rect3,screen))
#runfile("D:/Maxwell/SpecialRobotStuff/blind-navigation/utils/display/sidewalk_display.py")
#runfile("D:/Maxwell/SpecialRobotStuff/blind-navigation/src/sidewalk-classification/model_evaluator.py")