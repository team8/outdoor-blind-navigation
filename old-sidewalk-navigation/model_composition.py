import tensorflow as tf

import constants

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(64, 5,
                           input_shape=(constants.capture_dimensions[1], constants.capture_dimensions[0])),
tf.keras.layers.Conv1D(64, 5,
                           input_shape=(constants.capture_dimensions[1], constants.capture_dimensions[0])),
tf.keras.layers.Conv1D(64, 5,
                           input_shape=(constants.capture_dimensions[1], constants.capture_dimensions[0])),
tf.keras.layers.Conv1D(64, 3,
                           input_shape=(constants.capture_dimensions[1], constants.capture_dimensions[0])),
tf.keras.layers.Conv1D(64, 3,
                           input_shape=(constants.capture_dimensions[1], constants.capture_dimensions[0])),
    # tf.keras.layers.MaxPooling1D(pool_size=(2, 2)),
    # tf.keras.layers.Conv1D(128, (3, 3),
    #                        input_shape=(constants.capture_dimensions[0], constants.capture_dimensions[1])),
    # tf.keras.layers.MaxPooling1D(pool_size=(2, 2)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Flatten(input_shape=(constants.capture_dimensions[1], constants.capture_dimensions[0])),
    tf.keras.layers.Dense(1164, activation='relu'),
    tf.keras.layers.Dense(100, activation='relu'),
    tf.keras.layers.Dense(50, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(3, activation='softmax')])
