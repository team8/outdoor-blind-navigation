import os
import random

import cv2
import numpy as np
#Need to fill in paths
import skimage
import tensorflow as tf
from tensorflow.python.layers import layers
from tensorflow.keras.layers.experimental import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from skimage import io
from PIL import Image, ImageOps

#
# data = np.asarray([['left']['middle']['right']])
# label_encoder = LabelEncoder()
# integer_encoded = label_encoder.fit_transform(data)

#Generate the one hot encoded path
data_augmentation = tf.keras.Sequential([
        preprocessing.RandomRotation(0.2),
        preprocessing.RandomZoom(0.2, 0.2),
        preprocessing.RandomContrast(0.25),
        preprocessing.RandomTranslation(0.2,0.2)
])

#This should duplicate everything in a directory and put it into another one
def flipData(path, label, outpath):
    images = []
    for im in os.listdir(path):  # read image from folder, append into images array
        images.append(os.path.join(path, im))
    i = 1
    # I know that i should start at 0 but it needs to be 1 for clean image titles
    while i <= len(images):
        image = images[i]
        original_image = Image.open(image)
        transformed_image = ImageOps.mirror(original_image)
        new_image_path = "%s/flipped_%s_%s.jpg" % (outpath, label, i)
        transformed_image = skimage.img_as_ubyte(transformed_image)
        transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(new_image_path, transformed_image)  # save transformed image to path
        i += 1

def fillDataSet(images_to_generate, path, label, outpath):
    images = []
    for im in os.listdir(path):  # read image from folder, append into images array
        images.append(os.path.join(path, im))
    i = 1
    # I know that i should start at 0 but it needs to be 1 for clean image titles
    while i <= images_to_generate:
        image = random.choice(images)
        original_image = io.imread(image)
        transformed_image = random.choice(data_augmentation)(original_image)

        new_image_path = "%s/augmented_%s_%s.jpg" %(outpath,label,i)
        transformed_image = skimage.img_as_ubyte(transformed_image)
        transformed_image=cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(new_image_path, transformed_image)  # save transformed image to path
        i += 1



