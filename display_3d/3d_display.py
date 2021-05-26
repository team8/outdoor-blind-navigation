import pygame
import pangolin as pango
from OpenGL.GL import *
import numpy as np
import PIL
import cv2
from PIL import Image


def main():
    win = pango.CreateWindowAndBind("Visualization Tool 3d", 640 * 2, 480 * 2)
    glEnable(GL_DEPTH_TEST)

    # Define Projection and initial ModelView matrix

    #   ProjectionMatrix (int w, int h, double fu, double fv, double u0, double v0, double zNear, double zFar)
    pm = pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.5, 100)

    # This allows changing of "camera" angle : glulookat style model view matrix (x, y, z, lx, ly, lz, AxisDirection
    # Up) Forward is -z and up is +y
    # mv = pango.ModelViewLookAt(-1, 2, -2,
    # 0, 1, 0,
    # 0, -1, 0)
    # mv = pango.ModelViewLookAt(10, 10, 20,
    # 0, 0, 0,
    # 0, -1, 0)
    # This is normal view of object
    # mv = pango.ModelViewLookAt(-1, 0, 5, 0, 0, 0, pango.AxisY) ## TODO: what is axis y and axis x
    mv = pango.ModelViewLookAt(0.3, 0, -2.5,
                               0, 0, 0,
                               0, -0.5, 0)

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

    vid = cv2.VideoCapture("../Sidewalk.mp4")
    # texture_data = vid.read()[1]
    pbo = 0
    pbo = glGenBuffers(1, pbo)
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
        texture_data = cv2.rotate(cv2.cvtColor(cv2.resize(texture_data, (1400, 1400)), cv2.COLOR_BGR2RGBA),
                                  cv2.ROTATE_180)
        height, width, dims = texture_data.shape

        glEnable(GL_TEXTURE_2D)

        size = (height * width * dims)
        glBindBuffer(GL_PIXEL_PACK_BUFFER, pbo)
        glBufferData(GL_PIXEL_PACK_BUFFER,
                     size,
                     texture_data,
                     GL_DYNAMIC_DRAW)

        draw_rect()

        d_cam.Activate(s_cam)

        # Swap Frames and Process Events
        pango.FinishFrame()


def draw_rect():
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


if __name__ == "__main__":
    main()
