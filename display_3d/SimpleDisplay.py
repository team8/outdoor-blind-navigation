import pygame
import pypangolin as pango
from OpenGL.GL import *
import cv2

def main():
    win = pango.CreateWindowAndBind("pySimpleDisplay", 640, 480)
    glEnable(GL_DEPTH_TEST)


    # Define Projection and initial ModelView matrix

    # last param is like movement speed, find second last parameter meaning
    pm = pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.2, 100)

    # This allows changing of "camera" angle
    mv = pango.ModelViewLookAt(0, -10, -8,
                             0, 0, 0,
                             0, -1, 0)

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

    textureSurface = pygame.image.load('test_image.jpg')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    # vid = cv2.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk_Compressed.mp4")
    # textureData = vid.read()[1]
    # textureData = cv2.resize(cv2.imread("test_image.jpg"), (500, 500))
    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    while not pango.ShouldQuit():
        # Clear screen and activate view to render into
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

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
        glVertex3f(-0.5, -0.5, 0.05)
        # glTexCoord2f(0.5, 0.0)
        glVertex3f(0.5, -0.5,  0.05)
        # glTexCoord2f(0.5, 0.5)
        glVertex3f(0.5,  0.5,  0.05)
        # glTexCoord2f(0.0, 0.5)
        glVertex3f(-0.5,  0.5, 0.05)
        glTexCoord2f(0.5, 0.0)
        glVertex3f(-0.5, -0.5, -0.05)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(-0.5,  0.5, -0.05)
        glTexCoord2f(0.0, 0.5)
        glVertex3f(0.5,  0.5, -0.05)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5, -0.5, -0.05)
        # glTexCoord2f(0.0, 0.5)
        glVertex3f(-0.5,  0.5, -0.05)
        # glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5,  0.5,  0.05)
        # glTexCoord2f(0.5, 0.0)
        glVertex3f(0.5,  0.5,  0.05)
        # glTexCoord2f(0.5, 0.5)
        glVertex3f(0.5,  0.5, -0.05)
        # glTexCoord2f(0.5, 0.5)
        glVertex3f(-0.5, -0.5, -0.05)
        # glTexCoord2f(0.0, 0.5)
        glVertex3f(0.5, -0.5, -0.05)
        # glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5, -0.5, 0.05)
        # glTexCoord2f(0.5, 0.0)
        glVertex3f(-0.5, -0.5, 0.05)
        # glTexCoord2f(0.5, 0.0)
        glVertex3f(0.5, -0.5, -0.05)
        # glTexCoord2f(0.5, 0.5)
        glVertex3f(0.5,  0.5, -0.05)
        # glTexCoord2f(0.0, 0.5)
        glVertex3f(0.5,  0.5, 0.05)
        # glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5, -0.5, 0.05)
        # glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.05)
        # glTexCoord2f(0.5, 0.0)
        glVertex3f(-0.5, -0.5, 0.05)
        # glTexCoord2f(0.5, 0.5)
        glVertex3f(-0.5,  0.5, 0.05)
        # glTexCoord2f(0.0, 0.5)
        glVertex3f(-0.5,  0.5, -0.05)
        glEnd()
        # glBegin(GL_LINES)
        # for cubeEdge in cubeEdges:
        #     for cubeVertex in cubeEdge:
        #         glVertex3fv(cubeVertices[cubeVertex])
        # glEnd()

        # glColor3f(0.5.05.0.05.0)
        # Render OpenGL Cube
        # pango.glDrawColouredCube(5)

        # Swap Frames and Process Events
        pango.FinishFrame()


if __name__ == "__main__":
    main()
