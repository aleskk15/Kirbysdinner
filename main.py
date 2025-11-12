import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import math
import random 
import requests
import os
import numpy as np

from Mesero import Mesero
from Cliente import Cliente
from OBJLoader import OBJ

screen_width = 800
screen_height = 600
ancho_tablero = 14 * 3  
largo_tablero = 17 * 3  


X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

FOVY = 60
ZNEAR = 0.1
ZFAR = 2000.0
EYE_X, EYE_Y, EYE_Z = 200, 0, 100  
CENTER_X, CENTER_Y, CENTER_Z = 0, 0, 0
UP_X, UP_Y, UP_Z = 0, 1, 0



camera_yaw = 0.0   
camera_pitch = 20.0 
camera_distance = 10.0  
mouse_sensitivity = 0.2

current_cliente = 0



from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def cargar_textura(ruta):
    textura_surface = pygame.image.load(ruta)
    textura_data = pygame.image.tostring(textura_surface, "RGBA", True)
    ancho, alto = textura_surface.get_rect().size

    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ancho, alto, 0, GL_RGBA, GL_UNSIGNED_BYTE, textura_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return textura_id



def dibujar_suelo():
    glColor3f(0.6, 0.8, 1.0)  
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-ancho_tablero, 0, -largo_tablero)
    glTexCoord2f(5, 0); glVertex3f(ancho_tablero, 0, -largo_tablero)
    glTexCoord2f(5, 10); glVertex3f(ancho_tablero, 0, largo_tablero)
    glTexCoord2f(0, 10); glVertex3f(-ancho_tablero, 0, largo_tablero)
    glEnd()

def dibujar_paredes(textura_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor3f(1, 1, 1)

    altura = 50
    rep = 2  
    glBegin(GL_QUADS) 
    glTexCoord2f(0, 0); glVertex3f(0, 0, largo_tablero)
    glTexCoord2f(rep, 0); glVertex3f(ancho_tablero, 0, largo_tablero)
    glTexCoord2f(rep, rep); glVertex3f(ancho_tablero, altura, largo_tablero)
    glTexCoord2f(0, rep); glVertex3f(0, altura, largo_tablero)
    glEnd()
    
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(rep, 0); glVertex3f(ancho_tablero, 0, 0)
    glTexCoord2f(rep, rep); glVertex3f(ancho_tablero, altura, 0)
    glTexCoord2f(0, rep); glVertex3f(0, altura, 0)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(rep, 0); glVertex3f(0, 0, largo_tablero)
    glTexCoord2f(rep, rep); glVertex3f(0, altura, largo_tablero)
    glTexCoord2f(0, rep); glVertex3f(0, altura, 0)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(ancho_tablero, 0, largo_tablero)
    glTexCoord2f(rep, 0); glVertex3f(ancho_tablero, 0, 0)
    glTexCoord2f(rep, rep); glVertex3f(ancho_tablero, altura, 0)
    glTexCoord2f(0, rep); glVertex3f(ancho_tablero, altura, largo_tablero)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def dibujar_barra(textura_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor3f(1, 1, 1)

    x1 = 10.5 * 3          
    x2 = x1 + 3 
    z1 = 10.5 * 3          
    z2 = 13 * 3         
    y1 = 0.0
    y2 = 2.5
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x1, y2, z1)
    glTexCoord2f(1, 0); glVertex3f(x2, y2, z1)
    glTexCoord2f(1, 1); glVertex3f(x2, y2, z2)
    glTexCoord2f(0, 1); glVertex3f(x1, y2, z2)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x1, y1, z1)
    glTexCoord2f(1, 0); glVertex3f(x2, y1, z1)
    glTexCoord2f(1, 1); glVertex3f(x2, y1, z2)
    glTexCoord2f(0, 1); glVertex3f(x1, y1, z2)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x1, y1, z2)
    glTexCoord2f(1, 0); glVertex3f(x2, y1, z2)
    glTexCoord2f(1, 1); glVertex3f(x2, y2, z2)
    glTexCoord2f(0, 1); glVertex3f(x1, y2, z2)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x1, y1, z1)
    glTexCoord2f(1, 0); glVertex3f(x2, y1, z1)
    glTexCoord2f(1, 1); glVertex3f(x2, y2, z1)
    glTexCoord2f(0, 1); glVertex3f(x1, y2, z1)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x1, y1, z1)
    glTexCoord2f(1, 0); glVertex3f(x1, y1, z2)
    glTexCoord2f(1, 1); glVertex3f(x1, y2, z2)
    glTexCoord2f(0, 1); glVertex3f(x1, y2, z1)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x2, y1, z1)
    glTexCoord2f(1, 0); glVertex3f(x2, y1, z2)
    glTexCoord2f(1, 1); glVertex3f(x2, y2, z2)
    glTexCoord2f(0, 1); glVertex3f(x2, y2, z1)
    glEnd()

    glDisable(GL_TEXTURE_2D)




       

def lookat(player_x, player_y, player_z):
    global camera_yaw, camera_pitch, camera_distance

    yaw_rad = math.radians(camera_yaw)
    pitch_rad = math.radians(camera_pitch)

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
    pygame.display.set_caption("Kirby's dinner")
    
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

def display(mesero, clientes, silla_modelo, sillas_data, snow_texture, ice_texture, comida_data, modelo_plato, modelo_bebida, mesa_model):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()

    lookat(clientes[current_cliente].position[0], clientes[current_cliente].position[1], clientes[current_cliente].position[2])
    #print("Cliente 0", clientes[0].last_direction)
    #print("Cliente 1", clientes[1].last_direction)
    #print("Cliente 2", clientes[1].last_direction)

    dibujar_suelo()
    dibujar_paredes(snow_texture)
    dibujar_barra(ice_texture)


    mesero.draw()
    for cliente in clientes:
        cliente.draw()


    for c in comida_data:
        tipo = c['tipo']
        x, y, z = c['x'], c['y'], c['z']
        status =  c['status']

        if status == "entregada":
                x += 2.5
                y = 2.0

        glPushMatrix()
        glTranslatef(x, y, z) 

        

        matriz_act = glGetFloatv(GL_MODELVIEW_MATRIX) 

        if tipo == 'bebida' and modelo_bebida is not None:
            glScalef(0.05, 0.05, 0.05)
            
            glEnable(GL_TEXTURE_2D)

            modelo_bebida.render()
            glDisable(GL_TEXTURE_2D)
        elif tipo == 'plato' and modelo_plato is not None:
            glRotate(270, 1, 0, 0)
            
            glScalef(0.4, 0.4, 0.4)

            glEnable(GL_TEXTURE_2D)

            modelo_plato.render()
            glDisable(GL_TEXTURE_2D)
        glPopMatrix()


    if silla_modelo is not None:
        banco_y = 1.0 

        glEnable(GL_NORMALIZE)

        for idx, (banco_x, banco_z) in enumerate(sillas_data):
            glPushMatrix()
            #glTranslatef(banco_x, banco_y, banco_z)
            #glRotatef(90, 1, 0, 0)   
            #glScalef(0.5, 0.5, 0.5)
            MB_T = np.array([
                [0.5, 0, 0, 0],
                [0, 0, 0.5, 0],
                [0, -0.5, 0, 0],
                [banco_x, banco_y, banco_z, 1]
            ])
            glEnable(GL_TEXTURE_2D)
            matriz_act = glGetFloatv(GL_MODELVIEW_MATRIX) 
            m = matriz_act.flatten() 
            m0,m1,m2,m3, m4,m5,m6,m7, m8,m9,m10,m11, m12,m13,m14,m15 = m
            result = [
                [   
                    0.5*m0 + 0*m4 + 0*m8 + 0*m12,
                    0.5*m1 + 0*m5 + 0*m9 + 0*m13,
                    0.5*m2 + 0*m6 + 0*m10 + 0*m14,
                    0.5*m3 + 0*m7 + 0*m11 + 0*m15
                ],
                [ 
                    0*m0 + 0*m4 + 0.5*m8 + 0*m12,
                    0*m1 + 0*m5 + 0.5*m9 + 0*m13,
                    0*m2 + 0*m6 + 0.5*m10 + 0*m14,
                    0*m3 + 0*m7 + 0.5*m11 + 0*m15
                ],
                [  
                    0*m0 + -0.5*m4 + 0*m8 + 0*m12,
                    0*m1 + -0.5*m5 + 0*m9 + 0*m13,
                    0*m2 + -0.5*m6 + 0*m10 + 0*m14,
                    0*m3 + -0.5*m7 + 0*m11 + 0*m15
                ],
                [   
                    banco_x*m0 + banco_y*m4 + banco_z*m8 + 1*m12,
                    banco_x*m1 + banco_y*m5 + banco_z*m9 + 1*m13,
                    banco_x*m2 + banco_y*m6 + banco_z*m10 + 1*m14,
                    banco_x*m3 + banco_y*m7 + banco_z*m11 + 1*m15
                ]
            ]

            glLoadMatrixf(result)

            silla_modelo.render()
            glDisable(GL_TEXTURE_2D)
            glPopMatrix()

            if mesa_model is not None:
                glPushMatrix()
                mesax = banco_x + 3
                mesa_y = 0.0
                mesaz = banco_z
                #glTranslatef(mesax, mesa_y, mesaz)
                #glScalef(0.08, 0.08, 0.08)
                MM_T = np.array([
                    [0.08, 0, 0, 0],
                    [0, 0.08, 0, 0],
                    [0, 0, 0.08, 0],
                    [mesax, mesa_y, mesaz, 1]
                ])

                matriz_act = glGetFloatv(GL_MODELVIEW_MATRIX) 
                m = matriz_act.flatten() 
                m0,m1,m2,m3, m4,m5,m6,m7, m8,m9,m10,m11, m12,m13,m14,m15 = m


                result = [
                    [  
                        0.08*m0 + 0*m4 + 0*m8 + 0*m12,
                        0.08*m1 + 0*m5 + 0*m9 + 0*m13,
                        0.08*m2 + 0*m6 + 0*m10 + 0*m14,
                        0.08*m3 + 0*m7 + 0*m11 + 0*m15
                    ],
                    [  
                        0*m0 + 0.08*m4 + 0*m8 + 0*m12,
                        0*m1 + 0.08*m5 + 0*m9 + 0*m13,
                        0*m2 + 0.08*m6 + 0*m10 + 0*m14,
                        0*m3 + 0.08*m7 + 0*m11 + 0*m15
                    ],
                    [   
                        0*m0 + 0*m4 + 0.08*m8 + 0*m12,
                        0*m1 + 0*m5 + 0.08*m9 + 0*m13,
                        0*m2 + 0*m6 + 0.08*m10 + 0*m14,
                        0*m3 + 0*m7 + 0.08*m11 + 0*m15
                    ],
                    [  
                        mesax*m0 + mesa_y*m4 + mesaz*m8 + 1*m12,
                        mesax*m1 + mesa_y*m5 + mesaz*m9 + 1*m13,
                        mesax*m2 + mesa_y*m6 + mesaz*m10 + 1*m14,
                        mesax*m3 + mesa_y*m7 + mesaz*m11 + 1*m15
                    ]
                ]

                glLoadMatrixf(result)


                mesa_model.render()
                glPopMatrix()



        glDisable(GL_NORMALIZE)



 

    pygame.display.flip()
    
    

def main():
    global camera_yaw, camera_pitch, camera_distance, current_cliente  

    Init()

    pygame.event.set_grab(False)  
    pygame.mouse.set_visible(True)


    snow_texture = cargar_textura("objetos/nieve_pared.png")
    ice_texture = cargar_textura("objetos/hielo.jpg")

    sillas_data = []
    comida_data = []

    try:
        res = requests.get("http://localhost:8000/run")
        data = res.json()
        
        initialXM, initialZM = data['mesero'][0]['pos'][0] * 3, data['mesero'][0]['pos'][1] * 3
        #initialXC1, initialZC1 = data['cliente'][0]['pos'][0] * 3, data['cliente'][0]['pos'][1] * 3
        initial_clientes_data = []
        initial_clientes_data = data.get('cliente', [])

        
        print("Datos iniciales recibidos:", data)

        if 'silla' in data and data['silla']:
            sillas_data = [(s['posicion'][0] * 3, s['posicion'][1] * 3) for s in data['silla']] 
            print(f"Posiciones de {len(sillas_data)} sillas cargadas.")

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")
        print("Usando posiciones por defecto (0, 0) para iniciar.")
        initialXM, initialZM = 0, 0
        initialXC1, initialZC1 = 0, 0

    sillaPath = os.path.join('objetos', 'banco.obj')

    try:
        loaded_silla = OBJ(sillaPath, swapyz=True)
        print("Modelo cargado exitosamente.")
    except Exception as e:
        print(f"Error al cargar el OBJ: {e}")
        loaded_silla = None

    try:
        modelo_plato = OBJ(os.path.join('objetos', 'hamburger.obj'), swapyz=True)
        modelo_bebida = OBJ(os.path.join('objetos', 'drink.obj'), swapyz=True)
        print("Modelos de comida cargados correctamente.")
    except Exception as e:
        print(f"Error al cargar modelos de comida: {e}")
        modelo_plato = modelo_bebida = None
   
    try:
        mesa_model = OBJ(os.path.join('objetos', 'mesa.obj'), swapyz=True)
        print("Modelo de mesa cargado correctamente.")
    except Exception as e:
        print(f"Error al cargar el modelo de mesa: {e}")
        mesa_model = None

    mesero = Mesero()    
    mesero.position = [initialXM, 1.2, initialZM]

    clientes = []
    for cdata in initial_clientes_data:
        cliente = Cliente()
        cliente.position = [cdata['pos'][0] * 3, 1.2, cdata['pos'][1] * 3]
        clientes.append(cliente)





    running = True
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False 
            elif event.type == KEYDOWN:
                if event.key == pygame.K_RIGHT:  
                    current_cliente = (current_cliente + 1) % 3

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4: 
                camera_distance = max(1.0, camera_distance - 1.0)
            elif event.button == 5: 
                camera_distance += 1.0 

        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        buttons = pygame.mouse.get_pressed()

        if buttons[2]: 
            camera_yaw += mouse_dx * mouse_sensitivity
            camera_pitch -= mouse_dy * mouse_sensitivity
            camera_pitch = max(-89, min(89, camera_pitch))

        pygame.mouse.set_pos(screen_width // 2, screen_height // 2) 
                

        #mesero.update(data['mesero'][0]['pos'][0], data['mesero'][0]['pos'][1])    
        #cliente.update(data['cliente'][0]['pos'][0], data['cliente'][0]['pos'][1])
        
        res = requests.get("http://localhost:8000/run")
        data = res.json()

        ROTATION_RULES = {
            ("U", "R"): "R",
            ("U", "L"): "L",
            ("U", "D"): "RR",

            ("D", "R"): "L",
            ("D", "L"): "R",
            ("D", "U"): "RR",

            ("R", "U"): "L",
            ("R", "D"): "R",
            ("R", "L"): "RR",

            ("L", "U"): "R",
            ("L", "D"): "L",
            ("L", "R"): "RR",
        }
        
        if len(data['mesero']) > 0:
            mesero.lastposition = mesero.position
            m = data['mesero'][0]
            mesero_new_pos_x = m['pos'][0] * 3
            mesero_new_pos_z = m['pos'][1] * 3
            dx = mesero_new_pos_x- mesero.lastposition[0]
            dz = mesero_new_pos_z - mesero.lastposition[2]


            if abs(dx) > abs(dz):
                new_dir = "R" if dx > 0 else "L"
            else:
                new_dir = "D" if dz > 0 else "U"

            key = (mesero.last_direction, new_dir)
            if key in ROTATION_RULES:
                rot = ROTATION_RULES[key]
                if rot == "R":
                    mesero.rotate("R")
                elif rot == "L":
                    mesero.rotate("L")
                elif rot == "RR":  
                    mesero.rotate("R")
                    mesero.rotate("R")

            mesero.last_direction = new_dir

              
            
            mesero.update(mesero_new_pos_x, mesero_new_pos_z)
            mesero.isitMoving = (data['mesero'][0]['isMoving'])

            if (data['mesero'][0]['status']) == 'tomaOrden':
                mesero.grabcont = 0
            
            if (data['mesero'][0]['status']) == 'agarraOrden':
                if mesero.grabcont < 2:
                    mesero.grab()
                    mesero.grabcont += 1

            if (data['mesero'][0]['status']) == 'mandaOrden':
                mesero.servecont = 0
                
            if (data['mesero'][0]['status']) == 'ordenEntregada':
                if mesero.servecont < 2:
                    mesero.serve()
                    mesero.servecont += 1

        clientes_actualizados = []

        

        for i, cdata in enumerate(data['cliente']):
            if i >= len(clientes):
                nuevo_cliente = Cliente()
                nuevo_cliente.position = [cdata['pos'][0] * 3, 1.2, cdata['pos'][1] * 3]
                clientes.append(nuevo_cliente)

            cliente = clientes[i]

            cliente.lastposition = cliente.position
            cliente_new_pos_x = cdata['pos'][0] * 3
            cliente_new_pos_z = cdata['pos'][1] * 3
            if cliente.sitting:
                if cliente.last_direction == "U" and cliente.sitRotcont == 0:
                    cliente.rotate("R")
                    cliente.last_direction = "R"
                    cliente.sitRotcont += 1

            else:
                dx = cliente_new_pos_x - cliente.lastposition[0]
                dz = cliente_new_pos_z - cliente.lastposition[2]

                if abs(dx) > abs(dz):
                    new_dir = "R" if dx > 0 else "L"
                else:
                    new_dir = "D" if dz > 0 else "U"

                key = (cliente.last_direction, new_dir)
                if key in ROTATION_RULES:
                    rot = ROTATION_RULES[key]
                    if rot == "R":
                        cliente.rotate("R")
                    elif rot == "L":
                        cliente.rotate("L")
                    elif rot == "RR":
                        cliente.rotate("R")
                        cliente.rotate("R")

                cliente.last_direction = new_dir

            cliente.update(cdata['pos'][0] * 3, cdata['pos'][1] * 3)
            cliente.isitMoving = cdata['isMoving']

            if cdata['isMoving'] and cliente.sitting:
                cliente.sit()

            if cdata['status'] == 'sentarse':
                if cliente.sitcont <= 1:
                    cliente.sit()
                    #cliente.rotate("L")

                    #cliente.last_direction = "R"
                    cliente.sitcont += 1

            elif cdata['status'] == 'comiendo':
                cliente.sitcont = 0
                if cliente.eatcont < 4:
                    cliente.eat()
                    cliente.eatcont += 1

            clientes_actualizados.append(cliente)

        clientes = clientes_actualizados
    
  

            

        comida_data.clear() 
        if 'comida' in data and len(data['comida']) > 0:
            for c in data['comida']:
                status = c['status']
                if status != "orden" and status != "preparando":
                    tipo = c['nombre']
                    x = c['posicion'][0] * 3
                    y = 2.5
                    z = c['posicion'][1] * 3
                    status = c['status']
                    comida_data.append({'tipo': tipo, 'x': x, 'y': y, 'z': z, 'status': status})




        display(mesero, clientes, loaded_silla, sillas_data, snow_texture,  ice_texture, comida_data, modelo_plato, modelo_bebida, mesa_model)
        
        clock.tick(60)

    if loaded_silla: 
        loaded_silla.free()
        
    mesero.cleanup()
    for cliente in clientes:
        cliente.cleanup()
    pygame.quit()
    

if __name__ == "__main__":
    main()
