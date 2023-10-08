from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np
import random

T1 = 0
T2 = 0
T3 = 0

angulo_ovni = 0
cima = 0
baixo = 0
esquerda = 0
direita = 0
velocidade = 0.8

ovnis = []
tiros = []
space = 0
part_velocidade = 0.1
explosao_tempo = 0.05
explosoes = []

class Particula:
    vx = vy = vz = 0.0

    def __init__(self, vx, vy, vz):
        self.vx = vx
        self.vy = vy
        self.vz = vz

class Explosao:
    px = py = pz = 0.0
    contador = 0
    tdv = 1
    particulas = []

    def __init__(self, px, py, pz, n_part):
        self.px = px
        self.py = py
        self.pz = pz
        for i in range(n_part):
            vx = np.random.randn() * part_velocidade
            vy = np.random.randn() * part_velocidade
            vz = np.random.randn() * part_velocidade
            self.particulas.append(Particula(vx, vy, vz))
    
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
            glVertex3f(0.0, 0.2, 0.0) 
            glVertex3f(0.2, 0.0, 0.0) 
            glEnd()
            glPopMatrix()
            
        self.tdv -= explosao_tempo	
        self.contador += 1


class Tiro:
    def __init__(self, x, y,angulo_tiro):
        self.x = x
        self.y = y
        self.size = 0.35
        self.velocidade_tiro = 5.0
        self.angulo_tiro = angulo_tiro

def adicionar_tiro():
    global angulo_tiro, tiros
    angulo_tiro = np.copy(angulo_ovni)
    x = T1
    y = T2
    tiro = Tiro(x, y, angulo_tiro)
    tiros.append(tiro)

def movimentos_tiro(): 
    global tiros, ovnis, T1, T2
    for tiro in tiros:
        tiro.x += (0.15 * np.cos(np.radians(tiro.angulo_tiro))) * tiro.velocidade_tiro
        tiro.y += (0.15 * np.sin(np.radians(tiro.angulo_tiro))) * tiro.velocidade_tiro

        # detectar colisão entre o tiro e o ovni
        for ovni in ovnis:
            if np.sqrt((tiro.x - ovni.x)**2 + (tiro.y - ovni.y)**2) < (ovni.size-(ovni.size*0.1)):
                tiros.remove(tiro)
                ovnis.remove(ovni)
                explosoes.append(Explosao(ovni.x, ovni.y, 0.0, 10))

            # detectar colisão entre nave e ovni
            if np.sqrt((T1 - ovni.x)**2 + (T2 - ovni.y)**2) < (ovni.size-(ovni.size*0.1)):
                ovnis.remove(ovni)
                explosoes.append(Explosao(ovni.x, ovni.y, 0.0, 10))
                break

        # detectar se o tiro saiu da tela
        if tiro.x < -20.0 or tiro.x > 20.0 or tiro.y < -20.0 or tiro.y > 20.0:
            tiros.remove(tiro)

# classe para representar um ovni
class Ovni:
    def __init__(self, x, y, velocidade_ovni, aparece_ovni, angulo_ovni):
        self.x = x
        self.y = y
        self.velocidade_ovni = velocidade_ovni
        self.size = 0.5
        self.aparece_ovni = aparece_ovni
        self.angulo_ovni = angulo_ovni

def adicionar_ovni():
    # Escolha aleatoriamente uma das quatro bordas (cima, baixo, esquerda, direita)
    borda = random.choice(["cima", "direita", "esquerda", "baixo"])
    
    if borda == "cima":
        angulo_ovni = random.uniform(225, 315)
        aparece_ovni = "cima"
        x = random.uniform(-10.0, 10.0)  # Posição x aleatória
        y = 10.0  # Na parte superior da tela
    elif borda == "baixo":
        angulo_ovni = random.uniform(45, 135)
        aparece_ovni = "baixo"
        x = random.uniform(-10.0, 10.0)  # Posição x aleatória
        y = -10.0  # Na parte inferior da tela
    elif borda == "esquerda":
        # Escolher aleatoriamente entre os dois intervalos: (270, 360) ou (0, 90)
        intervalo = random.choice([(315, 360), (0, 45)])
        # Gerar um ângulo aleatório dentro do intervalo selecionado
        angulo_ovni = random.uniform(intervalo[0], intervalo[1])
        aparece_ovni = "esquerda"
        x = -10.0  # Na parte esquerda da tela
        y = random.uniform(-10.0, 10.0)  # Posição y aleatória
    else:
        angulo_ovni = random.uniform(135, 225)
        aparece_ovni = "direita"
        x = 10.0  # Na parte direita da tela
        y = random.uniform(-10.0, 10.0)  # Posição y aleatória
    

    velocidade_ovni = random.uniform(0.1, 0.2)  # Velocidade aleatória
    
    # Crie um novo asteroide e adicione-o à lista
    ovni = Ovni(x, y, velocidade_ovni, aparece_ovni, angulo_ovni)
    ovnis.append(ovni)

# Atualiza a posição de cada asteroide
def movimentos_ovni():
    global ovnis
    for ovni in ovnis:
        # Se o asteroide estiver na parte superior da tela, mova-o para baixo
        if ovni.aparece_ovni == "cima":
            ovni.x -= ovni.velocidade_ovni * np.cos(np.radians(ovni.angulo_ovni))
            ovni.y -= ovni.velocidade_ovni * np.sin(np.radians(ovni.angulo_ovni))
        # Se o asteroide estiver na parte inferior da tela, mova-o para cima
        elif ovni.aparece_ovni == "baixo":
            ovni.x += ovni.velocidade_ovni * np.cos(np.radians(ovni.angulo_ovni))
            ovni.y += ovni.velocidade_ovni * np.sin(np.radians(ovni.angulo_ovni))
        # Se o asteroide estiver na parte esquerda da tela, mova-o para a direita
        elif ovni.aparece_ovni == "esquerda":
            ovni.x += ovni.velocidade_ovni * np.cos(np.radians(ovni.angulo_ovni))
            ovni.y += ovni.velocidade_ovni * np.sin(np.radians(ovni.angulo_ovni))
        # Se o asteroide estiver na parte direita da tela, mova-o para a esquerda
        if ovni.aparece_ovni == "direita":
            ovni.x += ovni.velocidade_ovni * np.cos(np.radians(ovni.angulo_ovni))
            ovni.y += ovni.velocidade_ovni * np.sin(np.radians(ovni.angulo_ovni))

        # Se o asteroide sair da tela, remova-o da lista
        if ovni.x < -30.0 or ovni.x > 30.0 or ovni.y < -30.0 or ovni.y > 30.0:
            ovnis.remove(ovni)

# -------------- Desenha o Jogo --------------
def display():
    global ovnis, explosoes, space
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    movimentos_nave()
    movimentos_ovni()
    movimentos_tiro()

    # Configurar material roxo
    glColor3f(1.0, 1.0, 1.0)  # Cor branca
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [5.0])  # Brilho

    glPushMatrix()
    # Ações em toda a nave
    glTranslatef(T1, T2, T3)# posicao inicial da nave
    # Corpo da nave
    # glColor3f(0.0, 1.0, 1.1) # cor da nave
    glRotatef(angulo_ovni, 0.0, 0.0, 1.0) # rotacao da nave
    glScalef(1.5, 1.5, 1.5)
    visualization.draw(nave) # desenha a nave
    glPopMatrix()

    # -------------- TIRO --------------
    for tiro in tiros:
        glPushMatrix()
        glTranslatef(tiro.x, tiro.y, 0.0)
        glScalef(tiro.size, tiro.size, tiro.size)
        # glutSolidSphere(0.1, 20, 20)
        visualization.draw(tiro_obj)
        glPopMatrix()
    # -------------- OVNI --------------
    for ovni in ovnis:
        glPushMatrix()
        glTranslatef(ovni.x, ovni.y, 0.0)
        glScalef(0.5, 0.5, 0.5)
        visualization.draw(ovni_obj)
        glPopMatrix()

    if(space):
        px = np.random.uniform(-5.0, 5.0)
        py = np.random.uniform(-5.0, 5.0)
        pz = np.random.uniform(-5.0, 5.0)
        explosoes.append(Explosao(px, py, pz, 10))
        space = 0

    glPushMatrix()
    glTranslatef(T1, T2, T3)

    glEnable(GL_COLOR_MATERIAL)

    for i, expl in enumerate(explosoes):
        expl.desenha()
        if expl.tdv < 0.0:
            del explosoes[i]

    glPopMatrix()    
    # # -------------- eixo X --------------
    # glBegin(GL_LINES)
    # glColor3f(1.0, 0.0, 0.0) # cor do eixo X é vermelho
    # glVertex3f(0.0, 0.0, 0.0)
    # glVertex3f(10.0, 0.0, 0.0)
    # glEnd()

    # glBegin(GL_LINES)
    # glColor3f(1.0, 0.0, 0.0) # cor do eixo X é vermelho
    # glVertex3f(0.0, 0.0, 0.0)
    # glVertex3f(-10.0, 0.0, 0.0)
    # glEnd()
    
    # # -------------- eixo Y --------------
    # glBegin(GL_LINES)
    # glColor3f(0.0, 1.0, 0.0) # cor do eixo Y é verde
    # glVertex3f(0.0, 0.0, 0.0)
    # glVertex3f(0.0, 10.0, 0.0)
    # glEnd()

    # glBegin(GL_LINES)
    # glColor3f(0.0, 1.0, 0.0) # cor do eixo Y é verde
    # glVertex3f(0.0, 0.0, 0.0)
    # glVertex3f(0.0, -10.0, 0.0)
    # glEnd()
    
    # # -------------- eixo Z --------------
    # glBegin(GL_LINES)
    # glColor3f(0.0, 0.0, 1.0) # cor do eixo Z é azul
    # glVertex3f(0.0, 0.0, 0.0)
    # glVertex3f(0.0, 0.0, 10.0)
    # glEnd()

    # glBegin(GL_LINES)
    # glColor3f(0.0, 0.0, 1.0) # cor do eixo Z é azul
    # glVertex3f(0.0, 0.0, 0.0)
    # glVertex3f(0.0, 0.0, -10.0)
    # glEnd()

    #-------------- FUNDO -------------- 
    glPushMatrix()
    glTranslatef(0.0, 0.0, -5.0)
    glScalef(2.0,2.0,2.0)
    visualization.draw(fundo)
    glPopMatrix()

    glutSwapBuffers()

def KeysBoard(key, x, y):
    if key == b' ':
        adicionar_tiro()
        
        


def Keys(key, x, y):
    global cima, baixo, esquerda, direita, velocidade
    
    if(key == GLUT_KEY_LEFT ): 
        esquerda = 1
    elif(key == GLUT_KEY_RIGHT ): 
        direita = 1
    elif(key == GLUT_KEY_UP ): 
        cima = 1
    elif(key == GLUT_KEY_DOWN ):
        baixo = 1

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

# Função de atualização da nave
def movimentos_nave():
    global angulo_ovni, cima, esquerda, direita, velocidade

    if esquerda == 1:
        angulo_ovni += 5.0
        if velocidade > 1.0:
            velocidade -= 0.02
    if direita == 1:
        angulo_ovni -= 5.0
        if velocidade > 1.0:
            velocidade -= 0.02
    if cima == 1:
        move_cima_nave()
    if baixo == 1:
        move_baixo_nave()


# Função para mover a nave para frente
def move_cima_nave():
    global T1, T2, angulo_ovni, velocidade
    if velocidade < 4.0:
        velocidade += 0.02
    T1 += (0.10 * np.cos(np.radians(angulo_ovni))) * velocidade
    T2 += (0.10 * np.sin(np.radians(angulo_ovni))) * velocidade

def move_baixo_nave():
    global T1, T2, angulo_ovni, velocidade
    if velocidade < 4.0:
        velocidade += 0.02
    T1 -= (0.10 * np.cos(np.radians(angulo_ovni))) * velocidade
    T2 -= (0.10 * np.sin(np.radians(angulo_ovni))) * velocidade

# -------------- animacao do jogo --------------        
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)

    if random.random() < 0.03: # 3% de chance de gerar um novo asteroide
        adicionar_ovni()


def idle():
    global T1
    T1 -= 1
    
# -------------- Câmera do Jogo --------------
def resize(w, h): # função para a câmera acompanhar o movimento da nave
    glViewport(0, 0, w, h) # define a área de visualização
    glMatrixMode(GL_PROJECTION) # define o tipo de matriz
    glLoadIdentity()
    gluPerspective(25.0, w/h, 1.0, 100.0) # define o angulo_ovni de visão
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 40.0, # posição da câmera 
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
    luz_roxa = [1.0, 1.0, 1.0, 1.0]  # Cor da luz branca (RGBA)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_roxa)

    # Configurar a posição da fonte de luz
    luz_posicao = [5.0, 5.0, 5.0, 1.0]  # Posição da fonte de luz (x, y, z, w)
    glLightfv(GL_LIGHT0, GL_POSITION, luz_posicao)

    # Configurar o modelo de iluminação
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1098, 720)
    glutInitWindowPosition(100, 100)
    wind = glutCreateWindow('NAVE VERSUS OVNIS')
    init()

    ovni_obj = pywavefront.Wavefront('ovni.obj')
    
    nave = pywavefront.Wavefront('nave.obj')
    
    fundo = pywavefront.Wavefront('fundo.obj')
    
    tiro_obj = pywavefront.Wavefront('tiro.obj')

    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutTimerFunc(30,animacao,1)
    glutSpecialFunc(Keys) # controle de teclas especiais que não consegue escrever para movimentar a nave (cima, baixo, esquerda, direita)
    glutSpecialUpFunc(KeysUp) # controle de teclas para apertar e soltar ()
    glutKeyboardUpFunc(KeysBoard) # controle de teclas do alfabeto 
    glutMainLoop()
