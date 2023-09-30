from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np


from OpenGL.arrays import vbo
from OpenGL.GL import shaders

T = 1
T2 = 1
T3 = 1


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    
    vertices_ovni = ovni.materials['Default_OBJ'].vertices_ovni
    vertices_ovni = np.array(vertices_ovni, dtype=np.float32).reshape(-1,6)
    vbo_ovni = vbo.VBO(vertices_ovni)

    

    glPushMatrix()
    glRotatef(T, 1.0, 0.0, 0.0)
    glRotatef(T2, 0.0, 1.0, 0.0)
    glRotatef(T3, 0.0, 0.0, 1.0)
    glScalef(1.0, 1.0, 1.0)
    
    glUseProgram(ovni_shader)
    vbo_ovni.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 24, vbo_ovni+12)
    glNormalPointer(GL_FLOAT, 24, vbo_ovni)
    glDrawArrays(GL_TRIANGLES, 0, vertices_ovni.shape[0])
    vbo_ovni.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glUseProgram(0)
    
    glPopMatrix()
    
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 10.0)
    glEnd()
  


    glutSwapBuffers()
    
# def Keys(key, x, y):
#     global T
#     global T2
#     global T3
    
#     if(key == GLUT_KEY_LEFT ): 
#         T -= 5 
#     elif(key == GLUT_KEY_RIGHT ): 
#         T += 5
#     elif(key == GLUT_KEY_UP ): 
#         T2 -= 5 
#     elif(key == GLUT_KEY_DOWN ): 
#         T2 += 5 
#     elif(key == GLUT_KEY_PAGE_UP ): 
#         T3 -= 5 
#     elif(key == GLUT_KEY_PAGE_DOWN ): 
#         T3 += 5         
       
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)
    
    
def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 3.0, 3.0,
                0.0, 0.0, 0.0,
                0.0, 1.0, 0.0)

  

def init():
    glClearColor (0.3, 0.3, 0.3, 0.0)
    glShadeModel( GL_SMOOTH )
    glClearColor( 0.0, 0.1, 0.0, 0.5 )
    glClearDepth( 1.0 )
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LEQUAL )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    
    vertexShader = shaders.compileShader(open('roda.vert', 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = shaders.compileShader(open('roda.frag', 'r').read(), GL_FRAGMENT_SHADER)

    global ovni_shader
    ovni_shader = glCreateProgram()
    glAttachShader(ovni_shader, vertexShader)
    glAttachShader(ovni_shader, fragmentShader)
    glLinkProgram(ovni_shader)
    

    

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Roda")
init()
ovni = pywavefront.Wavefront("Ovni.obj")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
# glutSpecialFunc(Keys)
glutMainLoop()
