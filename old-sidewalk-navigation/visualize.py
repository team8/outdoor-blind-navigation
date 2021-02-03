import cv2
import numpy as np
import constants
import time

x_train = np.load(constants.x_train_npy_path)
y_train = np.load(constants.y_train_npy_path)
for i in range(0, len(x_train)):
    x_train[i] = cv2.putText(x_train[i], constants.reverse_categories[y_train[i]], (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv2.imshow("Visualizer", x_train[i])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(1)
