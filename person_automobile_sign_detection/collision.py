# Checks for collision

'''
Check if arrow is inside collision ROI region
Check if arrow pointing toward center of image as opposed to away from person (even if in collision ROI)
Check if same object has been in collision roi before

Perhaps move to object detector stuffs so you get detection instance to play with

'''
import math

collision_ROI = [[0.4, -0.2, -0.15], [0.6, 0.8, -0.15], [-0.6, 0.8, -0.15], [-0.4, -0.2, -0.15], [0.4, -0.2, -0.15]] # in opengl 3d coordinate system [-1, 1] in both x and y axis. bottom right hand corner is (1, 1). Toward self is negative, away is positive for z pos. Points go cyclicly from top right to bottom right to bottom left to top left back to top right
areaROI = (collision_ROI[1][1] - collision_ROI[0][1]) * ((collision_ROI[1][0] - collision_ROI[2][0]) + (collision_ROI[4][0] - collision_ROI[3][0]))/2

#
# # Test Cases
# def __area_triangle(pt1, pt2, pt3):
#     return round(abs(0.5 * (pt1[0] * (pt2[1] - pt3[1]) + pt2[0] * (pt3[1] - pt1[1]) + pt3[0] * (pt1[1] - pt2[1]))) * 10, 3) / 10
# # print(sum([__area_triangle((0, 0, 0), collision_ROI[i], collision_ROI[i+1]) for i in range(0, len(collision_ROI) - 1)]))
# inside_roi = True if areaROI == sum([__area_triangle((0, 0, 0), collision_ROI[i], collision_ROI[i+1]) for i in range(0, len(collision_ROI) - 1)]) else False
# print("0, 0, 0", inside_roi)
# inside_roi = True if areaROI == sum([__area_triangle((0.1, 0.1, 0), collision_ROI[i], collision_ROI[i+1]) for i in range(0, len(collision_ROI) - 1)]) else False
#

viewer3d_size = None
viewer3d_stretch = None

def set_constants(size, stretch):
    global viewer3d_size
    global viewer3d_stretch
    viewer3d_size = size
    viewer3d_stretch = stretch

def is_colliding(detection):
    if detection["label"] == "person" or detection["label"] == "car":
        x_offset, y_offset, z_offset = detection["mdv"]
        x_anchor, y_anchor, w, h = detection["bbox"]
        x_offset = (x_offset * viewer3d_stretch[0] / viewer3d_size[0])
        y_offset = (y_offset * viewer3d_stretch[1] / viewer3d_size[1])
        x_anchor = (x_anchor * viewer3d_stretch[0] / viewer3d_size[0]) * 2 - 1
        y_anchor = (y_anchor * viewer3d_stretch[1] / viewer3d_size[1]) * 2 - 1
        wanted_z_anchor = -(z_offset)
        # z_anchor = min(math.sqrt(1 - x_offset**2 - y_offset**2) * wanted_z_anchor, 0.5)
        z_anchor = math.sqrt(1 - x_offset**2 - y_offset**2) * wanted_z_anchor
        pointing_toward_center = True if math.ceil(abs(x_offset + x_anchor) * 10) < math.floor(abs(x_offset) * 10) else False # TODO: enhance this alg
        inside_roi = True if abs(areaROI - sum([__area_triangle((x_anchor + x_offset, y_anchor + y_offset, z_anchor), collision_ROI[i], collision_ROI[i+1]) for i in range(0, len(collision_ROI) - 1)])) < 0.01 and all(z_anchor <= z[2] for z in collision_ROI) else False # using inside polygon alg where area taken from central point to pairs of 2 corner points (creating triangle) and taking summation of area of all triangles and comparing to original area of trapezoid
        # inside_roi = True if abs(areaROI - sum([__area_triangle((x_anchor + x_offset, y_anchor + y_offset, z_anchor), collision_ROI[i], collision_ROI[i+1]) for i in range(0, len(collision_ROI) - 1)])) < 0.01 else False # using inside polygon alg where area taken from central point to pairs of 2 corner points (creating triangle) and taking summation of area of all triangles and comparing to original area of trapezoid
        if inside_roi:
            return True
        return False
            # print(detection[0], (x_anchor + x_offset, y_anchor + y_offset, z_anchor))
def __area_triangle(pt1, pt2, pt3):
    return abs(0.5 * (pt1[0] * (pt2[1] - pt3[1]) + pt2[0] * (pt3[1] - pt1[1]) + pt3[0] * (pt1[1] - pt2[1])))
