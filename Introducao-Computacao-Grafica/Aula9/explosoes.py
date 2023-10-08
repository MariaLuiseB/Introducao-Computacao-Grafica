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

space = 0

PART_VELOCIDADE = 0.1
EXPLOSAO_TEMPO = 0.05

explosoes = []

class Particula:
    vx = vy = vz = 0.0 # velocidade da particula
    
    def __init__(self, vx, vy, vz):
        self.vx = vx
        self.vy = vy
        self.vz = vz
        
class Explosao:
    px = py = pz = 0.0 # posicao da explosao
    contador = 0
    tdv = 1 # tempo de vida da explosao
    particulas = []
        
    def __init__(self, px, py, pz, n_part):
        self.px = px
        self.py = py
        self.pz = pz
        for i in range(n_part): # cria as particulas da explosao com velocidades aleatorias
            vx = np.random.randn() * PART_VELOCIDADE 
            vy = np.random.randn() * PART_VELOCIDADE
            vz = np.random.randn() * PART_VELOCIDADE
            self.particulas.append(Particula(vx + 0.1, vy/2, vz/2)) # adiciona uma particula nova na lista de particulas da explosao
        
        
    def desenha(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        for particula in self.particulas:
            part_px = self.px + particula.vx * (self.contador / 2)
            part_py = self.py + particula.vy * (self.contador / 2)
            part_pz = self.pz + particula.vz * (self.contador / 2)
            glPushMatrix()
            glTranslatef(part_px, part_py, part_pz)
            glRotatef( self.contador*10, 0.0, 1.0, 0.0)
            glBegin(GL_TRIANGLES)
            glColor4f(0.9,  0.1, 0.1, self.tdv)
            glNormal3f(0.0, 0.0, 1.0)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(0.0, 0.6, 0.0)
            glVertex3f(0.6, 0.0, 0.0)
            glEnd()
            glPopMatrix()
            
        self.tdv -= EXPLOSAO_TEMPO
        self.contador += 1
            


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)  
    global explosoes, space
    
    
    if(space):
        px = np.random.uniform(-5.0, 5.0)
        py = np.random.uniform(-5.0, 5.0)
        pz = np.random.uniform(-5.0, 5.0)
        explosoes.append(Explosao(px, py, pz, 10))
        space=0

    glPushMatrix()
    #glRotatef(T, 0.0, 1.0, 0.0)
    glTranslatef(T, T2, T3)

    glEnable( GL_COLOR_MATERIAL )
       
    for i, expl in enumerate(explosoes):
        expl.desenha()
        if(expl.tdv < 0):
            del explosoes[i]
            
    
    
    glPopMatrix()
    
    
    glUseProgram(0)
    
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
    
    glPushMatrix()
    glTranslatef(-5.0, 5.0, 0.0)
    glutSolidSphere(0.8, 8, 8)
    glPopMatrix()
  


    glutSwapBuffers()
    
def Keys(key, x, y):
    global T
    global T2
    global T3
    
    if(key == GLUT_KEY_LEFT ): 
        T -= 1 
    elif(key == GLUT_KEY_RIGHT ): 
        T += 1 
    elif(key == GLUT_KEY_UP ): 
        T2 -= 1
    elif(key == GLUT_KEY_DOWN ): 
        T2 += 1 
    elif(key == GLUT_KEY_PAGE_UP ): 
        T3 -= 1 
    elif(key == GLUT_KEY_PAGE_DOWN ): 
        T3 += 1         
       
def Keys_letras(key, x ,y):
    global space
    if(key == b' ' ): #Espaço
        space = 1       

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
    gluLookAt(15.0, 12.0, 14.0,
                0.0, 3.0, 0.0,
                0.0, 1.0, 0.0)

  

def init():
    glClearColor (0.3, 0.3, 0.3, 0.0)
    glShadeModel( GL_SMOOTH )
    glClearColor( 0.0, 0.0, 0.0, 1.0 )
    glClearDepth( 1.0 )
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LEQUAL )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    glDepthFunc( GL_LEQUAL )
    glEnable( GL_DEPTH_TEST )
    
    vertexShader = shaders.compileShader(open('carro.vert', 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = shaders.compileShader(open('carro.frag', 'r').read(), GL_FRAGMENT_SHADER)

    global carro_shader
    carro_shader = glCreateProgram()
    glAttachShader(carro_shader, vertexShader)
    glAttachShader(carro_shader, fragmentShader)
    glLinkProgram(carro_shader)
    
    global LIGTH_LOCATIONS
    LIGTH_LOCATIONS = {
        'Global_ambient': glGetUniformLocation( carro_shader, 'Global_ambient' ),
        'Light_ambient': glGetUniformLocation( carro_shader, 'Light_ambient' ),
        'Light_diffuse': glGetUniformLocation( carro_shader, 'Light_diffuse' ),
        'Light_location': glGetUniformLocation( carro_shader, 'Light_location' ),
        'Light_specular': glGetUniformLocation( carro_shader, 'Light_specular' ),
        'Material_ambient': glGetUniformLocation( carro_shader, 'Material_ambient' ),
        'Material_diffuse': glGetUniformLocation( carro_shader, 'Material_diffuse' ),
        'Material_shininess': glGetUniformLocation( carro_shader, 'Material_shininess' ),
        'Material_specular': glGetUniformLocation( carro_shader, 'Material_specular' ),
    }
    
    global ATTR_LOCATIONS
    ATTR_LOCATIONS = {
        'Vertex_position': glGetAttribLocation( carro_shader, 'Vertex_position' ),
        'Vertex_normal': glGetAttribLocation( carro_shader, 'Vertex_normal' )
    }

    

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Cubo")
init()
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(Keys)
glutKeyboardFunc(Keys_letras)
glutMainLoop()
