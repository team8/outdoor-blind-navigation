from person_automobile_sign_detection.detection import Detection
import numpy as np

blank_detection = Detection()
# provides psuedo direction vector
def get_direction_vector(label, bbox_buffer):
    bbox_list = np.array([x for x in bbox_buffer if x is not None])
    average_bbox = bbox_list.mean(axis=0)
    newest_bbox = bbox_list[0]
    oldest_bbox = bbox_list[-1]
    newest_bbox_area = newest_bbox[2] * newest_bbox[3]
    average_bbox_area = average_bbox[2] * average_bbox[3]
    return [newest_bbox[0] - average_bbox[0], newest_bbox[1] - average_bbox[1], ((newest_bbox_area - average_bbox_area)/average_bbox_area)]
    # weighting = 0.1
    # base_position = (bbox_list[-1][0], bbox_list[-1][1])
    # base_area = bbox_list[-1][2] * bbox_list[-1][3]
    # new_area = bbox_list[0][2] * bbox_list[0][3]
    #
    # summation_direction_vector = (0, 0, new_area - base_area)
    # for i in range(len(bbox_list) - 1, 0):
    #     summation_direction_vector = ((bbox_list[i][0] - base_position[0])*weighting + summation_direction_vector[0], (bbox_list[i][1] - base_position[1])*weighting + summation_direction_vector[1],25)
    #
    #     # z offset :  (new_area - base_area)**(1/3)
    #
    # return summation_direction_vector
    #


def compute_iou(orig_bbox, new_bbox): # Should also look at general shape of bboxes to see if they match? Likely not needed                                           
    x1, y1, w1, h1 = orig_bbox
    x2, y2, w2, h2 = new_bbox

    # 4 corners bbox                                                                                                                      
    x11 = int(x1 - w1/2)
    x12 = int(x1 + w1/2)
    y11 = int(y1 - h1/2)
    y12 = int(y1 + h1/2)

    x21 = int(x2 - w2/2)
    x22 = int(x2 + w2/2)
    y21 = int(y2 - h2/2)
    y22 = int(y2 + h2/2)

    # finds iou points                                                                                                                    
    y1 = y11 if y11 > y21 else y21
    x1 = x11 if x11 > x21 else x21
    y2 = y12 if y12 < y22 else y22
    x2 = x12 if x12 < x22 else x22
    iou_area = (x2 - x1) * (y2 - y1)
    prev_bbox_area = w1 * h1
    new_bbox_area = w2 * h2
    if iou_area < 0:
        return 0
    iou_percentage = iou_area * 100 / prev_bbox_area

    return iou_percentage


def get_iou_rect(orig_bbox, new_bbox): # should also look at general shape to see if they match
    x1, y1, w1, h1 = orig_bbox
    x2, y2, w2, h2 = new_bbox

    # 4 corners bbox
    x11 = int(x1 - w1/2)
    x12 = int(x1 + w1/2)
    y11 = int(y1 - h1/2)
    y12 = int(y1 + h1/2)

    x21 = int(x2 - w2/2)
    x22 = int(x2 + w2/2)
    y21 = int(y2 - h2/2)
    y22 = int(y2 + h2/2)


    # finds iou points
    y1 = y11 if y11 > y21 else y21
    x1 = x11 if x11 > x21 else x21
    y2 = y12 if y12 < y22 else y22
    x2 = x12 if x12 < x22 else x22
    # print("Intersection Box: ", x1, y1, x2, y2)
    return (x1, y1, x2, y2)
