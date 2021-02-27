
def compute_iou(bbox1, bbox2):
    x11, y11, x12, y12 = bbox1
    x21, y21, x22, y22 = bbox1
    # finds iou points
    y1 = y11 if y11 > y21 else y21
    x1 = x11 if x11 > x21 else x21
    y2 = y12 if y12 < y22 else y22
    x2 = x12 if x12 < x22 else x22

    area = (x2 - x1) * (y2 - y1)
    return area

