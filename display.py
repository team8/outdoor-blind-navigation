import sys
import cv2
import math
class Display:
    # dimension can be 3d or 2d
    def __init__(self, dimension=3):
        self.dimension = dimension
        if self.dimension == 3:
            # initialize pangolin opengl 3d viewer
            print("Initializing pangolin opengl 3d viewer")

            win = pango.CreateWindowAndBind("Visualization Tool 3d", 640, 480)
            glEnable(GL_DEPTH_TEST)

            # Define Projection and initial ModelView matrix

            #   ProjectionMatrix (int w, int h, double fu, double fv, double u0, double v0, double zNear, double zFar)
            pm = pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.5, 100)

            # This allows changing of "camera" angle : glulookat style model view matrix (x, y, z, lx, ly, lz, AxisDirection Up) Forward is -z and up is +y
            mv = pango.ModelViewLookAt(-1.5, 0, -1,
                                       0.25, 0.75, 0,
                                       0, -1, 0)

            '''
            The gluLookAt function provides an easy and intuitive way to set the camera position and orientation. Basically it has three groups of parameters, each one is composed of 3 floating point values. The first three values indicate the camera position. The second set of values defines the point we’re looking at. Actually it can be any point in our line of sight.The last group indicates the up vector, this is usually set to (0.0, 1.0, 0.0), meaning that the camera’s is not tilted. If you want to tilt the camera just play with these values. For example, to see everything upside down try (0.0, -1.0, 0.0).
            '''

            s_cam = pango.OpenGlRenderState(pm, mv)

            # Create Interactive View in window
            handler = pango.Handler3D(s_cam)
            d_cam = (
                pango.CreateDisplay()
                .SetBounds(
                    pango.Attach(0),
                    pango.Attach(1),
                    pango.Attach.Pix(1), # side bar which can be used for notification system
                    pango.Attach(1),
                    -640.0 / 480.0,
                )
                .SetHandler(handler)
            )
            glLineWidth(5)
            glPointSize(15)
        elif self.dimension == 2:
            # initialize cv2 2d viewer
            print("Initializing cv2 2d viewer")
        else:
            raise Exception("Dimension for viewing tool must be either 2 or 3")
    def putVideoFrame(self,orig_cap):
        self.frame = cv2.resize(orig_cap, (720, 540))
    def putSidewalkState(self, state):
        # nolan this is yours
    def putObjects(self, obstacles):
        # this is yours as well

    def displayScreen(self):
        if self.dimension == 3:
            # pangolin texture update
        else:
            # nolan just do cv2 imshow
        # just use cv2.imshow here nolan
