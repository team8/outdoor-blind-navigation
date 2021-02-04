import numpy as np
import cv2


def preprocess(img_location, side):
    # probably put this to something more permanent
    img = cv2.imread('test.jpg')
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img_size = (480, 480)
    # img = cv2.resize(img, img_size)
    img = cv2.transpose(img)

    print(img.shape)
    size_x, size_y, _ = img.shape
    # crop - needs work
    if side == 1:
        img = img[0:img_size[0], (size_y - img_size[1]):size_y]
    elif side == -1:
        img = img
    else:
        img = img

    edges = cv2.Canny(img, 275, 350)

    img = cv2.medianBlur(img, 5)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=25, maxLineGap=200)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edges = cv2.dilate(edges, kernel)

    # remove the blue red layer for smaller image size
    b, g, r = cv2.split(img)
    img = cv2.merge((b, g, edges))

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if not -0.2 < (y1 - y2) / (x1 - x2) < 0.2:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

    cv2.imshow('test2', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


preprocess('test.jpg', 1)
