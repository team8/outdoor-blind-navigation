
# Takes set of bboxes and id's them from frame to frame
def frame_object_mapper(prev_detections, new_detections):
    for i in prev_detections.getLast():
        for j in new_detections.getLast():
            if i[0] == j[0]:
                # if same object, compute iou
                compute_iou(i[2], j[2])


def compute_iou(orig_bbox, new_bbox):
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
    iou_area = (x2 - x1) * (y2 - y1)
    prev_bbox_area = w1 * h1
    new_bbox_area = w2 * h2
    # print("bbox area", new_bbox_area, prev_bbox_area)

    # iou_percentage = abs(new_bbox_area - prev_bbox_area) * 100 / prev_bbox_area
    iou_percentage = iou_area * 100 / prev_bbox_area
    return iou_percentage

