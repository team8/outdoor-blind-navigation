# Checks for collision 

'''
Check if arrow is inside collision ROI region
Check if arrow pointing toward center of image as opposed to away from person (even if in collision ROI)
Check if same object has been in collision roi before

Perhaps move to object detector stuffs so you get detection instance to play with

'''
import math

collisionROI = [[0.4, -0.2, -0.3], [0.6, 0.8, -0.3], [-0.6, 0.8, -0.3], [-0.4, -0.2, -0.3], [0.4, -0.2, -0.3]] # in opengl 3d coordinate system [-1, 1] in both x and y axis. bottom right hand corner is (1, 1). Toward self is negative, away is positive for z pos. Points go cyclicly from top right to bottom right to bottom left to top left back to top right
areaROI = (collisionROI[1][1] - collisionROI[0][1]) * ((collisionROI[1][0] - collisionROI[2][0]) + (collisionROI[4][0] - collisionROI[3][0]))/2

# Test Cases
def __area_triangle(pt1, pt2, pt3):
    return round(abs(0.5 * (pt1[0] * (pt2[1] - pt3[1]) + pt2[0] * (pt3[1] - pt1[1]) + pt3[0] * (pt1[1] - pt2[1]))) * 10, 3) / 10
# print(sum([__area_triangle((0, 0, 0), collisionROI[i], collisionROI[i+1]) for i in range(0, len(collisionROI) - 1)]))
inside_roi = True if areaROI == sum([__area_triangle((0, 0, 0), collisionROI[i], collisionROI[i+1]) for i in range(0, len(collisionROI) - 1)]) else False
print("0, 0, 0", inside_roi)
inside_roi = True if areaROI == sum([__area_triangle((0.1, 0.1, 0), collisionROI[i], collisionROI[i+1]) for i in range(0, len(collisionROI) - 1)]) else False


class CollisionDetector:
    def __init__(self, viewer3d_size, viewer3d_stretch):
        self.viewer3d_size = viewer3d_size
        self.viewer3d_stretch = viewer3d_stretch
    def findCollisions(self, detections):
        collision_detections = []
        for detection in detections:
            if detection[0] == "person" or detection[0] == "car":
                x_offset, y_offset, z_offset = detection[4]
                x_anchor, y_anchor, w, h = detection[2]
                x_offset = (x_offset * self.viewer3d_stretch[0] / self.viewer3d_size[0])
                y_offset = (y_offset * self.viewer3d_stretch[1] / self.viewer3d_size[1])
                x_anchor = (x_anchor * self.viewer3d_stretch[0] / self.viewer3d_size[0]) * 2 - 1
                y_anchor = (y_anchor * self.viewer3d_stretch[1] / self.viewer3d_size[1]) * 2 - 1

                wanted_z_anchor = (abs(z_offset) - 1) * 0.5
                z_anchor = min(math.sqrt(1 - x_offset**2 - y_offset**2) * wanted_z_anchor, 0.5)
                pointing_toward_center = True if math.ceil(abs(x_offset + x_anchor) * 10) < math.floor(abs(x_offset) * 10) else False # TODO: enhance this alg
                inside_roi = True if abs(areaROI - sum([self.__area_triangle((x_anchor + x_offset, y_anchor + y_offset, z_anchor), collisionROI[i], collisionROI[i+1]) for i in range(0, len(collisionROI) - 1)])) < 0.01 and all(z_anchor <= z[2] for z in collisionROI) else False # using inside polygon alg where area taken from central point to pairs of 2 corner points (creating triangle) and taking summation of area of all triangles and comparing to original area of trapezoid
                # inside_roi = True if abs(areaROI - sum([self.__area_triangle((x_anchor + x_offset, y_anchor + y_offset, z_anchor), collisionROI[i], collisionROI[i+1]) for i in range(0, len(collisionROI) - 1)])) < 0.01 else False # using inside polygon alg where area taken from central point to pairs of 2 corner points (creating triangle) and taking summation of area of all triangles and comparing to original area of trapezoid
                if inside_roi:
                    collision_detections.append(detection)
                    # print(detection[0], (x_anchor + x_offset, y_anchor + y_offset, z_anchor))
        return collision_detections

    def __area_triangle(self, pt1, pt2, pt3):
        return abs(0.5 * (pt1[0] * (pt2[1] - pt3[1]) + pt2[0] * (pt3[1] - pt1[1]) + pt3[0] * (pt1[1] - pt2[1])))
