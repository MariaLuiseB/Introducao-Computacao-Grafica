from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization

T = 0
T2 = 0
T3 = 0


# -------------- Desenha o Jogo --------------
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    
    glPushMatrix()
    # Ações em toda a nave
    glRotatef(0.0, 0.0, 0.0, 0.0) # rotação da nave
    glTranslatef(T, T2, 8.0)# posicao inicial da nave
    glPushMatrix()


    # Corpo da nave
    glTranslatef(0.0, 0.0, 0.0) 
    glColor3f(0.0, 1.0, 1.1) # cor da nave
    visualization.draw(nave) # desenha a nave
    glPopMatrix()

    glPushMatrix()
   # Desenha vários ovnis
    for pos in ovni_posicoes:
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glColor3f(1.0, 0.0, 0.0)
        visualization.draw(ovni)
        glPopMatrix()
    
    glPopMatrix()

    glPopMatrix()
    
    # -------------- eixo X --------------
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(-10.0, 0.0, 0.0)
    glEnd()
    
    # -------------- eixo Y --------------
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, -10.0, 0.0)
    glEnd()
    
    # -------------- eixo Z --------------
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 10.0)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, -10.0)
    glEnd()

    # -------------- CHÃO --------------
    glBegin(GL_POLYGON)
    glColor3f(1,0.5,1)
    glVertex3f(5,-1,9) # ponto do 1º quadrante (x,z)
    glVertex3f(5,-1,-50) # ponto do 2º quadrante (x,z)
    glVertex3f(-5,-1,-50) # ponto do 3º quadrandte (x,z)
    glVertex3f(-5,-1,9) # ponto do 4º quadrandte (x,z)
    glEnd()

    glutSwapBuffers()
    
def Keys(key, x, y):
    global T
    global T2
    global T3
    
    if(key == GLUT_KEY_LEFT ): 
        if (T > -0.8):
            T -= 0.03
    elif(key == GLUT_KEY_RIGHT ): 
        if (T < 0.8):
            T += 0.03
    elif(key == GLUT_KEY_UP ): 
        if(T2 < 0.3):
            T2 += 0.03
    elif(key == GLUT_KEY_DOWN ):
        if(T2 > 0):
            T2 -= 0.03
    elif(key == GLUT_KEY_PAGE_UP ): 
        T3 -= 1 
    elif(key == GLUT_KEY_PAGE_DOWN ): 
        T3 += 1         

# -------------- animacao do jogo --------------        
def animacao():
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)



def idle():
    global T
    T -= 1
    
# -------------- Câmera do Jogo --------------
def resize(w, h): # função para a câmera acompanhar o movimento da nave
    glViewport(0, 0, w, h) # define a área de visualização
    glMatrixMode(GL_PROJECTION) # define o tipo de matriz
    glLoadIdentity()
    gluPerspective(25.0, w/h, 1.0, 100.0) # define o angulo de visão
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.50, 10.0, # posição da câmera 
                0.0, 0.0, 0.0, # onde a câmera vai apontar
                0.0, 1.0, 0.0) # parte pra cima

# Lista das Posições dos Ovnis 
ovni_posicoes = [
    (-1.0, 0.50, -4.0),
    (0.8, 0.60, -4.5),
    (-0.5, 0.45, -4.2),
    (1.0, 0.30, -4.6),
]


def init():
    glClearColor (0.3, 0.3, 0.3, 0.0)
    glShadeModel( GL_SMOOTH )
    glClearColor( 0.0, 0.1, 0.0, 0.5 )
    glClearDepth( 1.0 )
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LEQUAL )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    glLightModelfv( GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0] )
    glLightfv( GL_LIGHT0, GL_AMBIENT, [ 0.2, 0.2, 0.2, 1.0] )
    glLightfv( GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0] )
    glLightfv( GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1] );
    glLightfv( GL_LIGHT0, GL_POSITION, [10.0, 10.0, 10.0, 0.0])
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.01)
    glEnable( GL_LIGHT0 )
    glEnable( GL_COLOR_MATERIAL )
    glShadeModel( GL_SMOOTH )
    glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE )
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("JOGO DE ASTEROIDES")
init()
ovni = pywavefront.Wavefront("Inimigo.obj")
nave = pywavefront.Wavefront("Nave.obj")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(Keys)
glutMainLoop()
