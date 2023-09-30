from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
import numpy as np

T = 0
T2 = 0.09
T3 = 0

# Lista das Posições dos Ovnis 
ovni_posicoes = [
    (-1.0, 0.55, -4.7),
    (0.8, 0.60, -4.5),
    (-0.5, 0.45, -4.2),
    (1.0, 0.30, -4.0),
]

posicao_luz_ovnis = (0.0, 1.0, -5.0, 1.0)

# -------------- Desenha o Jogo --------------
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    # Ativar iluminação para a nave 
    glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # Configurar propriedades da iluminação para os ovnis
    ovni_amb = [0.1, 0.1, 0.1, 1.0]
    ovni_dif = [1., 0.0, 0.0, 1.0]  # Cor da luz difusa dos ovnis (vermelha, por exemplo)
    ovni_spe = [1.0, 1.0, 1.0, 1.0]  # Cor da luz especular dos ovnis (branca, por exemplo)

    # Aplicar propriedades da iluminação para os ovnis
    glMaterialfv(GL_FRONT, GL_AMBIENT, ovni_amb)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, ovni_dif)
    glMaterialfv(GL_FRONT, GL_SPECULAR, ovni_spe)
    glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

    #Configurar propriedades da iluminação para a nave
    nave_amb = [0.1, 0.1, 0.1, 1.0]
    nave_dif = [0.5, 0.5, 0.5, 1.0]
    nave_spe = [0.7, 1.0, 0.7, 1.0]

    # Aplicar propriedades da iluminação para a nave
    glMaterialfv(GL_FRONT, GL_AMBIENT, nave_amb)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, nave_dif)
    glMaterialfv(GL_FRONT, GL_SPECULAR, nave_spe)
    glMaterialf(GL_FRONT, GL_SHININESS, 100.0)


    # vertices_nave = nave.materials['Material'].vertices
    # vertices_nave = np.array(vertices_nave, dtype=np.float32)
    # vbo_nave = vbo.VBO(vertices_nave)
    
    glPushMatrix()
    # Ações em toda a nave
    glRotatef(0.0, 0.0, 0.0, 0.0) # rotação da nave
    glTranslatef(T, T2, 8.0)# posicao inicial da nave


    glPushMatrix()

    # # Colocar shader na nave 
    # glUseProgram(nave_shaders) # Usar o programa de shader

    # glUniform4f(LIGHT_LOCATIONS['global_ambient'], 0.1, 0.1, 0.1, 1.0)
    # glUniform4f(LIGHT_LOCATIONS['light_ambient'], 0.1, 0.1, 0.1, 1.0)
    # glUniform4f(LIGHT_LOCATIONS['light_diffuse'], 0.5, 0.5, 0.5, 1.0)
    # glUniform4f(LIGHT_LOCATIONS['light_specular'], 0.7, 0.7, 0.7, 1.0)
    # glUniform3f(LIGHT_LOCATIONS['light_position'], 10.0, 10.0, 1.0)
    # glUniform3f(LIGHT_LOCATIONS['light_direction'], 0.0, 0.0, 1.0)

    # glUniform4f(LIGHT_LOCATIONS['material_ambient'],chrome_ambient[0], chrome_ambient[1], chrome_ambient[2], chrome_ambient[3])
    # glUniform4f(LIGHT_LOCATIONS['material_diffuse'], chrome_diffuse[0], chrome_diffuse[1], chrome_diffuse[2], chrome_diffuse[3])
    # glUniform4f(LIGHT_LOCATIONS['material_specular'], chrome_specular[0], chrome_specular[1], chrome_specular[2], chrome_specular[3])
    # glUniform1f(LIGHT_LOCATIONS['material_shininess'], chrome_shininess)


    # vbo_nave.bind() # Vincular o VBO

    # glEnableClientState(GL_VERTEX_ARRAY) # Habilitar o uso de arrays de vértices no VBO
    # glEnableClientState(GL_NORMAL_ARRAY) # Habilitar o uso de arrays de normais no VBO
    # glVertexPointer(3, GL_FLOAT, 24, vbo_nave +12) # Especificar o array de vértices
    # glNormalPointer(GL_FLOAT, 24, vbo_nave) # Especificar o array de normais
    # glDrawArrays(GL_TRIANGLES, 0, vertices_nave.shape[0]) # Desenhar o objeto
    # vbo_nave.unbind() # Desvincular o VB

    glPushMatrix()
    # Corpo da nave
    glTranslatef(0.0, 0.0, 0.0) 
    glColor3f(0.0, 1.0, 1.1) # cor da nave
    visualization.draw(nave) # desenha a nave
    glPopMatrix()

    # glDisableClientState(GL_VERTEX_ARRAY) # Desabilitar o uso de arrays de vértices no VBO
    # glDisableClientState(GL_NORMAL_ARRAY) # Desabilitar o uso de arrays de normais no VBO
    # glUseProgram(0) # Desativar o programa de shader

    # Desativa iluminação para os ovnis
    glDisable(GL_LIGHTING)  
    # glDisable(GL_LIGHT0)
    
    # Ativar iluminação para os ovnis
    glEnable(GL_LIGHT1) 
    glPopMatrix()

    glEnable(GL_LIGHT1)
    # -------------- Desenha os Ovnis --------------
    for pos in ovni_posicoes:
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glColor3f(1.0, 0.0, 0.0)
        visualization.draw(ovni)
        glPopMatrix()

    glPopMatrix()

    
    glDisable(GL_LIGHT1)
    
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


def init():
    glClearColor (0.3, 0.3, 0.3, 0.0)
    glShadeModel( GL_SMOOTH )
    glClearColor( 0.0, 0.1, 0.0, 0.5 )
    glClearDepth( 1.0 )
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LEQUAL )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    #Configurar a primeira fonte de luz (luz ambiente)
    # glLightModelfv( GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0] )
    # glEnable( GL_LIGHT0 )
    # glLightfv( GL_LIGHT0, GL_AMBIENT, [ 1.0, 0.0, 0.0, 1.0] )
    # glLightfv( GL_LIGHT0, GL_DIFFUSE, [0.5, 0.3, 0.5, 1.0] )
    # glLightfv( GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1] );
    # glLightfv( GL_LIGHT0, GL_POSITION, [0.0, 0.0, 8.0, 0.0])
    # glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)
    # glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.01)

    # Configurar a segunda fonte de luz (luz sobre os ovnis)
    glEnable(GL_LIGHT1)  # Ativar a segunda fonte de luz
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    # Posicionar a segunda fonte de luz acima dos OVNIs
    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 1.0, -5.0, 1.0])  # Posição acima dos OVNIs
    # Configurar a direção do feixe de luz (spot direction) apontando para baixo (dependendo da orientação desejada)
    spotlight_direction = [0.0, -1.0, 0.0]  # Para iluminar para baixo
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, spotlight_direction)
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 30.0)  # Ângulo do feixe de luz (ajuste conforme necessário)

    # # Configurar o programa de shader
    # vertex_shader = shaders.compileShader(open("Nave.vert", 'r').read(), GL_VERTEX_SHADER)
    # fragment_shader = shaders.compileShader(open("Nave.frag", 'r').read(), GL_FRAGMENT_SHADER)
    
    # # Criação do programa de shader
    # global nave_shaders
    # nave_shaders = glCreateProgram()
    # glAttachShader(nave_shaders, vertex_shader)
    # glAttachShader(nave_shaders, fragment_shader)
    # glLinkProgram(nave_shaders)

    # global LIGHT_LOCATIONS
    # LIGHT_LOCATIONS = {
    #     'global_ambient': glGetUniformLocation(nave_shaders, 'global_ambient'),
    #     'light_ambient': glGetUniformLocation(nave_shaders, 'light_ambient'),
    #     'light_diffuse': glGetUniformLocation(nave_shaders, 'light_diffuse'),
    #     'light_specular': glGetUniformLocation(nave_shaders, 'light_specular'),
    #     'light_position': glGetUniformLocation(nave_shaders, 'light_position'),
    #     'light_direction': glGetUniformLocation(nave_shaders, 'light_direction'),
    #     'material_ambient': glGetUniformLocation(nave_shaders, 'material_ambient'),
    #     'material_diffuse': glGetUniformLocation(nave_shaders, 'material_diffuse'),
    #     'material_specular': glGetUniformLocation(nave_shaders, 'material_specular'),
    #     'material_shininess': glGetUniformLocation(nave_shaders, 'material_shininess'),
    # }

    # global ATTR_LOCATIONS 
    # ATTR_LOCATIONS = {
    #     'vertex': glGetAttribLocation(nave_shaders, 'vertex'),
    #     'normal': glGetAttribLocation(nave_shaders, 'normal'),
    # }

    # global chrome_ambient
    # global chrome_diffuse
    # global chrome_specular
    # global chrome_shininess

    # chrome_ambient = [0.1, 0.1, 0.1, 1.0]  # Substitua esses valores pelos desejados
    # chrome_diffuse = [0.1, 0.1, 0.8, 1.0]
    # chrome_specular = [0.9, 0.9, 0.9, 1.0]
    # chrome_shininess = 128.0

    
    glEnable( GL_COLOR_MATERIAL )
    glShadeModel( GL_SMOOTH )
    glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE )
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    # glEnable( GL_LIGHT0 )
    glEnable( GL_LIGHT1 )


glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("JOGO DE ASTEROIDES")
init()
ovni = pywavefront.Wavefront("Ovni.obj")
nave = pywavefront.Wavefront("Nave.obj")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(Keys)
glutMainLoop()
