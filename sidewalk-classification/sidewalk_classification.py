import tensorflow as tf
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
   tf.keras.layers.Dense(2, activation='softmax')])

model.compile(
    optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy'])
#find best optimizer (Adam, rmsprop, ADAsgrad etc), loss function is binary closs entropy for now because only binary output but try multi-class cross-entropy loss

# important note: if your true labels are one hot encoded ie. [1, 0, 0], [0, 1, 0], use categorical crossentropy, if true labels are integers ie [1], [2], [3], use sparse categorical_srossentropy.  (saves time in computation and memory because uses single integer for a class)

# important note 2: use binary cross entropy when doing multi label classification (possibly inclusive classes) (categorical cross entropy is when you have exclusive classes) (i need binary cross entropy)


# model.fit(x=np.array(fire_detection_train_dataset), y=one_hot_encoded_array, epochs=8)

dataset_path = "../../../ml-datasets/Sidewalk Dataset Augmented/"
left_sidewalk_path = dataset_path + "Left of Sidewalk/"
right_sidewalk_path = dataset_path + "Right of Sidewalk/"
left_sidewalk_images_dataset_dir = os.listdir(left_sidewalk_path)
right_sidewalk_images_dataset_dir = os.listdir(right_sidewalk_path)
sidewalk_detection_train_dataset = []
one_hot_encoded_array = []
count = 0
print(left_sidewalk_path + random.choice(left_sidewalk_images_dataset_dir))
print(random.choice(left_sidewalk_images_dataset_dir))
for i in range(150):
    sidewalk_detection_train_dataset.append(cv2.resize(cv2.imread(left_sidewalk_path + random.choice(left_sidewalk_images_dataset_dir)), (240, 100)))
    one_hot_encoded_array.append([1, 0])
    print(i)
for i in range(150):
    sidewalk_detection_train_dataset.append(cv2.resize(cv2.imread(right_sidewalk_path + random.choice(right_sidewalk_images_dataset_dir)), (240, 100)))
    one_hot_encoded_array.append([0, 1])



for i in range(0, len(sidewalk_detection_train_dataset)):
    cv2.imshow("image", sidewalk_detection_train_dataset[i])
    print(one_hot_encoded_array[i])
    cv2.waitKey(1000)

model.fit(x=np.array(sidewalk_detection_train_dataset), y=np.array(one_hot_encoded_array), epochs=7)

print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[0], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[1], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[2], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[3], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[4], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[5], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[6], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[7], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[8], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[9], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[10], 0)))
print("\n\n\n\n")
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[-1], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[-2], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[-3], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[-4], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[-5], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[-6], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[-7], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[-8], 0)))
print(model.predict(np.expand_dims(sidewalk_detection_train_dataset[-9], 0)))

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
