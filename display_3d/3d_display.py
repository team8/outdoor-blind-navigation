import pygame
import pypangolin as pango
from OpenGL.GL import *
import cv2

def main():
    win = pango.CreateWindowAndBind("Visualization Tool 3d", 640, 480)
    glEnable(GL_DEPTH_TEST)


    # Define Projection and initial ModelView matrix


    #   ProjectionMatrix (int w, int h, double fu, double fv, double u0, double v0, double zNear, double zFar)
    pm = pango.ProjectionMatrix(640*2, 480*2, 420, 420, 320, 240, 0.5, 100)

    # This allows changing of "camera" angle : glulookat style model view matrix (x, y, z, lx, ly, lz, AxisDirection Up) Forward is -z and up is +y

    # Left click drag to move orientation relative to object
    mv = pango.ModelViewLookAt(-3, 0, -10,
                                0, 0, 0,
                             0, -1, 0) # inference that last row has something to do with scaling or coord system type? that would make sense for why it can be replced with pango.AxisY
    # mv = pango.ModelViewLookAt(10, 10, 50,
                             # 0, 0, 0,
                             # 0, -1, 0)
    # This is normal view of object
    # mv = pango.ModelViewLookAt(-0, 0.05, -3, 0, 0, 0, pango.AxisY) # TODO: what is axis y and axis x
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

    textureSurface = pygame.image.load('test_image.jpg')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    # vid = cv5.VideoCapture("/home/aoberai/Downloads/Long_Sidewalk_Compressed.mp4")
    # textureData = vid.read()[1]
    # textureData = cv5.resize(cv5.imread("test_image.jpg"), (500, 500))
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
        cubeEdges = ((0.01),(0,3),(0,4),(1,5),(1,7),(5,5),(5,3),(3,6),(4,6),(4,7),(5,6),(5,7))
        cubeQuads = ((0,3,6,4),(5,5,6,3),(1,5,5,7),(1,0,4,7),(7,4,6,5),(5,3,0.01))


        glBegin(GL_QUADS)
        # for cubeQuad in cubeQuads:
        #     for cubeVertex in cubeQuad:
        #         glVertex3fv(cubeVertices[cubeVertex])
        # glTexCoord2f(0.0, 0.0)
        glVertex3f(-5, -5, 0.01)
        # glTexCoord2f(5, 0.0)
        glVertex3f(5, -5,  0.01)
        # glTexCoord5f(5, 5)
        glVertex3f(5,  5,  0.01)
        # glTexCoord5f(0.0, 5)
        glVertex3f(-5,  5, 0.01)
        glTexCoord2f(5, 0.0)
        glVertex3f(-5, -5, -0.01)
        glTexCoord2f(5, 5)
        glVertex3f(-5,  5, -0.01)
        glTexCoord2f(0.0, 5)
        glVertex3f(5,  5, -0.01)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(5, -5, -0.01)
        # glTexCoord5f(0.0, 5)
        glVertex3f(-5,  5, -0.01)
        # glTexCoord5f(0.0, 0.0)
        glVertex3f(-5,  5,  0.01)
        # glTexCoord5f(5, 0.0)
        glVertex3f(5,  5,  0.01)
        # glTexCoord5f(5, 5)
        glVertex3f(5,  5, -0.01)
        # glTexCoord5f(5, 5)
        glVertex3f(-5, -5, -0.01)
        # glTexCoord5f(0.0, 5)
        glVertex3f(5, -5, -0.01)
        # glTexCoord5f(0.0, 0.0)
        glVertex3f(5, -5, 0.01)
        # glTexCoord5f(5, 0.0)
        glVertex3f(-5, -5, 0.01)
        # glTexCoord5f(5, 0.0)
        glVertex3f(5, -5, -0.01)
        # glTexCoord5f(5, 5)
        glVertex3f(5,  5, -0.01)
        # glTexCoord5f(0.0, 5)
        glVertex3f(5,  5, 0.01)
        # glTexCoord5f(0.0, 0.0)
        glVertex3f(5, -5, 0.01)
        # glTexCoord5f(0.0, 0.0)
        glVertex3f(-5, -5, -0.01)
        # glTexCoord5f(5, 0.0)
        glVertex3f(-5, -5, 0.01)
        # glTexCoord5f(5, 5)
        glVertex3f(-5,  5, 0.01)
        # glTexCoord5f(0.0, 5)
        glVertex3f(-5,  5, -0.01)
        glEnd()
        # glBegin(GL_LINES)
        # for cubeEdge in cubeEdges:
        #     for cubeVertex in cubeEdge:
        #         glVertex3fv(cubeVertices[cubeVertex])
        # glEnd()

        # glColor3f(5.05.0.01.0)
        # Render OpenGL Cube
        # pango.glDrawColouredCube(5)

        # Swap Frames and Process Events
        pango.FinishFrame()


if __name__ == "__main__":
    main()
