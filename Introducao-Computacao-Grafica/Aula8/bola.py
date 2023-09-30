from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
#from pywavefront import visualization
from PIL import Image
import numpy as np


GRAVIDADE = 0.1
VOLANTE = 20.0
VELOCIDADE = 0.1
PULO = 1.5
RESISTENCIA = 1.4
F_RESISTENCIA = 0.2
F_RESISTENCIA_AR = 0.05

light_position = [5.0, 10.0, -5.0, 1.0]
light_position2 = [-15.0, 10.0, 20.0, 1.0]

amb_light = [ 0.3, 0.3, 0.3, 1.0]
diffuse = [ 0.9, 0.9, 0.9, 1.0]
specular = [ 1.0, 1.0, 1.0, 1.0]
attenuation_quad = 0.01
attenuation_linear = 0.01

up = down = frente = space = pulo = 0

class Bola:

    vx = vy = vz = 0.0
    px = py = pz = 0.0
    yaw = pitch = roll = 0.0
    dir_y = rx = rz = 0.0
    
    
    def atualiza_bola(self):
        self.px += self.vx
        self.py += self.vy
        self.pz += self.vz

        if(not (abs(self.px)<=25.0)):
            self.px -= self.vx

        if(not (abs(self.pz)<=25.0)):
            self.pz -= self.vz

        if(self.py>15.0):
            self.py = 15.0
        elif(self.py<0.0):
            self.py = 0.0
            self.vy = 0.0

        print("Px: {} // Pz: {} // Py: {}\n".format(self.px, self.pz, self.py))
        
        
    def calcula_velocidade(self):
        global up, down, frente, space, pulo
        if(self.py==0.0):
            if(up):
              self.vx += np.sin(self.yaw * 3.14159/180.0)*VELOCIDADE
              self.vz += np.cos(self.yaw * 3.14159/180.0)*VELOCIDADE
              frente = 1
            elif(down):
              self.vx += - np.sin(self.yaw * 3.14159/180.0)*VELOCIDADE
              self.vz += - np.cos(self.yaw * 3.14159/180.0)*VELOCIDADE   
              frente = 0
          
        
            self.rx = (pow(RESISTENCIA,abs(self.vx))-1.0)*F_RESISTENCIA
            self.rz = (pow(RESISTENCIA,abs(self.vz))-1.0)*F_RESISTENCIA
        else:
            self.rx = (pow(RESISTENCIA,abs(self.vx))-1.0)*F_RESISTENCIA_AR
            self.rz = (pow(RESISTENCIA,abs(self.vz))-1.0)*F_RESISTENCIA_AR
        

        if(self.vx>self.rx):
            self.vx -= self.rx
        elif(self.vx<-self.rx):
            self.vx += self.rx
        elif(abs(self.vz)<self.rx):
            if(abs(self.vx)>0):
                printf("Parou\n")
                self.vx = 0.0
                self.vz = 0.0


        if(self.vz>self.rz):
            self.vz -= self.rz
        elif(self.vz<-self.rz):
            self.vz += self.rz
        elif(abs(self.vx)<self.rz):
            if(abs(self.vz)>0):
                printf("Parou\n")
                self.vz = 0.0
                self.vx = 0.0
        

        if(frente):
            self.pitch += 10*np.sqrt(pow(self.vx,2)+pow(self.vz,2))
        else:
            self.pitch -= 10*np.sqrt(pow(self.vx,2)+pow(self.vz,2))


        if((space) and not (pulo)):
            self.vy = PULO
            pulo = 1
        elif((not space) and (pulo)):
            if(self.vy>PULO/2):
              self.vy = PULO/2
              pulo = 0
            else:
              pulo = 0
            
        

        self.vy -= GRAVIDADE

        print("Vx: {} // Vz: {} // Vy: {}\n".format(self.vx, self.vz, self.vy))





bola = Bola()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    
    luz()
    

    bola.calcula_velocidade()
    bola.atualiza_bola()
    
    glEnable(GL_COLOR_MATERIAL)
    glCullFace(GL_FRONT_AND_BACK)
    

    glPushMatrix()
    glTranslatef(bola.px, bola.py, bola.pz)
    
    glBegin(GL_LINES)
    glColor3f(1.0, 0.1, 0.1)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(bola.vx*3, 0.0, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.1, 1.0, 0.1)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, bola.vy*3, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.3, 0.3, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, bola.vz*3)
    glEnd()
    
    glColor3f(0.4, 0.4, 0.6)
    glRotatef(bola.yaw, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 0.8, 0.0)
    glRotatef(bola.pitch, 1.0, 0.0, 0.0)
    glutSolidSphere(0.8, 8, 8)
    glPopMatrix()
    
    
    glColor3f(0.6, 0.6, 0.6)
    glBegin(GL_POLYGON)
    glNormal3f(0.0,1.0,0.0)
   
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-25.0, 0.0, -25.0)
    
    glTexCoord2f(4.0, 0.0)
    glVertex3f( 25.0, 0.0, -25.0)
    
    glTexCoord2f(4.0, 4.0)
    glVertex3f( 25.0, 0.0,  25.0)
    
    glTexCoord2f(0.0, 4.0)
    glVertex3f(-25.0, 0.0,  25.0)
    glEnd()

    glDisable(GL_COLOR_MATERIAL)
    

    glutSwapBuffers()
    
def Keys(key, x, y):
    global up, down
    
    if(key == GLUT_KEY_LEFT ): 
        bola.yaw -= VOLANTE
    elif(key == GLUT_KEY_RIGHT ): 
        bola.yaw += VOLANTE
    elif(key == GLUT_KEY_UP ): 
        up = 1 
    elif(key == GLUT_KEY_DOWN ): 
        down = 1
    
        
        
def KeysUp(key, x, y):
    global up, down
    
    if(key == GLUT_KEY_UP ): 
        up = 0
    elif(key == GLUT_KEY_DOWN ): 
        down = 0
        
def Keys_letras(key, x ,y):
    global space
    
    if(key == b' ' ): #Espaço
        space = 1
        
        
        
def Keys_letras_Up(key, x ,y):
    global space

    if(key == b' ' ): #Espaço
        space = 0

       
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(33, animacao,1)
    
    
def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 25.0, 35.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)

  

def init():
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LESS )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
    glEnable(GL_LIGHTING)
    glEnable( GL_LIGHT0 )
    glEnable( GL_LIGHT1 )
    #glEnable( GL_COLOR_MATERIAL ) # Transforma cores em materiais
    glShadeModel( GL_SMOOTH )  #Suaviza normais
    glEnable(GL_NORMALIZE)
    glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE )
    


    
    
    
def luz():
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, amb_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, attenuation_quad)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, attenuation_linear)
    
    glLightfv(GL_LIGHT1, GL_POSITION, light_position2)
    glLightfv(GL_LIGHT1, GL_AMBIENT, amb_light)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, attenuation_quad)
    glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION, attenuation_linear)

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Cubo")
init()
luz()
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(33,animacao,1)
glutSpecialFunc(Keys)
glutSpecialUpFunc(KeysUp)
glutKeyboardFunc(Keys_letras)
glutKeyboardUpFunc(Keys_letras_Up)
glutMainLoop()
