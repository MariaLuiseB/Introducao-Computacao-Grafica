from OpenGL.GL import *
from OpenGL.GLUT import *

def display(): 
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0) # pinta quadrado de vermelho (RGB)
    glBegin(GL_POLYGON) # desenha um poligono (quadrado) preenchido com a cor que foi estabelecida na linha 6
    glVertex3f(0.0, 0.0, 0.0) # coordenadas do vértice 1 (canto esquerdo inferior do quadrado) 
    glVertex3f(1.0, 0.0, 0.0) # coordenadas do vértice 2 (canto direito inferior do quadrado)
    glVertex3f(1.0, 1.0, 0.0) # coordenadas do vértice 3 (canto direito superior do quadrado)
    glVertex3f(0.0, 1.0, 0.0) # coordenadas do vértice 4 (canto esquerdo superior do quadrado)
    
    glEnd()
    glFlush() # limpa o buffer de desenho


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(350, 350)
glutInitWindowPosition(100, 100) # posição da janela na tela
wind = glutCreateWindow("Quadrado")
glClearColor(0.0, 0.0, 0.0, 0.0) # limpa a janela de exibição com a cor preta
glutDisplayFunc(display) # chama a função display da linha 4 
glutMainLoop() # entra no loop de processamento de eventos da GLUT
