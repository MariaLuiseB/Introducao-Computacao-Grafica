from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np


T1 = 0
T2 = 0
T3 = 0
angulo = 0
cima = 0
baixo = 0
esquerda = 0
direita = 0
velocidade = 0.8

# Lista das Posições dos Ovnis 
ovni_posicoes = [
    (-5.0, 0.0, -1.7),
    (3.0, 0.0, -2.5),
    (-1.0, 0.0, 3.2),
    (1.0, 0.0, 1.0),
]
# -------------- Desenha o Jogo --------------
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    movimentos()

    # Configurar material roxo
    glColor3f(1.0, 1.0, 1.0)  # Cor branca
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [5.0])  # Brilho

    glPushMatrix()
    # Ações em toda a nave
    glTranslatef(T1, 0.0, T3)# posicao inicial da nave
    # Corpo da nave
    # glColor3f(0.0, 1.0, 1.1) # cor da nave
    glRotatef(-90, 0.0, 1.0, 0.0) # rotacao da nave
    glRotatef(angulo, 0.0, 1.0, 0.0) # rotacao da nave
    visualization.draw(nave) # desenha a nave
    glPopMatrix()

   # Desenha vários ovnis
    for _, pos in enumerate(ovni_posicoes): 
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        # glColor3f(*ovni_cores[i])
        glScalef(0.2, 0.2, 0.2)  # Reduz o tamanho do ovni para 20%
        visualization.draw(ovni) # desenha o ovni
        glPopMatrix()
    
    # Desenha o planeta 
    glPushMatrix()
    glTranslatef(8.0, 0.0, -2.0) # posicao inicial do planeta
    glRotatef(180, 0.0, 0.5, 1.0) # rotacao do planeta
    glScalef(2.0, 2.0, 2.0) # tamanho do planeta 
    visualization.draw(planeta) # desenha o planeta
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
    # glBegin(GL_POLYGON)
    # glColor3f(0.0,0.0,0.2) # cor do chão
    # glVertex3f(10,-1,9) # ponto do 1º quadrante (x,z)
    # glVertex3f(10,-1,-50) # ponto do 2º quadrante (x,z)
    # glVertex3f(-10,-1,-50) # ponto do 3º quadrandte (x,z)
    # glVertex3f(-10,-1,9) # ponto do 4º quadrandte (x,z)
    # glEnd()

    glutSwapBuffers()

def KeysUp(key, x, y):
    global cima, baixo, esquerda, direita, velocidade
    if(key == GLUT_KEY_LEFT ): 
        esquerda = 0
    elif(key == GLUT_KEY_RIGHT ):
        direita = 0
    elif(key == GLUT_KEY_UP ):
        cima = 0
    elif(key == GLUT_KEY_DOWN ):
        baixo = 0
        velocidade = 0.8

def Keys(key, x, y):
    global T1
    global T3
    global angulo, cima, baixo, esquerda, direita, velocidade
    
    if(key == GLUT_KEY_LEFT ): 
            esquerda = 1
    elif(key == GLUT_KEY_RIGHT ): 
            direita = 1
    elif(key == GLUT_KEY_UP ): 
           cima = 1
    elif(key == GLUT_KEY_DOWN ):
            baixo = 1

def movimentos():
    global T1
    global T3
    global angulo
    global cima, baixo, esquerda, direita, velocidade

    if esquerda == 1:
        angulo += 5.0
    if direita == 1:
        angulo -= 5.0
    if cima == 1:
        if (velocidade < 4.0):
            velocidade += 0.03
        T1 -= (0.15 * np.cos(np.radians(angulo))) * velocidade
        T3 -= (0.15 * np.sin(np.radians(angulo))) * velocidade
    
    if baixo == 1:
        if (velocidade > 4.0):
            velocidade -= 0.03
        T1 += (0.15 * np.cos(np.radians(angulo))) * velocidade
        T3 += (0.15 * np.sin(np.radians(angulo))) * velocidade
    
    if cima == 0 and baixo == 0:
        if (velocidade > 0.8):
            velocidade -= 0.2
            T1 += (0.15 * np.cos(np.radians(angulo))) * velocidade
            T3 += (0.15 * np.sin(np.radians(angulo))) * velocidade

# -------------- animacao do jogo --------------        
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)

# def idle():
#     global T1
#     T1 -= 1
    
# -------------- Câmera do Jogo --------------
def resize(w, h): # função para a câmera acompanhar o movimento da nave
    glViewport(0, 0, w, h) # define a área de visualização
    glMatrixMode(GL_PROJECTION) # define o tipo de matriz
    glLoadIdentity()
    gluPerspective(25.0, w/h, 1.0, 100.0) # define o angulo de visão
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 20.0, 5.0, # posição da câmera 
                0.0, 0.0, 0.0, # onde a câmera vai apontar
                0.0, 1.0, 0.0) # parte pra cima


def init():
    glClearColor (0.3, 0.3, 0.3, 0.0)
    glClearColor( 0.0, 0.0, 0.0, 1.0 )
    glClearDepth( 1.0 )
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LEQUAL )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    glDepthFunc( GL_LEQUAL )
    glEnable( GL_DEPTH_TEST )

    # Defina a posição da fonte de luz roxa
    posicao_da_fonte_de_luz_branca = [1.0, 1.0, 1.0, 0.0]  # (x, y, z, w)
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_da_fonte_de_luz_branca)

    # Ativar iluminação
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)  # Você pode ter até 8 fontes de luz (GL_LIGHT0 a GL_LIGHT7)

    # Configurar a cor da luz
    luz_roxa = [1.0, 1.0, 1.0, 1.0]  # Cor da luz roxa (RGB + Alpha)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_roxa)

    # Configurar a posição da fonte de luz
    luz_posicao = [5.0, 5.0, 5.0, 1.0]  # Posição da fonte de luz (x, y, z, w)
    glLightfv(GL_LIGHT0, GL_POSITION, luz_posicao)

    # Configurar o modelo de iluminação
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)


glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("JOGO DE ASTEROIDES")
init()
ovni = pywavefront.Wavefront("Ovni.obj")
nave = pywavefront.Wavefront("SpaceShip.obj")
planeta = pywavefront.Wavefront("planeta.obj")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(Keys)
glutSpecialUpFunc(KeysUp)
glutMainLoop()
