import json
import random
import cv2
import numpy as np
import constants
import image_processing as fp

timestamps = {}
x_train = []
y_train = []
frame_counter = 0


def load_json():
    with open('timestamps.json', "r+") as file:
        global timestamps
        timestamps = json.load(file)
        new_timestamps = []
        for timestamp in timestamps:
            new_timestamps.append([float(timestamp), timestamps.get(str(timestamp))])

        return new_timestamps


def save_x_train(x_train_np):
    np.save(constants.train_npy_path + 'x_train', x_train_np)


def save_y_train(y_train_list):
    np.save(constants.train_npy_path + 'y_train', np.array(y_train_list))


def generate_training_data():
    training_data = cv2.VideoCapture(constants.video_training_data_path)
    timestamps = load_json()
    timestamps_index = 0
    while training_data.isOpened():
        if timestamps_index < len(timestamps):
            ret, capture = training_data.read()
            if ret:
                global frame_counter
                frame_counter += 1
                print("Frame Counter: {}".format(frame_counter))
                sec_since_start = training_data.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                print("Video Current Position {}".format(sec_since_start))
                print(timestamps[timestamps_index])

                edges = fp.pre_processing(capture)
                x_train.append(edges)
                y_train.append(constants.categories.get(timestamps[timestamps_index][1]))

                if len(timestamps) > timestamps_index + 1 and timestamps[timestamps_index + 1][0] < sec_since_start:
                    timestamps_index += 1

                # lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100)
                # try:
                #     for x1, y1, x2, y2 in lines[0]:
                #         cv2.line(edges, (x1, y1), (x2, y2), (100, 100, 0), 5)
                # except:
                #     pass
                cv2.imshow("Sidewalk Dataset", edges)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
    training_data.release()
    cv2.destroyAllWindows()


def balance_training_data():
    global x_train
    global y_train
    print("Balancing training data.")
    raw_straight_frame_count = y_train.count(constants.categories.get("Straight"))
    raw_right_frame_count = y_train.count(constants.categories.get("Right"))
    raw_left_frame_count = y_train.count(constants.categories.get("Left"))

    print("\nStraight Frame Count: {}".format(y_train.count(constants.categories.get("Straight"))))
    print("Right Frame Count: {}".format(y_train.count(constants.categories.get("Right"))))
    print("Left Frame Count: {}".format(y_train.count(constants.categories.get("Left"))))

    max_category_training_size = min(raw_straight_frame_count, raw_left_frame_count, raw_right_frame_count)

    print("Max Category Training Size: {}".format(max_category_training_size))
    straight_frame_counter = 0
    right_frame_counter = 0
    left_frame_counter = 0

    balanced_x_train = []
    balanced_y_train = []
    for i in range(0, max_category_training_size + 1):
        if y_train[i] == "Straight":
            if straight_frame_counter < max_category_training_size:
                straight_frame_counter += 1
                balanced_x_train.append(x_train[i])
                balanced_y_train.append(y_train[i])

        elif y_train[i] == "Right":
            if right_frame_counter < max_category_training_size:
                right_frame_counter += 1
                balanced_x_train.append(x_train[i])
                balanced_y_train.append(y_train[i])
        else:
            if left_frame_counter < max_category_training_size:
                left_frame_counter += 1
                balanced_x_train.append(x_train[i])
                balanced_y_train.append(y_train[i])

# for c in range(0, len(balanced_x_train)):
#     cv2.imshow("asd", balanced_x_train[c])
#     print(balanced_y_train[c])

    x_train = np.array(balanced_x_train)
    y_train = balanced_y_train


def shuffling_training_data():
    print("Shuffling training data.")
    seed = random.random()
    random.seed(seed)
    random.shuffle(x_train)
    random.seed(seed)
    random.shuffle(y_train)


generate_training_data()
shuffling_training_data()
balance_training_data()

if input("Do you want to save x_train? y for yes, n for no?\n") == 'y':
    save_x_train(x_train)
if input("Do you want to save y_train? y for yes, n for no?\n") == 'y':
    save_y_train(y_train)


