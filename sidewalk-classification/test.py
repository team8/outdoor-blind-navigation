import cv2
import os

print(os.listdir("/home/aoberai/Downloads/"))

vid = cv2.VideoCapture("/home/aoberai/Downloads/1080p.mov")
while True:
    _, cap = vid.read()
    cap = cv2.resize(cap, (240, 100))
    cv2.imshow("Test", cap)
    cv2.waitKey(1)

