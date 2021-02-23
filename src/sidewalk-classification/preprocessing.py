import numpy as np
import cv2


def preprocess(img, side):
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.transpose(img)
    size_y, size_x, _ = img.shape
    img_crop_size = (480, 480)
    min_resize = max(img_crop_size[0] / size_x, img_crop_size[1] / size_y)
    img = cv2.resize(img, (int(size_x * min_resize), int(size_y * min_resize)))  # keeps the same aspect ratio
    size_y, size_x, _ = img.shape
    if side == 1:
        # road is on the left so crop it there
        img = img[(size_y - img_crop_size[1]):size_y, 0:img_crop_size[0]]
    elif side == -1:
        # road is on the right so crop it there
        img = img[(size_y - img_crop_size[1]):size_y, (size_x - img_crop_size[0]):size_x]
    else:
        img = img[(size_y - img_crop_size[1]):size_y, int((size_x - img_crop_size[0]) / 2):int(size_x - (size_x - img_crop_size[0]) / 2)]

    edges = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(edges, 200, 300)
    edges = cv2.GaussianBlur(edges, (3, 3), 0)

    img = cv2.medianBlur(img, 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edges = cv2.dilate(edges, kernel)

    # remove the blue red layer for smaller image size
    b, g, r = cv2.split(img)
    img = cv2.merge((b, edges, r))

    cv2.imshow('test2', img)
    cv2.waitKey(1)

    img = img / 255
    return img

