from OpenGL.GL import *
from OpenGL.GLUT import *
from math import * 

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)  # Define a cor vermelha para o círculo
    glBegin(GL_POLYGON)

    num_segmentos = 100  # Número de segmentos para aproximar o círculo
    raio = 0.8  # Raio do círculo
    x_centro = 0.0  # Coordenada x do centro do círculo
    y_centro = 0.0  # Coordenada y do centro do círculo

    for i in range(num_segmentos):
        angulo = 2.0 * pi * i / num_segmentos # ângulo do segmento atual do círculo (em radianos)
        x = x_centro + raio * cos(angulo) # coordenada x do ponto atual do círculo que começa no centro e vai até o raio 
        y = y_centro + raio * sin(angulo) # coordenada y do ponto atual do círculo
        glVertex3f(x, y, 0) # desenha o ponto atual do círculo

    glEnd()
    glFlush()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(350, 350)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Circulo")
glClearColor(0.0, 0.0, 0.0, 0.0)
glutDisplayFunc(display)
glutMainLoop()
