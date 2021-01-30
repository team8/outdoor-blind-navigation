import tensorflow as tf
import cv2
import os
import numpy as np
import random

input_shape = (150, 150, 3)
model = tf.keras.models.Sequential([
   tf.keras.layers.Conv2D(64, (5, 5), input_shape=input_shape),
   tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
   tf.keras.layers.Conv2D(128, (3, 3), input_shape=input_shape),
   tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
   tf.keras.layers.Flatten(input_shape=input_shape),
   tf.keras.layers.Dense(512, activation='relu'),
   tf.keras.layers.Dropout(0.3),
   tf.keras.layers.Dense(2, activation='softmax')])

model.compile(
    optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy'])
#find best optimizer (Adam, rmsprop, ADAsgrad etc), loss function is binary closs entropy for now because only binary output but try multi-class cross-entropy loss

# important note: if your true labels are one hot encoded ie. [1, 0, 0], [0, 1, 0], use categorical crossentropy, if true labels are integers ie [1], [2], [3], use sparse categorical_srossentropy.  (saves time in computation and memory because uses single integer for a class)

# important note 2: use binary cross entropy when doing multi label classification (possibly inclusive classes) (categorical cross entropy is when you have exclusive classes) (i need binary cross entropy)


# model.fit(x=np.array(fire_detection_train_dataset), y=one_hot_encoded_array, epochs=8)


def preprocess_image(preprocessed_image: np.ndarray) -> np.ndarray:
    new_image = cv2.resize(src=preprocessed_image, dsize=(input_shape[0], input_shape[1]      ))
    new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    return new_image/255.0

dataset_path = "./fire_dataset/"
fire_images_dataset_dir = os.listdir(dataset_path + "fire_images")
non_fire_images_dataset_dir = os.listdir(dataset_path + "non_fire_images")
fire_detection_train_dataset = []
one_hot_encoded_array = []
count = 0
for image_file_name in non_fire_images_dataset_dir:
    image = cv2.imread(dataset_path + "non_fire_images/" + image_file_name)
    new_image = preprocess_image(image)
    fire_detection_train_dataset.append(new_image)
    one_hot_encoded_array.append([0, 1])
for image_file_name in fire_images_dataset_dir:
    count += 1
    if count >  217:
        break
    image = cv2.imread(dataset_path + "fire_images/" + image_file_name)
    new_image = preprocess_image(image)
    fire_detection_train_dataset.append(new_image)
    one_hot_encoded_array.append([1, 0])


for i in range(0, len(fire_detection_train_dataset)):
    cv2.imshow("image", fire_detection_train_dataset[i])
    print(one_hot_encoded_array[i])
    cv2.waitKey(3)

model.fit(x=np.array(fire_detection_train_dataset), y=np.array(one_hot_encoded_array), epochs=7)

print("Prediction for first image")
print(model.predict(np.expand_dims(fire_detection_train_dataset[0], 0)))
print("Prediction for second image")
print(model.predict(np.expand_dims(fire_detection_train_dataset[len(fire_detection_train_dataset) - 5], 0)))

print(model.summary())



capture = cv2.VideoCapture(0)
while True:
    ret, image = capture.read()
    orig = image.copy()
    image = np.expand_dims(preprocess_image(image), 0)
    cv2.imshow("image", orig);
    cv2.waitKey(1)
    prediction = model.predict(image)
    if prediction[0][0] < prediction[0][1]:
        print("Image is detected as not fire")
    else:
        print("Image is detected as fire")

    print(random.randint(0,5))
