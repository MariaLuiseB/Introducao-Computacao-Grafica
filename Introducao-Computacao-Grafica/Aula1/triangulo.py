from OpenGL.GL import *
from OpenGL.GLUT import *

def display(): 
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0) # pinta quadrado de vermelho (RGB)
    glBegin(GL_POLYGON) # desenha um poligono (triangulo) preenchido com a cor que foi estabelecida na linha 6
    glVertex3i(-1, 0, 0) # coordenadas do vértice 1 (canto esquerdo inferior do triangulo)
    glVertex3i(1,0,0)
    glVertex3i(0,1,0)
    
    glEnd()
    glFlush() # limpa o buffer de desenho


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(350, 350)
glutInitWindowPosition(100, 100) # posição da janela na tela
wind = glutCreateWindow("Triangulo")
glClearColor(0.0, 0.0, 0.0, 0.0) # limpa a janela de exibição com a cor preta
glutDisplayFunc(display) # chama a função display da linha 4 
glutMainLoop() # entra no loop de processamento de eventos da GLUT
