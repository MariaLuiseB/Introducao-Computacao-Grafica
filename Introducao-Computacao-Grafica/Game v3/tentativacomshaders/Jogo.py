from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np
from OpenGL.arrays import vbo
from OpenGL.GL import shaders

T = 0
T2 = 0
T3 = 0
rotacao_nave = -90  # Ângulo de rotação inicial da nave

# ovni_cores = [
#     (1.0, 0.0, 0.0),  # Cor do primeiro ovni (vermelho)
#     (0.0, 1.0, 0.0),  # Cor do segundo ovni (verde)
#     (0.0, 0.0, 1.0),  # Cor do terceiro ovni (azul)
#     (1.0, 1.0, 0.0),  # Cor do quarto ovni (amarelo)
#     ]

# Lista das Posições dos Ovnis 
ovni_posicoes = [
    (-1.0, 0.55, 1.7),
    (0.8, 0.60, 2.5),
    (-0.5, 0.45, 2.2),
    (1.0, 0.30, 1.0),
]

# -------------- Desenha o Jogo --------------
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    
    glPushMatrix()
    
    vertices = nave.materials['sh3'].vertices
    vertices = np.array(vertices, dtype=np.float32).reshape(-1,6)
    vbo_nave = vbo.VBO(vertices)

    # Aplicar shader a nave 
    glUseProgram(nave_shader)

    # Ações em toda a nave
    glTranslatef(T, T2, T3)# posicao inicial da nave
    glRotatef(rotacao_nave, 0.0, 1.0, 0.0) # rotacao da nave
    # Corpo da nave
    # glColor3f(0.0, 1.0, 1.1) # cor da nave
    visualization.draw(nave) # desenha a nave
    
    glPopMatrix()

    glPushMatrix()

    glUseProgram(nave_shader)
    glUniform4f( LIGHT_LOCATIONS['Global_ambient'], 0.1, 0.1, 0.1, 1.0 )
    glUniform3f( LIGHT_LOCATIONS['Light_location'], -5.0, 5.0, 0.0 )
    glUniform4f( LIGHT_LOCATIONS['Light_ambient'], 0.2, 0.2, 0.2, 1.0 )
    glUniform4f( LIGHT_LOCATIONS['Light_diffuse'], 0.9, 0.9, 0.9, 1.0 )
    glUniform4f( LIGHT_LOCATIONS['Light_specular'], 0.9,0.9,0.9, 1.0 )
    
    glUniform4f( LIGHT_LOCATIONS['Material_ambient'], .1,.1,.1, 1.0 )
    glUniform4f( LIGHT_LOCATIONS['Material_diffuse'], 0.1,0.1,0.9, 1 )
    glUniform4f( LIGHT_LOCATIONS['Material_specular'], 0.9,0.9,0.9, 1 )
    glUniform1f( LIGHT_LOCATIONS['Material_shininess'], 0.6*128.0 )

    vbo_nave.bind()

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    glVertexPointer(3, GL_FLOAT, 24, vbo_nave+12)
    glNormalPointer(GL_FLOAT, 24, vbo_nave)
    glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0])
    vbo_nave.unbind()

    glUseProgram(0)

    glPopMatrix()

    glPushMatrix()

    # Criar VBO para os ovnis
    vertices_ovni = ovni.materials['Brown'].vertices  # Substitua 'material_name' pelo nome correto do material dos ovnis
    vertices_ovni = np.array(vertices_ovni, dtype=np.float32).reshape(-1, 6)
    global vbo_ovni
    vbo_ovni = vbo.VBO(vertices_ovni)

    # -------------- OVNIS --------------
    # Aplicar shader aos ovnis
    glUseProgram(ovni_shader)

    vbo_ovni.bind()

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    glVertexPointer(3, GL_FLOAT, 24, vbo_ovni + 12)
    glNormalPointer(GL_FLOAT, 24, vbo_ovni)
    glDrawArrays(GL_TRIANGLES, 0, vertices_ovni.shape[0])
    vbo_ovni.unbind()

    glUseProgram(0)  # Desativar o shader dos ovnis

    glPopMatrix()

   # Desenha vários ovnis
    for i, pos in enumerate(ovni_posicoes): 
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glDrawArrays(GL_TRIANGLES, 0, vertices_ovni.shape[0])
        # glColor3f(*ovni_cores[i])
        visualization.draw(ovni) # desenha o ovni
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
    glColor3f(10,0.5,1)
    glVertex3f(10,-1,9) # ponto do 1º quadrante (x,z)
    glVertex3f(10,-1,-50) # ponto do 2º quadrante (x,z)
    glVertex3f(-10,-1,-50) # ponto do 3º quadrante (x,z)
    glVertex3f(-10,-1,9) # ponto do 4º quadrandte (x,z)
    glEnd()

    glutSwapBuffers()
    
def Keys(key, x, y):
    global T
    global T2
    global T3
    global rotacao_nave
    
    if(key == GLUT_KEY_LEFT ): 
        if (T > -8):
            T -= 0.05
            rotacao_nave += 10.0
    elif(key == GLUT_KEY_RIGHT ): 
        if (T < 8):
            T += 0.05
            rotacao_nave -= 10.0
    elif(key == GLUT_KEY_UP ): 
        if (T3 < 4):
            T3 -= 0.05
    elif(key == GLUT_KEY_DOWN ):
        if (T3 > -4):
            T3 += 0.05         

# -------------- animacao do jogo --------------        
def animacao(value):
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
    gluLookAt(0.0, 20.0, 5.0, # posição da câmera 
                0.0, 0.0, 0.0, # onde a câmera vai apontar
                0.0, 1.0, 0.0) # parte pra cima


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

    # Carregue o código do shader de vértice de 'Nave.vert'
    with open('SpaceShip.vert', 'r') as vertex_shader_file:
        vertex_shader_arquivo = vertex_shader_file.read()

    # Carregue o código do shader de fragmento de 'Nave.frag'
    with open('SpaceShip.frag', 'r') as fragment_shader_file:
        fragment_shader_arquivo = fragment_shader_file.read()

    # Crie e compile o shader de vértice
    vertexShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertexShader, vertex_shader_arquivo)
    glCompileShader(vertexShader)

    # Crie e compile o shader de fragmento
    fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragmentShader, fragment_shader_arquivo)
    glCompileShader(fragmentShader)

    
    global nave_shader
    nave_shader = glCreateProgram()
    glAttachShader(nave_shader, vertexShader)
    glAttachShader(nave_shader, fragmentShader)
    glLinkProgram(nave_shader)

    
    global LIGHT_LOCATIONS
    LIGHT_LOCATIONS = {
        'Global_ambient': glGetUniformLocation( nave_shader, 'Global_ambient' ),
        'Light_ambient': glGetUniformLocation( nave_shader, 'Light_ambient' ),
        'Light_diffuse': glGetUniformLocation( nave_shader, 'Light_diffuse' ),
        'Light_location': glGetUniformLocation( nave_shader, 'Light_location' ),
        'Light_specular': glGetUniformLocation( nave_shader, 'Light_specular' ),
        'Material_ambient': glGetUniformLocation( nave_shader, 'Material_ambient' ),
        'Material_diffuse': glGetUniformLocation( nave_shader, 'Material_diffuse' ),
        'Material_shininess': glGetUniformLocation( nave_shader, 'Material_shininess' ),
        'Material_specular': glGetUniformLocation( nave_shader, 'Material_specular' ),
    }

    global ATTR_LOCATIONS
    ATTR_LOCATIONS = {
        'Vertex_position': glGetAttribLocation( nave_shader, 'Vertex_position' ),
        'Vertex_normal': glGetAttribLocation( nave_shader, 'Vertex_normal' )
    }

     # Carregar shader dos ovnis
    with open('Ovni.vert', 'r') as vertex_shader_file:
        vertex_shader_code_ovni = vertex_shader_file.read()
    
    with open('Ovni.frag', 'r') as fragment_shader_file:
        fragment_shader_code_ovni = fragment_shader_file.read()

    global ovni_shader
    ovni_shader = shaders.compileProgram(
        shaders.compileShader(vertex_shader_code_ovni, GL_VERTEX_SHADER),
        shaders.compileShader(fragment_shader_code_ovni, GL_FRAGMENT_SHADER)
    )

    global OVNI_LIGHT_LOCATIONS
    OVNI_LIGHT_LOCATIONS = {
        'Light_ambient': glGetUniformLocation(ovni_shader, 'Light_ambient'),
        'Light_diffuse': glGetUniformLocation(ovni_shader, 'Light_diffuse'),
        'Light_specular': glGetUniformLocation(ovni_shader, 'Light_specular'),
        'Material_ambient': glGetUniformLocation(ovni_shader, 'Material_ambient'),
        'Material_diffuse': glGetUniformLocation(ovni_shader, 'Material_diffuse'),
        'Material_shininess': glGetUniformLocation(ovni_shader, 'Material_shininess'),
        'Material_specular': glGetUniformLocation(ovni_shader, 'Material_specular'),
    }

    global OVNI_ATTR_LOCATIONS
    OVNI_ATTR_LOCATIONS = {
        'Vertex_position': glGetAttribLocation(ovni_shader, 'Vertex_position'),
        'Vertex_normal': glGetAttribLocation(ovni_shader, 'Vertex_normal')
    }


glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("JOGO DE ASTEROIDES")
init()
ovni = pywavefront.Wavefront("Ovni.obj")
nave = pywavefront.Wavefront("SpaceShip.obj")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(Keys)
glutMainLoop()
