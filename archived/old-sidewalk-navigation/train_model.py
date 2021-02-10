import datetime

import numpy as np
import tensorflow as tf

import constants
import model_composition

x_train = []
y_train = []


def retrieve_x_train():
    global x_train
    x_train = np.load(constants.x_train_npy_path)


def retrieve_y_train():
    global y_train
    y_train = np.load(constants.y_train_npy_path)


print("Retrieving data")
retrieve_x_train()
retrieve_y_train()

print("\n\nx_train length: {}".format(len(x_train)))
print("y_train length: {}\n\n".format(len(y_train)))

model = model_composition.model

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print(np.shape(x_train))

log_dir = constants.train_npy_path + "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.fit(x=x_train,
          y=y_train,
          epochs=30,
          callbacks=[tensorboard_callback])

if input("Do you want to save model? y for yes, n for no?\n") == 'y':
    model.save(constants.model_path)

print(model.metrics_names)
print(model.evaluate(x_train, y_train))
