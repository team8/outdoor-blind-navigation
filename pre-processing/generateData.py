import os
import random

import cv2
import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing

data_augmentation = tf.keras.Sequential([
        preprocessing.RandomRotation(0.2),
        preprocessing.RandomZoom(0.2, 0.2),
        preprocessing.RandomContrast(0.25),
        preprocessing.RandomTranslation(0.2,0.2)
])

#This should duplicate everything in a directory and put it into another one
def flipData(path, label, outpath):
    images = []
    print(os.listdir(path))
    for im in os.listdir(path):  # read image from folder, append into images array
        images.append(os.path.join(path, im))
    for i in range(0, len(images)):
        image = images[i]
        original_image = cv2.imread(image)
        transformed_image = cv2.flip(original_image, 1)
        new_image_path = "%s/fd_%s_%s.jpg" % (outpath, label, i + 1)
        transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(new_image_path, transformed_image)  # save transformed image to path

def flipData(numberToMake, path, label, outpath):
    images = []
    print(os.listdir(path))
    for im in os.listdir(path):  # read image from folder, append into images array
        images.append(os.path.join(path, im))
    for i in range(0, numberToMake):
        image = images[i]
        original_image = cv2.imread(image)
        transformed_image = cv2.flip(original_image, 1)
        new_image_path = "%s/fd_%s_%s.jpg" % (outpath, label, i + 1)
        transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(new_image_path, transformed_image)  # save transformed image to path


def fillDataSet(images_to_generate, path, label, outpath):
    images = []
    for im in os.listdir(path):  # read image from folder, append into images array
        images.append(os.path.join(path, im))
    for i in range(0, images_to_generate):
        image = random.choice(images)
        original_image = cv2.imread(image)
        transformed_image = random.choice(data_augmentation)(original_image)
        new_image_path = "%s/aug_%s_%s.jpg" %(outpath,label,i + 1)
        transformed_image=cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(new_image_path, transformed_image)  # save transformed image to path

        i += 1
def genLeft():
    flipData(300, "/programming/ml-dataset/Sidewalk Dataset/Right of Sidewalk", "Left", "~/programming/ml-dataset/Sidewalk Dataset Augmented/Left of Sidewalk")
    fillDataSet(1000, "/programming/ml-dataset/Sidewalk Dataset/Left of Sidewalk", "Left",  "~/programming/ml-dataset/Sidewalk Dataset Augmented/Left of Sidewalk")
def genRight():
    flipData(300, "/programming/ml-dataset/Sidewalk Dataset/Left of Sidewalk", "Right", "~/programming/ml-dataset/Sidewalk Dataset Augmented/Right of Sidewalk")
    fillDataSet(1000, "/programming/ml-dataset/Sidewalk Dataset/Right of Sidewalk", "Right",  "~/programming/ml-dataset/Sidewalk Dataset Augmented/Right of Sidewalk")


genLeft()
genRight()