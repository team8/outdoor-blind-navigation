import os
import random

import cv2
from tensorflow.keras.layers.experimental import preprocessing
import pathlib


data_augmentation = [
        preprocessing.RandomRotation(0.2),
        preprocessing.RandomZoom(0.2, 0.2),
        preprocessing.RandomContrast(0.25),
        preprocessing.RandomTranslation(0.2,0.2)
]

#This should duplicate everything in a directory and put it into another one
def flipData(path, label, outpath):
    images = []
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
    for im in os.listdir(path):  # read image from folder, append into images array
        images.append(os.path.join(path, im))
    for i in range(0, numberToMake):
        image = images[i]
        original_image = cv2.imread(image)
        # print(cv2.imshow("image", original_image))
        transformed_image = cv2.flip(original_image, 1)
        new_image_path = "%s/fd_%s_%s.jpg" % (outpath, label, i + 1)
        new_image_path = pathlib.PurePosixPath(new_image_path)
        cv2.imwrite(new_image_path.__str__(), transformed_image)  # save transformed image to path




def genLeft(num):
    flipData(num, "../ml-datasets/Right of Sidewalk/", "Left", "../ml-datasets/Sidewalk Dataset Augmented/Left of Sidewalk")
def genRight(num):
    flipData(num, "../ml-datasets/Left of Sidewalk", "Right", "../ml-datasets/Sidewalk Dataset Augmented/Right of Sidewalk")
def genMiddle(num):
    flipData(num, "../ml-datasets/Middle of Sidewalk", "Middle", "../ml-datasets/Sidewalk Dataset Augmented/Middle of Sidewalk")

#Left percent, middle percent, right percent correspond to what percent of the total images generated will be what. total is how many in total you will geneate, smallestSetNum will be how many images are in the smallest set
def genBalanced(leftPercent, middlePercent, rightPercent, total, smallestSetNum):
    if((int)(leftPercent * total) > smallestSetNum):
        total = smallestSetNum / leftPercent
    if ((int)(middlePercent * total) > smallestSetNum):
        total = middlePercent / leftPercent
    if ((int)(rightPercent * total) > smallestSetNum):
        total = smallestSetNum / rightPercent
    genLeft((int)(leftPercent * total))
    genMiddle((int)(middlePercent * total))
    genRight((int)(rightPercent * total))

genBalanced(1/3, 1/3, 1/3, 9, 3)




