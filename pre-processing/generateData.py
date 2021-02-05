import io
import os
import random

import cv2
import numpy as np
#Need to fill in paths
import tf as tf
from tensorflow.python.layers import layers

images_path = ""
augmented_path = ""
data = np.asarray([['left']['middle']['right']])
def fillDataSet(images_to_generate, path, label):
    data_augmentation = tf.keras.Sequential([
        layers.experimental.preprocessing.RandomRotation(0.2),
        layers.experimental.preprocessing.RandomZoom(0.2, 0.2),
        layers.experimental.preprocessing.RandomContranst(),
        layers.experimental.preprocessing.RanomTranslation()
    ])
    images = []
    for im in os.listdir(images_path):  # read image from folder, append into images array
        images.append(os.path.join(images_path, im))
    i = 1
    # I know that i should start at 0 but it needs to be 1 for clean image titles
    while i <= images_to_generate:
        image = random.choice(images)
        original_image = io.imread(image)
        transformed_image = random.choice(data_augmentation)(original_image)


