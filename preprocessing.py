import numpy as np
import cv2

# probably put this to something more permanent
img = cv2.imread('test.jpg')
img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

img_size = (480, 480)

img = cv2.resize(img, img_size)

img = cv2.transpose(img)
edges = cv2.Canny(img, 275, 350)

lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, minLineLength=10, maxLineGap=250)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
edges = cv2.dilate(edges, kernel)

# remove the blue red layer for smaller image size
b, g, r = cv2.split(img)
img = cv2.merge((b, g, edges))


cv2.imshow('test', edges)
cv2.imshow('test2', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
