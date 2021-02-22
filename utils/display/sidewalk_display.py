import pygame
import sys
import cv2
import PIL
from PIL import Image
def convertImg(str):
    img = Image.open(str)
    img = img.transpose(Image.ROTATE_90)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] <= 255 and item[0] >= 205-40 and item[1] <= 255 and item[1] >= 205-40 and item[2] <= 255 and item[2] >= 205-40:
            newData.append((255,255,255,0))
        else:
            newData.append((item[0],item[1],item[2],170))
    img.putdata(newData)
    img.save("./UpMe2.png","PNG")
def convertImg2(str):
    img = Image.open(str)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] <= 255 and item[0] >= 205-25 and item[1] <= 255 and item[1] >= 205-25 and item[2] <= 255 and item[2] >= 205-25:
            newData.append((255,255,255,0))
        else:
            newData.append((item[0],item[1],item[2],170))
    img.putdata(newData)
    img.save("./Up5.png","PNG")
def start_display():
    pygame.init()
    screen = pygame.display.set_mode((1920,1050))
    bg_color = (0, 0, 0)
    varx = 1575
    vary = 1000
    stream = cv2.VideoCapture(0)
    while True:
        direction = 1
        transform = stream.read()[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(bg_color)
        #img2 = pygame.image.load("D:/Maxwell/SpecialRobotStuff/blind-navigation/utils/display/School.jpg")
        img2 = pygame.surfarray.make_surface(transform)
        img2 = img2.convert()

        rect2 = img2.get_rect()
        if (rect2[2] > 1920):
            rect2[3] *= 1920/rect2[2]
            rect2[2] *= 1920/rect2[2]
        if (rect2[3] > 1000):
            rect2[2] *= 1000/rect2[3]
            rect2[3] *= 1000/rect2[3]
        img2 = pygame.transform.scale(img2, (rect2[2], rect2[3]))
        screen = pygame.display.set_mode((rect2[2], rect2[3]))
        screen.blit(img2, rect2)
        if direction == 0:
            img = pygame.image.load("D:/Maxwell/SpecialRobotStuff/blind-navigation/utils/display/Right5.png")
            img = img.convert_alpha()
            rect = img.get_rect()
            rect[2]/=3
            rect[3]/=3
            rect[2] *= rect2[2]/varx
            rect[3] *= rect2[3]/vary
            img = pygame.transform.scale(img, (rect[2], rect[3]))
            rect = rect.move((rect2[2]/2-rect[2]/2, 5/10*rect2[3]))
            screen.blit(img, rect)
        if direction == 1:
            img = pygame.image.load("D:/Maxwell/SpecialRobotStuff/blind-navigation/utils/display/Right6.png")
            img = img.convert_alpha()
            rect = img.get_rect()
            rect[2]/=3
            rect[3]/=3
            rect[2] *= rect2[2]/varx
            rect[3] *= rect2[3]/vary
            img = pygame.transform.scale(img, (rect[2], rect[3]))
            rect = rect.move((rect2[2] / 2 - rect[2] / 2, 5 / 10 * rect2[3]))
            screen.blit(img, rect)
        if direction == 2:
            img = pygame.image.load("D:/Maxwell/SpecialRobotStuff/blind-navigation/utils/display/UpMe2.png")
            img = img.convert_alpha()
            rect = img.get_rect()
            rect[2]/=3
            rect[3]/=3
            rect[2] *= rect2[2]/varx
            rect[3] *= rect2[3]/vary
            img = pygame.transform.scale(img, (rect[2], rect[3]))
            rect = rect.move((rect2[2] / 2 - rect[2] / 2, 5 / 10 * rect2[3]))
            screen.blit(img, rect)
        pygame.display.flip()
        pygame.display.update()
#convertImg(("D:/Maxwell/SpecialRobotStuff/blind-navigation/utils/display/UpMe.png"))
start_display()
#runfile("D:/Maxwell/SpecialRobotStuff/blind-navigation/utils/display/sidewalk_display.py")