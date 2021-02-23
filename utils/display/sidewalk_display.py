import pygame
def initPics(orig_cap):
    imgLeft = pygame.image.load("/utils/display/Right5.png")
    imgForward = pygame.image.load("/utils/display/Forward.png")
    imgRight = pygame.image.load("/utils/display/Left.png")
    varx = 1575
    vary = 1000
    orig_cap = orig_cap.swapaxes(0, 1)
    orig_cap = orig_cap[:, :, ::-1]
    img2 = pygame.surfarray.make_surface(orig_cap)
    img2 = img2.convert()
    rect2 = img2.get_rect()

    imgLeft = imgLeft.convert_alpha()
    rect = imgLeft.get_rect()
    rect[2] /= 3
    rect[3] /= 3
    rect[2] *= rect2[2] / varx
    rect[3] *= rect2[3] / vary
    imgLeft = pygame.transform.scale(imgLeft, (rect[2], rect[3]))
    rect = rect.move((rect2[2] / 2 - rect[2] / 2 - rect2[2]/10, 5 / 10 * rect2[3]))
    imgLeft = pygame.transform.scale(imgLeft, (rect[2], rect[3]))

    imgForward = imgForward.convert_alpha()
    rect = imgForward.get_rect()
    rect[2] /= 2
    rect[3] /= 2
    rect[2] *= rect2[2] / varx
    rect[3] *= rect2[3] / vary
    imgForward = pygame.transform.scale(imgForward, (rect[2], rect[3]))
    rect = rect.move((rect2[2] / 2 - rect[2] / 2, 5 / 10 * rect2[3]))
    imgForward = pygame.transform.scale(imgForward, (rect[2], rect[3]))

    imgRight = imgRight.convert_alpha()
    rect = imgRight.get_rect()
    rect[2] /= 3
    rect[3] /= 3
    rect[2] *= rect2[2] / varx
    rect[3] *= rect2[3] / vary
    imgRight = pygame.transform.scale(imgRight, (rect[2], rect[3]))
    rect = rect.move((rect2[2] / 2 - rect[2] / 2 + rect2[2]/10, 5 / 10 * rect2[3]))
    imgRight = pygame.transform.scale(imgRight, (rect[2], rect[3]))

    screen = pygame.display.set_mode((rect2[2], rect2[3]))

    return ((imgLeft,imgForward,imgRight,screen))
def start_display(rect2, screen, img, off):
    varx = 1575
    vary = 1000
    rect = img.get_rect()
    rect[2] *= rect2[2] / varx
    rect[3] *= rect2[3] / vary
    img = pygame.transform.scale(img, (rect[2], rect[3]))
    rect = rect.move((rect2[2] / 2 - rect[2] / 2, 5 / 10 * rect2[3]))
    screen.blit(img, rect)
    return screen
#runfile("D:/Maxwell/SpecialRobotStuff/blind-navigation/utils/display/sidewalk_display.py")