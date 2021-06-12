import cv2
import math
import pangolin as pango
from OpenGL.GL import *
import numpy as np
import cv2
from PIL import Image
import person_automobile_sign_detection.collision as collision


class Display:
    # dimension can be 2 or 3
    def __init__(self, dimension=3, size=(720, 540), bbox_inference_coord_size=(618, 618)):
        global viewer_size
        global stretch
        self.dimension = dimension
        self.viewer_size = size
        self.bbox_inference_coord_size = bbox_inference_coord_size
        self.stretchXValue = self.viewer_size[0]/self.bbox_inference_coord_size[0]
        self.stretchYValue = self.viewer_size[1]/self.bbox_inference_coord_size[1]
        self.stretch = (self.stretchXValue, self.stretchYValue)
        self.labelToColor = {"stop sign": ((0, 0, 255)),
                             "person": ((0, 255, 0)),
                             "car": ((255, 0, 0)),
                             "bicycle": ((255, 255, 0)),
                             "traffic light": ((255, 0, 255)),
                             "fire hydrant": ((0, 255, 255)),
                             "bench": ((200, 100, 200))}

        self.rightArrow = Image.open("./display_resources/RightExpanded.png")
        self.leftArrow = Image.open("./display_resources/LeftExpanded.png")
        self.forwardArrow = Image.open("./display_resources/ForwardExpanded.png")
        self.view_mode = 0
        self.t = 0
        self.tX = 0
        self.tY = 0

        if self.dimension == 3:
            print("Initializing pangolin opengl 3d viewer")

            self.win = pango.CreateWindowAndBind("Visualization Tool 3d", size[0], size[1])
            glEnable(GL_DEPTH_TEST)

            # Definition of Projection and initial ModelView matrices

            # ProjectionMatrix (int w, int h, double fu, double fv, double u0, double v0, double zNear, double zFar)
            self.pm = pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.5, 100)

            # This allows changing of "camera" angle : glulookat style model view matrix (x, y, z, lx, ly, lz, AxisDirection Up) Forward is -z and up is +y
            self.mv = pango.ModelViewLookAt(0.3, 0, -2.5,
                                            0, 0, 0,
                                            0, -1, 0)
            '''
            The gluLookAt function provides an easy and intuitive way to set the camera position and orientation. Basically it has three groups of parameters, each one is composed of 3 floating point values. The first three values indicate the camera position. The second set of values defines the point we’re looking at. Actually it can be any point in our line of sight.The last group indicates the up vector, this is usually set to (0.0, 1.0, 0.0), meaning that the camera’s is not tilted. If you want to tilt the camera just play with these values. For example, to see everything upside down try (0.0, -1.0, 0.0).
            '''

            self.s_cam = pango.OpenGlRenderState(self.pm, self.mv)

            # Create Interactive View in window
            self.handler = pango.Handler3D(self.s_cam)
            self.d_cam = (
                pango.CreateDisplay()
                    .SetBounds(
                    pango.Attach(0),
                    pango.Attach(1),
                    pango.Attach.Pix(1),  # side bar which can be used for notification system; not used right now
                    pango.Attach(1),
                    -640.0 / 480.0,
                )
                    .SetHandler(self.handler)
            )

            panel = pango.CreatePanel('ui')
            panel.SetBounds(0.0, 1.0, 0.0, 60 / 640.)
            self.checkBox = pango.VarBool('ui.N', value=True, toggle=True)
            self.xspeed = pango.VarFloat('ui.sX', value=False, toggle=False)
            self.yspeed = pango.VarFloat('ui.sY', value=False, toggle=False)
            self.stop = pango.VarBool('ui.Stop Sign', value=False, toggle=True)
            self.person = pango.VarBool('ui.Person', value=False, toggle=True)
            self.car = pango.VarBool('ui.Car', value=False, toggle=True)
            self.cperson = pango.VarBool('ui.Person Collision', value=False, toggle=True)
            self.ccar = pango.VarBool('ui.Car Collision', value=False, toggle=True)
            self.tright = pango.VarBool('ui.Turn Right', value=False, toggle=True)
            self.tleft = pango.VarBool('ui.Turn Left', value=False, toggle=True)
            self.sright = pango.VarBool('ui.Shift Right', value=False, toggle=True)
            self.sleft = pango.VarBool('ui.Shift Left', value=False, toggle=True)

            glPointSize(15)
            # pango.RegisterKeyPressCallback(int(pango.PANGO_CTRL) + ord('r'), self.rehome3dViewer()) # Key press with panfolin for rehoming is broken - use different key press lib
            # glTranslatef(0.0, 0.0, -10)
        elif self.dimension == 2:
            print("Initializing cv2 2d viewer")
        else:
            raise Exception("Dimension for viewing tool must be either 2 or 3")

    def putVideoFrame(self, orig_cap):
        self.frame = cv2.resize(orig_cap, self.viewer_size)

    def putSidewalkState(self, state):
        if state == "Left of Sidewalk":
            self.__showLeftArrow()
        if state == "Middle of Sidewalk":
            self.__showForwardArrow()
        if (state == "Right of Sidewalk"):
            self.__showRightArrow()

    def view(self):
        self.mv = pango.ModelViewLookAt(math.cos(self.tX), math.sin(self.tY), -2.5,
                                        0, 0, 0,
                                        0, -1, 0)

        self.s_cam = pango.OpenGlRenderState(self.pm, self.mv)
        # Create Interactive View in window
        self.handler = pango.Handler3D(self.s_cam)
        self.tX += self.xspeed.Get() / 10
        self.tY += self.yspeed.Get() / 10

    def view_n(self):
        self.mv = pango.ModelViewLookAt(0, 0, -2.5,
                                        0, 0, 0,
                                        0, -1, 0)

        self.s_cam = pango.OpenGlRenderState(self.pm, self.mv)
        # Create Interactive View in window
        self.handler = pango.Handler3D(self.s_cam)

        self.tX = 0
        self.tY = 0

    def displayScreen(self):
        if self.dimension == 3:
            glEnable(GL_TEXTURE_2D)
            self.texid = glGenTextures(1)

            if not pango.ShouldQuit():
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glClearColor(0.5, 0.7, 0.7, 0.0)
                glLineWidth(5)

                # Generates and applies texture for canvas
                texture_data = cv2.rotate(cv2.cvtColor(cv2.resize(self.frame, (1400, 1400)), cv2.COLOR_BGR2RGBA),
                                          cv2.ROTATE_180)
                height, width, _ = texture_data.shape

                glBindTexture(GL_TEXTURE_2D, self.texid)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                             0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
                glBindTexture(GL_TEXTURE_2D, 0)

                self.d_cam.Activate(self.s_cam)
                glColor3f(0.0, 0.0, 0.0)

                if self.checkBox.Get() and self.view_mode != 0:
                    self.view_n()
                    self.view_mode = 0
                elif not self.checkBox.Get():
                    self.view_mode = 1
                    self.view()

                self.__drawCanvas((1, 1.0, 0.025), (-1, -1.0, 0))  # Draws 3d canvas
                self.__putMovementDirectionVectors()  # Draws arrows on 3d viewer for movement direction vector of objects
                # self.__put_statuses({"person": False, "stop sign": False, "car": True, "turn left": False, "turn right": False, "shift right": False, "shift left": False, "person collision": False, "car collision": True})
                self.__putCollisionROI()
                self.t += 0.05
                # Swap Frames and Process Events
                pango.FinishFrame()

            glDeleteTextures(self.texid)
        else:
            cv2.imshow("2d visualizer", self.frame)
            cv2.waitKey(1)

    def putState(self, map):
        self.person.SetVal(map["person"])
        self.car.SetVal(map["car"])
        self.cperson.SetVal(map["person collision"])
        self.ccar.SetVal(map["car collision"])
        self.stop.SetVal(map["stop sign"])
        self.tright.SetVal(map["turn left"])
        self.tleft.SetVal(map["turn right"])
        self.sright.SetVal(map["shift right"])
        self.sleft.SetVal(map["shift left"])

    def __rehome3dViewer(self):
        print("Resetting cam position")
        # self.s_cam = pango.OpenGlRenderState(self.pm, self.mv)
        # # Create Interactive View in window
        # self.handler = pango.Handler3D(self.s_cam)

    def __drawCanvas(self, p1, p2):
        x1, y1, z1 = p1
        x2, y2, z2 = p2

        # z axis (-) is toward self, down is positive y, right is positive x
        pango.DrawLine([[x2, y1, z1], [x2, y1, z1 - 0.3]])  # bottom left
        pango.DrawLine([[x1, y2, z1], [x1, y2, z1 - 0.3]])  # top right
        pango.DrawLine([[x2, y2, z1], [x2, y2, z1 - 0.3]])  # top left
        pango.DrawLine([[x1, y1, z1], [x1, y1, z1 - 0.3]])  # bottom right
        pango.DrawPoints([[x2, y1, z1 - 0.3], [x1, y2, z1 - 0.3], [x2, y2, z1 - 0.3], [x1, y1, z1 - 0.3]])

        glColor3f(1.0, 1.0, 1.0)

        glBindTexture(GL_TEXTURE_2D, self.texid)

        glBegin(GL_QUADS)

        glVertex3f(x1, y1, z2)
        glVertex3f(x2, y1, z2)
        glVertex3f(x2, y1, z1)
        glVertex3f(x1, y1, z1)

        glVertex3f(x1, y2, z2)
        glVertex3f(x2, y2, z2)
        glVertex3f(x2, y2, z1)
        glVertex3f(x1, y2, z1)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(x1, y1, z1)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x2, y1, z1)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x2, y2, z1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x1, y2, z1)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(x1, y2, z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x2, y2, z2)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x2, y1, z2)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x1, y1, z2)

        glVertex3f(x2, y1, z1)
        glVertex3f(x2, y1, z2)
        glVertex3f(x2, y2, z2)
        glVertex3f(x2, y2, z1)

        glVertex3f(x1, y1, z1)
        glVertex3f(x1, y1, z2)
        glVertex3f(x1, y2, z2)
        glVertex3f(x1, y2, z1)

        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)

    def __putMovementDirectionVectors(self):
        glLineWidth(3)
        if self.obstacles is not None:
            for detection in self.obstacles:
                if detection["label"] == "person" or detection["label"] == "car":
                    if detection["colliding"] == True:
                        glColor3f(1, 0.5, 0.25)
                    x_offset, y_offset, z_offset = detection["mdv"]
                    x_anchor, y_anchor, w, h = detection["bbox"]
                    x_offset = (x_offset * self.stretchXValue / self.viewer_size[0])
                    y_offset = (y_offset * self.stretchYValue / self.viewer_size[1])
                    x_anchor = (x_anchor * self.stretchXValue / self.viewer_size[0]) * 2 - 1
                    y_anchor = (y_anchor * self.stretchYValue / self.viewer_size[1]) * 2 - 1

                    wanted_z_anchor = -abs(z_offset)
                    z_anchor = max(math.sqrt(1 - x_offset**2 - y_offset**2) * wanted_z_anchor, -0.5) if detection["colliding"] == False else min(math.sqrt(1 - x_offset**2 - y_offset**2) * wanted_z_anchor, -collision.collisionROI[0][2] - 0.2)
                    # z axis (+)  is toward self
                    pango.DrawLine([[x_anchor, y_anchor, 0], [x_anchor + x_offset, y_anchor + y_offset,
                                                              z_anchor]])  # down is positive y, right is positive x - this does bottom left

                    pango.DrawPoints([[x_anchor + x_offset, y_anchor + y_offset, z_anchor]])

                    if detection["colliding"] == True:
                        glColor3f(1, 1, 1)

    def __putCollisionROI(self):
        collisionROI = collision.collisionROI
        for i in range(0, len(collisionROI) - 1):
           pango.DrawLine([collisionROI[i], collisionROI[i+1]])

    def putObjects(self, obstacles):
        self.obstacles = obstacles
        if obstacles is None:
            return
        for detection in obstacles:
            if detection["label"] in self.labelToColor.keys():
                self.frame = self.__displayObjects(detection)

    def __displayObjects(self, objectInfo):
        x, y, w, h = objectInfo["bbox"]
        x *= self.stretchXValue
        y *= self.stretchYValue
        w *= self.stretchXValue
        h *= self.stretchYValue
        lineLengthWeightage = 2
        centerX = x
        centerY = y + (h / 2) + 15
        if (centerY + 15 >= self.viewer_size[1]):
            centerY = y - (h / 2) - 15
        self.rect = cv2.rectangle(self.frame, (int(x - (w / 2)), int(y - (h / 2))), (int(x + (w / 2)), int(y + (h / 2))), self.labelToColor[objectInfo["label"]], lineLengthWeightage)
        font = cv2.FONT_HERSHEY_SIMPLEX
        shownText = objectInfo["label"].replace("sign", "") + " ID: " + str(objectInfo["id"])
        textsize = cv2.getTextSize(shownText, font, 0.5, 2)[0]
        cv2.putText(self.frame, shownText, (int(centerX - (textsize[0] / 2)), int(centerY)), font, 0.7, (255, 255, 255),
                    2, cv2.LINE_AA)
        return self.frame

    def __pilToOpenCV(self, pil_image):
        return np.array(pil_image)

    def __openCVToPil(self, cv_image):
        im_pil = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_RGB2RGBA))
        return im_pil

    def transposeImageSrc(self, arrow):
        src = self.__openCVToPil(self.frame)
        img = arrow.resize(src.size)
        img = Image.alpha_composite(src, img)
        imcv = self.__pilToOpenCV(img)
        return imcv

    def __showLeftArrow(self):
        self.frame = self.transposeImageSrc(self.rightArrow)

    def __showForwardArrow(self):
        self.frame = self.transposeImageSrc(self.forwardArrow)

    def __showRightArrow(self):
        self.frame = self.transposeImageSrc(self.leftArrow)

    def getStretchFactor(self):
        return self.stretch
    def getViewerSize(self):
        return self.viewer_size


