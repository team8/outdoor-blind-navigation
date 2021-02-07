import tensorflow as tf
import matplotlib as plt
import cv2
import os
import numpy as np
import random
import preprocessing

input_shape = (240, 100, 3)
model = tf.keras.models.Sequential([
   tf.keras.layers.Conv2D(64, (11, 11), input_shape=input_shape),
   tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
   tf.keras.layers.Conv2D(128, (9, 9), input_shape=input_shape),
   tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
   tf.keras.layers.Flatten(input_shape=input_shape),
   tf.keras.layers.Dense(300, activation='relu'),
   tf.keras.layers.Dropout(0.3),
   tf.keras.layers.Dense(3, activation='softmax')])

model.compile(
    optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
#find best optimizer (Adam, rmsprop, ADAsgrad etc), loss function is binary closs entropy for now because only binary output but try multi-class cross-entropy loss

# important note: if your true labels are one hot encoded ie. [1, 0, 0], [0, 1, 0], use categorical crossentropy, if true labels are integers ie [1], [2], [3], use sparse categorical_srossentropy.  (saves time in computation and memory because uses single integer for a class)

# important note 2: use binary cross entropy when doing multi label classification (possibly inclusive classes) (categorical cross entropy is when you have exclusive classes) (i need binary cross entropy)


# model.fit(x=np.array(fire_detection_train_dataset), y=one_hot_encoded_array, epochs=8)
batch_size = 32
dataset_path = "../../../ml-datasets/Sidewalk Dataset Augmented/"
# train_ds = tf.keras.preprocessing.image_dataset_from_directory( dataset_path , validation_split = 0.1, subset="training", seed=123, image_size = (input_shape[0], input_shape[1]))
train_ds = tf.keras.preprocessing.image_dataset_from_directory( dataset_path , validation_split = 0.1, subset="training", seed=123, image_size = (input_shape[0], input_shape[1]), batch_size=batch_size, label_mode="categorical")
labels = ["Left of Sidewalk", "Middle of Sidewalk", "Right of Sidewalk"]
# def fix(image, label):
    # img = tf.cast(image, tf.float32)
    # return tf.expand_dims(img, 0), label

# train_ds = train_ds.map(fix)

# left_sidewalk_path = dataset_path + "Left of Sidewalk/"
# right_sidewalk_path = dataset_path + "Right of Sidewalk/"
# left_sidewalk_images_dataset_dir = os.listdir(left_sidewalk_path)
# right_sidewalk_images_dataset_dir = os.listdir(right_sidewalk_path)
# sidewalk_detection_train_dataset = []
# one_hot_encoded_array = []
# count = 0
# print(left_sidewalk_path + random.choice(left_sidewalk_images_dataset_dir))
# print(random.choice(left_sidewalk_images_dataset_dir))
# for i in range(150):
    # sidewalk_detection_train_dataset.append(cv2.resize(cv2.imread(left_sidewalk_path + random.choice(left_sidewalk_images_dataset_dir)), (240, 100)))
    # one_hot_encoded_array.append([1, 0])
    # print(i)
# for i in range(150):
    # sidewalk_detection_train_dataset.append(cv2.resize(cv2.imread(right_sidewalk_path + random.choice(right_sidewalk_images_dataset_dir)), (240, 100)))
    # one_hot_encoded_array.append([0, 1])

# def create_one_hot_encoded(image, label):
    # print(label)
    # if label == "Left of Sidewalk":
        # one_hot_encoded_array.append([1, 0, 0])
#
    # if label == "Right of Sidewalk":
        # one_hot_encoded_array.append([0, 0, 1])
#
    # if label == "Middle of Sidewalk":
        # one_hot_encoded_array.append([0, 1, 0])

# train_ds = train_ds.map(create_one_hot_encoded)

train_ds = train_ds.shuffle(buffer_size = 100)
# train_ds = train_ds.map(lambda x, y: (x, [0, 1, 0]))
# train_ds = train_ds.map(lambda x, y: (x, np.array(labels.index(y))))
train_ds = train_ds.cache()
# train_ds = train_ds.batch(batch_size)
print(train_ds)
model.fit(train_ds, batch_size = batch_size, epochs=15)

print(model.summary())


vid = cv2.VideoCapture("/home/aoberai/Downloads/1080p.mov")
while True:
    _, cap = vid.read()
    cap = cv2.flip(cv2.resize(cap, (240, 100)), 1)
    cv2.imshow("Test", cap)
    prediction = model.predict(np.expand_dims(cap, 0))
    if prediction[0][0] > 0.5:
            print("Right")
    else:
            print("Left")
    cv2.waitKey(1)
