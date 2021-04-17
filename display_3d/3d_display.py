import pygame
import pangolin as pango
from OpenGL.GL import *
import numpy as np
import PIL
import cv2
from PIL import Image


def main():
    win = pango.CreateWindowAndBind("Visualization Tool 3d", 640, 480)
    glEnable(GL_DEPTH_TEST)

    # Define Projection and initial ModelView matrix

    #   ProjectionMatrix (int w, int h, double fu, double fv, double u0, double v0, double zNear, double zFar)
    pm = pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.5, 100)

    # This allows changing of "camera" angle : glulookat style model view matrix (x, y, z, lx, ly, lz, AxisDirection Up) Forward is -z and up is +y
    # mv = pango.ModelViewLookAt(-1, 2, -2,
    # 0, 1, 0,
    # 0, -1, 0)
    # mv = pango.ModelViewLookAt(10, 10, 20,
    # 0, 0, 0,
    # 0, -1, 0)
    # This is normal view of object
    # mv = pango.ModelViewLookAt(-1, 0, 5, 0, 0, 0, pango.AxisY) ## TODO: what is axis y and axis x
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
            pango.Attach.Pix(1),  # side bar which can be used for notification system
            pango.Attach(1),
            -640.0 / 480.0,
        )
            .SetHandler(handler)
    )

    # pango.CreatePanel("ui").SetBounds(
    # pango.Attach(0), pango.Attach(1), pango.Attach(0), pango.Attach.Pix(ui_width)
    # )
    # var_ui = pango.Var("ui")
    # var_ui.a_Button = False
    # var_ui.a_double = (0.0, pango.VarMeta(0, 5))
    # var_ui.an_int = (5, pango.VarMeta(0, 5))
    # var_ui.a_double_log = (3.0, pango.VarMeta(1, 1e4, logscale=True))
    # var_ui.a_checkbox = (False, pango.VarMeta(toggle=True))
    # var_ui.an_int_no_input = 5
    # var_ui.a_str = "sss"
    #
    # ctrl = -96
    # pango.RegisterKeyPressCallback(ctrl + ord("a"), a_callback)

    vid = cv2.VideoCapture("../Sidewalk.mp4")
    # texture_data = vid.read()[1]
    while not pango.ShouldQuit():
        # Clear screen and activate view to render into
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.3, 0.3, 0.0)
        glLineWidth(5)
        glPointSize(15)
        pango.DrawLine([[-1, 1, 0], [-1, 1, -1]])  # down is positive y, right is positive x - this does bottom left
        pango.DrawLine([[1, -1, 0], [1, -1, -1]])  # top right
        pango.DrawLine([[-1, -1, 0], [-1, -1, -1]])  # top left
        pango.DrawLine([[1, 1, 0], [1, 1, -1]])  # bottom right
        pango.DrawPoints([[-1, 1, -1], [1, -1, -1], [-1, -1, -1], [1, 1, -1]])

        ret, texture_data = vid.read()
        texture_data = cv2.rotate(cv2.cvtColor(cv2.resize(texture_data, (1400, 1400)), cv2.COLOR_BGR2RGBA), cv2.ROTATE_180)
        height, width, _ = texture_data.shape

        glEnable(GL_TEXTURE_2D)
        texid = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

        d_cam.Activate(s_cam)

        glBegin(GL_QUADS)

        glVertex3f(1.0, 1.0, -0.05)
        glVertex3f(-1.0, 1.0, -0.05)
        glVertex3f(-1.0, 1.0, 0.05)
        glVertex3f(1.0, 1.0, 0.05)

        glVertex3f(1.0, -1.0, -0.05)
        glVertex3f(-1.0, -1.0, -0.05)
        glVertex3f(-1.0, -1.0, 0.05)
        glVertex3f(1.0, -1.0, 0.05)

        glVertex3f(1.0, 1.0, 0.05)
        glVertex3f(-1.0, 1.0, 0.05)
        glVertex3f(-1.0, -1.0, 0.05)
        glVertex3f(1.0, -1.0, 0.05)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(1.0, -1.0, -0.05)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0, -1.0, -0.05)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, 1.0, -0.05)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1.0, 1.0, -0.05)

        glVertex3f(-1.0, 1.0, 0.05)
        glVertex3f(-1.0, 1.0, -0.05)
        glVertex3f(-1.0, -1.0, -0.05)
        glVertex3f(-1.0, -1.0, 0.05)

        glVertex3f(1.0, 1.0, 0.05)
        glVertex3f(1.0, 1.0, -0.05)
        glVertex3f(1.0, -1.0, -0.05)
        glVertex3f(1.0, -1.0, 0.05)

        glEnd()

        # glBegin(GL_LINES)
        # for cubeEdge in cubeEdges:
        #     for cubeVertex in cubeEdge:
        #         glVertex3fv(cubeVertices[cubeVertex])
        # glEnd()
        #

        # Swap Frames and Process Events
        pango.FinishFrame()

        glDeleteTextures(texid)


if __name__ == "__main__":
    main()
