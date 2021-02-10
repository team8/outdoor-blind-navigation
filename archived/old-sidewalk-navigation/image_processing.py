import cv2
import numpy as np

import constants

green_lower_bound = (35, 70, 40)
green_higher_bound = (90, 240, 220)
roi_vertices = np.array([[335, 0], [350, 125], [35, 125], [50, 0]], np.int32)


def pre_processing(img):
    new_img = cv2.resize(img, constants.capture_dimensions)
    new_img = cv2.GaussianBlur(new_img, (5, 5), 0)

    # finds green objects in image
    green_mask = cv2.inRange(cv2.GaussianBlur(np.copy(new_img), (13, 13), 0), green_lower_bound, green_higher_bound)
    contours = cv2.findContours(green_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]

    # finds edges in the image
    new_img = cv2.Canny(new_img, 175, 50)

    # create roi
    mask = np.zeros_like(new_img)
    cv2.fillPoly(mask, [roi_vertices], 255)
    new_img = cv2.bitwise_and(new_img, mask)

    # remove green objects from image
    cv2.drawContours(new_img, contours, -1, (0, 0, 0), thickness=cv2.FILLED)

    # shows original image
    # cv2.imshow("orig", img)

    return new_img
