import numpy as np
import cv2


def preprocess(img, side):
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.transpose(img)

    size_y, size_x, _ = img.shape
    # crop - needs work
    img_crop_size = (480, 480)
    min_resize = max(img_crop_size[0] / size_x, img_crop_size[1] / size_y)
    img = cv2.resize(img, (int(size_x * min_resize), int(size_y * min_resize)))  # keeps the same aspect ratio
    # print(img.shape)
    img2 = img
    size_y, size_x, _ = img.shape
    # print((int(size_x * min_resize), int(size_y * min_resize)))
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
    # lines = cv2.HoughLinesP(edges, 1, np.pi / 270, 150, minLineLength=20, maxLineGap=30)

    img = cv2.medianBlur(img, 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edges = cv2.dilate(edges, kernel)

    # remove the blue red layer for smaller image size
    b, g, r = cv2.split(img)
    img = cv2.merge((b, edges, r))

    # if lines is not None:
    #     for line in lines:
    #         x1, y1, x2, y2 = line[0]
    #         if not -0.3 < (y1 - y2) / (x1 - x2) < 0.3:
    #             cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

    # print(img.shape)
    cv2.imshow('test2', img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()


cap = cv2.VideoCapture('1080p.mov')
# cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    preprocess(img, 0)
