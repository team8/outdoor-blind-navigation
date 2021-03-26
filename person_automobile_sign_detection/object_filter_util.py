
# provides psuedo direction vector
def get_direction_vector(bbox_buffer):
    bbox_list = bbox_buffer.getList()
    if None not in bbox_list:
        # base_position = bbox_list.median()
        # bbox_current_pos = bbox_list.median(bbox_list.size() - 5, bbox_list.size())
        # print(base_position)
        # print(bbox_current_pos)
        # summation_direction_vector = (bbox_current_pos[0] - base_position[0], bbox_current_pos[1] - base_position[1])
        weighting = 0.1
        base_position = (bbox_list[0][0], bbox_list[0][1])
        summation_direction_vector = (0, 0)
        for i in range(1,(len(bbox_list))):
            summation_direction_vector = ((bbox_list[i][0] - base_position[0])*weighting + summation_direction_vector[0], (bbox_list[i][1] - base_position[1])*weighting + summation_direction_vector[1])
        return summation_direction_vector
    return (0, 0)



def compute_iou(orig_bbox, new_bbox): # should also look at general shape to see if they match                                            
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

    # print("Actual bbox coords 1", str((x11, y11, x12, y12)))
    # print("Actual bbox coords 2", str((x21, y21, x22, y22)))
    # finds iou points                                                                                                                    
    y1 = y11 if y11 > y21 else y21
    x1 = x11 if x11 > x21 else x21
    y2 = y12 if y12 < y22 else y22
    x2 = x12 if x12 < x22 else x22
    # print("Intersection Box: ", x1, y1, x2, y2)
    # print("intersection bbox", str((x1, y1, x2, y2)))
    iou_area = (x2 - x1) * (y2 - y1)
    prev_bbox_area = w1 * h1
    new_bbox_area = w2 * h2
    # print("bbox area", new_bbox_area, prev_bbox_area)                                                                                   
    if iou_area < 0:
        return 0
    # iou_percentage = abs(new_bbox_area - prev_bbox_area) * 100 / prev_bbox_area                                                         
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
