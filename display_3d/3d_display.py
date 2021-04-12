import pygame
import pypangolin as pango
from OpenGL.GL import *
import numpy as np
import PIL
import cv2
from PIL import Image


def main():
    win = pango.CreateWindowAndBind("Visualization Tool 3d", 640, 480)
    glEnable(GL_DEPTH_TEST)

    # Define Projection and initial ModelView matrix

    # last param is like movement speed, find second last parameter meaning
    pm = pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.2, 100)

    # This allows changing of "camera" angle : glulookat style model view matrix (x, y, z, lx, ly, lz, AxisDirection Up) Forward is -z and up is +y
    mv = pango.ModelViewLookAt(-3, 0, -8,
                             0, 0, 0,
                             0, -1, 0)
    # mv = pango.ModelViewLookAt(10, 10, 20,
                             # 0, 0, 0,
                             # 0, -1, 0)
    # This is normal view of object
    # mv = pango.ModelViewLookAt(-0, 0.05, -3, 0, 0, 0, pango.AxisY) ## TODO: what is axis y and axis x
    s_cam = pango.OpenGlRenderState(pm, mv)

    ui_width = 180
    # Create Interactive View in window

    handler = pango.Handler3D(s_cam)
    d_cam = (
        pango.CreateDisplay()
        .SetBounds(
            pango.Attach(0),
            pango.Attach(1),
            pango.Attach.Pix(ui_width),
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
    # var_ui.an_int = (2, pango.VarMeta(0, 5))
    # var_ui.a_double_log = (3.0, pango.VarMeta(1, 1e4, logscale=True))
    # var_ui.a_checkbox = (False, pango.VarMeta(toggle=True))
    # var_ui.an_int_no_input = 2
    # var_ui.a_str = "sss"
    #
    # ctrl = -96
    # pango.RegisterKeyPressCallback(ctrl + ord("a"), a_callback)

    vid = cv2.VideoCapture("../Sidewalk.mp4")
    # texture_data = vid.read()[1]

    while not pango.ShouldQuit():
        # Clear screen and activate view to render into
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ret, texture_data = vid.read()
        texture_data = cv2.cvtColor(texture_data, cv2.COLOR_BGR2RGBA)
        texture_data = cv2.flip(texture_data, 1)
        height, width, _ = texture_data.shape

        glEnable(GL_TEXTURE_2D)
        texid = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        # if var_ui.a_checkbox:
        # var_ui.an_int = var_ui.a_double
        #
        # var_ui.an_int_no_input = var_ui.an_int

        d_cam.Activate(s_cam)
        cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1, 1,-1))
        cubeEdges = ((0.05),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
        cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0.05))


        glBegin(GL_QUADS)
        # for cubeQuad in cubeQuads:
        #     for cubeVertex in cubeQuad:
        #         glVertex3fv(cubeVertices[cubeVertex])
        # glTexCoord2f(0.0, 0.0)
        glVertex3f(-2, -2, 0.05)
        # glTexCoord2f(2, 0.0)
        glVertex3f(2, -2,  0.05)
        # glTexCoord2f(2, 2)
        glVertex3f(2,  2,  0.05)
        # glTexCoord2f(0.0, 2)
        glVertex3f(-2,  2, 0.05)
        glTexCoord2f(2, 0.0)
        glVertex3f(-2, -2, -0.05)
        glTexCoord2f(2, 2)
        glVertex3f(-2,  2, -0.05)
        glTexCoord2f(0.0, 2)
        glVertex3f(2,  2, -0.05)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(2, -2, -0.05)
        # glTexCoord2f(0.0, 2)
        glVertex3f(-2,  2, -0.05)
        # glTexCoord2f(0.0, 0.0)
        glVertex3f(-2,  2,  0.05)
        # glTexCoord2f(2, 0.0)
        glVertex3f(2,  2,  0.05)
        # glTexCoord2f(2, 2)
        glVertex3f(2,  2, -0.05)
        # glTexCoord2f(2, 2)
        glVertex3f(-2, -2, -0.05)
        # glTexCoord2f(0.0, 2)
        glVertex3f(2, -2, -0.05)
        # glTexCoord2f(0.0, 0.0)
        glVertex3f(2, -2, 0.05)
        # glTexCoord2f(2, 0.0)
        glVertex3f(-2, -2, 0.05)
        # glTexCoord2f(2, 0.0)
        glVertex3f(2, -2, -0.05)
        # glTexCoord2f(2, 2)
        glVertex3f(2,  2, -0.05)
        # glTexCoord2f(0.0, 2)
        glVertex3f(2,  2, 0.05)
        # glTexCoord2f(0.0, 0.0)
        glVertex3f(2, -2, 0.05)
        # glTexCoord2f(0.0, 0.0)
        glVertex3f(-2, -2, -0.05)
        # glTexCoord2f(2, 0.0)
        glVertex3f(-2, -2, 0.05)
        # glTexCoord2f(2, 2)
        glVertex3f(-2,  2, 0.05)
        # glTexCoord2f(0.0, 2)
        glVertex3f(-2,  2, -0.05)
        glEnd()
        # glBegin(GL_LINES)
        # for cubeEdge in cubeEdges:
        #     for cubeVertex in cubeEdge:
        #         glVertex3fv(cubeVertices[cubeVertex])
        # glEnd()

        # glColor3f(2.05.0.05.0)
        # Render OpenGL Cube
        # pango.glDrawColouredCube(5)

        # Swap Frames and Process Events
        pango.FinishFrame()

        glDeleteTextures(texid)


if __name__ == "__main__":
    main()
