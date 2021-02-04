import numpy as np
import cv2

# probably put this to something more permanent
img = cv2.imread('test.jpg')
img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
img_size = (480, 480)
img = cv2.resize(img, img_size)
img = cv2.transpose(img)

original = img

edges = cv2.Canny(img, 275, 350)

img = cv2.medianBlur(img, 5)
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=25, maxLineGap=200)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
edges = cv2.dilate(edges, kernel)

# remove the blue red layer for smaller image size
b, g, r = cv2.split(img)
img = cv2.merge((b, g, edges))

for line in lines:
    x1, y1, x2, y2 = line[0]
    if not -0.2 < (y1 - y2) / (x1 - x2) < 0.2:
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

cv2.imshow('test2', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
