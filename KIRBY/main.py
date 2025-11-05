import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import math
import random 
import requests

from Mesero import Mesero
from Cliente import Cliente

res = requests.get("http://localhost:8000/run")
data = res.json()
initialXM, initialZM = data['mesero'][0]['pos'][0] * 5, data['mesero'][0]['pos'][1] * 5
initialXC1, initialZC1 = data['cliente'][0]['pos'][0] * 5, data['cliente'][0]['pos'][1] * 5


print(data)
# Configuración de pantalla y tablero
screen_width = 800
screen_height = 600

# Dimensiones rectangulares del tablero
ancho_tablero = 200  # Ancho del rectángulo (eje X)
largo_tablero = 400  # Largo del rectángulo (eje Z)


#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

# Parámetros de cámara y proyección
FOVY = 60
ZNEAR = 0.1
ZFAR = 2000.0
EYE_X, EYE_Y, EYE_Z = 200, 0, 100  # Posición ajustada para ver mejor el rectángulo
CENTER_X, CENTER_Y, CENTER_Z = 0, 0, 0
UP_X, UP_Y, UP_Z = 0, 1, 0

camera_yaw = 0.0   # Rotación en Y (izq-der)
camera_pitch = 20.0 # Rotación en X (arriba-abajo)
camera_distance = 10.0  # Qué tan lejos está la cámara del jugador
mouse_sensitivity = 0.2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *




def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)


def dibujar_suelo():
    glColor3f(0.3, 0.9, 0.3)  # Color verde
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-ancho_tablero, 0, -largo_tablero)
    glTexCoord2f(5, 0); glVertex3f(ancho_tablero, 0, -largo_tablero)
    glTexCoord2f(5, 10); glVertex3f(ancho_tablero, 0, largo_tablero)
    glTexCoord2f(0, 10); glVertex3f(-ancho_tablero, 0, largo_tablero)
    glEnd()

       

def lookat(player_x, player_y, player_z):
    global camera_yaw, camera_pitch, camera_distance

    # Convertir ángulos a radianes
    yaw_rad = math.radians(camera_yaw)
    pitch_rad = math.radians(camera_pitch)

    # Cámara en coordenadas esféricas
    eye_x = player_x + camera_distance * math.cos(pitch_rad) * math.sin(yaw_rad)
    eye_y = player_y + camera_distance * math.sin(pitch_rad)
    eye_z = player_z + camera_distance * math.cos(pitch_rad) * math.cos(yaw_rad)

    glLoadIdentity()
    gluLookAt(eye_x, eye_y, eye_z,
              player_x, player_y, player_z,
              0, 1, 0)


def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Penguin dinner")
    
    glClearColor(0.5, 0.7, 1.0, 0.1)
    #glEnable(GL_DEPTH_TEST)
    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.2, 0.2, 0.2, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)

def display(mesero, cliente):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()

    #lookat(mesero.position[0], mesero.position[1], mesero.position[2])
    lookat(cliente.position[0], cliente.position[1], cliente.position[2])

    dibujar_suelo()

    
    mesero.draw()
    cliente.draw()

    
    pygame.display.flip()
    
    

def main():
    global camera_yaw, camera_pitch, camera_distance  

    Init()
   
    mesero = Mesero()    
    mesero.position = [initialXM, 1.2, initialZM]
    cliente = Cliente()
    cliente.position = [initialXC1, 1.2, initialZC1]


    running = True
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    cliente.sit()
                elif event.key == pygame.K_x:
                    cliente.eat() 
                elif event.key == pygame.K_m:
                    mesero.grab() 
                elif event.key == pygame.K_n: 
                    mesero.serve() 
                

        #mesero.update(data['mesero'][0]['pos'][0], data['mesero'][0]['pos'][1])    
        #cliente.update(data['cliente'][0]['pos'][0], data['cliente'][0]['pos'][1])
        
        res = requests.get("http://localhost:8000/run")
        data = res.json()
        
        # Actualizar mesero (si hay al menos uno)
        if len(data['mesero']) > 0:
            m = data['mesero'][0]
            mesero.update(m['pos'][0] * 5, m['pos'][1] * 5)

        # Actualizar cliente (si hay al menos uno)
        if len(data['cliente']) > 0:
            c = data['cliente'][0]
            cliente.update(c['pos'][0] * 5, c['pos'][1] * 5)

        
        # Movimiento relativo del mouse
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        buttons = pygame.mouse.get_pressed()

        if buttons[2]:  # Botón derecho presionado → girar cámara
            camera_yaw += mouse_dx * mouse_sensitivity
            camera_pitch -= mouse_dy * mouse_sensitivity
            camera_pitch = max(-89, min(89, camera_pitch))  

        display(mesero, cliente)
        
        clock.tick(60)
        
    mesero.cleanup()
    cliente.cleanup()
    pygame.quit()
    

if __name__ == "__main__":
    main()