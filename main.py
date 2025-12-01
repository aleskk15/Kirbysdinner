import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import math
import requests
import os
import numpy as np

from Mesero import Mesero
from Cliente import Cliente
from Bartender import Bartender
from Cocinero import Cocinero
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
camera_distance = 8.0  
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




       
# Función para ver a donde ver 
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
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.4, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5, 1.0))


    glLightfv(GL_LIGHT1, GL_POSITION,  (100, 50, 100, 1.0))
    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0)) 
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.3, 0.3, 0.3, 1.0)) 
    glLightfv(GL_LIGHT1, GL_SPECULAR, (0.1, 0.1, 0.1, 1.0)) 

    glEnable(GL_LIGHT1)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)


# Función que muestra todos los objetos 
def display(mesero, bartender, clientes, cocinero, silla_modelo, sillas_data, ingredientes_data, snow_texture, ice_texture, comida_data, modelo_plato, modelo_plato2, modelo_bebida, mesa_model, comidacont, modelo_plato14, modelo_plato24, modelo_plato34):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()

    lookat(clientes[current_cliente].position[0], clientes[current_cliente].position[1], clientes[current_cliente].position[2])
    #lookat(mesero.position[0], mesero.position[1], mesero.position[2])
    #lookat(bartender.position[0], bartender.position[1], bartender.position[2])
    #lookat(cocinero.position[0], cocinero.position[1], cocinero.position[2])
    #print("Cliente 0", clientes[0].last_direction)
    #print("Cliente 1", clientes[1].last_direction)
    #print("Cliente 2", clientes[1].last_direction)

    dibujar_suelo()
    dibujar_paredes(snow_texture)
    dibujar_barra(ice_texture)


    mesero.draw()
    bartender.draw()
    cocinero.draw()
    for cliente in clientes:
        cliente.draw()

    # Dependiendo de los ingredientes se coloca una u otra 
    for ingrediente in ingredientes_data:
        ingrediente_x, ingrediente_z = ingrediente['pos']
        tipo = ingrediente['tipo']
        
        glPushMatrix()
        glTranslatef(ingrediente_x, 1.2, ingrediente_z)
        glRotatef(270, 1, 0, 0)
        glScalef(0.3, 0.3, 0.3)
        glEnable(GL_TEXTURE_2D)
        
        if tipo == "hamburguesa":
            modelo_plato.render()
        else:
            modelo_plato2.render()
        
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()


    for c in comida_data:
        tipo = c['tipo']
        nombre = c['n_comida']
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
            glRotatef(270, 1, 0, 0)
            
            glScalef(0.4, 0.4, 0.4)

            glEnable(GL_TEXTURE_2D)
            if nombre == "hamburguesa":
                if comidacont == 4:
                    modelo_plato14.render()
                elif comidacont == 3:
                    modelo_plato24.render()
                elif comidacont == 2:
                    modelo_plato34.render()
                elif comidacont == 1 or comidacont == 0:
                    modelo_plato.render()
                else:
                    modelo_plato14.render()
            else:
                modelo_plato2.render()
            
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

    #arreglos para los datos
    sillas_data = []
    comida_data = []
    ingredientes_data = []

    comidacont = 0

    INTERPOLATION_STEPS = 10  # Número de pasos que hace la interpolación intermedios
    
    # Se usan diccionarios para guardar los estados
    interpolation_data = {
        'mesero': {'target': None, 'current_step': 0, 'start': None, 'pending_status': None, 'pending_data': None},
        'bartender': {'target': None, 'current_step': 0, 'start': None, 'pending_status': None, 'pending_data': None},
        'cocinero': {'target': None, 'current_step': 0, 'start': None, 'pending_status': None, 'pending_data': None},
        'clientes': {}  # Se llenará dinámicamente para cada cliente
    }

    try:
        res = requests.get("http://localhost:8000/run")
        data = res.json()
        
        initialXM, initialZM = data['mesero'][0]['pos'][0] * 3, data['mesero'][0]['pos'][1] * 3
        initialXB, initialZB = data['bartender'][0]['pos'][0] * 3, data['bartender'][0]['pos'][1] * 3
        initialXC, initialZC = data['cocinero'][0]['pos'][0] * 3, data['cocinero'][0]['pos'][1] * 3
        initial_clientes_data = []
        initial_clientes_data = data.get('cliente', [])

        print("Datos iniciales recibidos:", data)

        if 'silla' in data and data['silla']:
            sillas_data = [(s['posicion'][0] * 3, s['posicion'][1] * 3) for s in data['silla']] 
            print(f"Posiciones de {len(sillas_data)} sillas cargadas.")
        
        if 'ingrediente' in data and data['ingrediente']:
            ingredientes_data = [
                {
                    'pos': (i['posicion'][0] * 3, i['posicion'][1] * 3),
                    'tipo': i.get('nombre', '')  
                } 
                for i in data['ingrediente']
            ]
            print(f"Posiciones de {len(ingredientes_data)} ingredientes cargados.")

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")
        print("Usando posiciones por defecto (0, 0) para iniciar.")
        initialXM, initialZM = 0, 0
        initialXB, initialZB = 0, 0
        initialXC, initialZC = 0, 0

    sillaPath = os.path.join('objetos', 'banco.obj')

    try:
        loaded_silla = OBJ(sillaPath, swapyz=True)
        print("Modelo cargado exitosamente.")
    except Exception as e:
        print(f"Error al cargar el OBJ: {e}")
        loaded_silla = None

    try:
        modelo_plato = OBJ(os.path.join('objetos', 'hamburger.obj'), swapyz=True)
        modelo_plato2 = OBJ(os.path.join('objetos', 'plate.obj'), swapyz=True)
        modelo_bebida = OBJ(os.path.join('objetos', 'drink.obj'), swapyz=True)
        modelo_plato14 = OBJ(os.path.join('objetos', 'comida1cuarto.obj'), swapyz=True)
        modelo_plato24 = OBJ(os.path.join('objetos', 'comida2cuartos.obj'), swapyz=True)
        modelo_plato34 = OBJ(os.path.join('objetos', 'comida3cuartos.obj'), swapyz=True)
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

    bartender = Bartender()
    bartender.position = [initialXB, 1.2, initialZB]

    cocinero = Cocinero()
    cocinero.position = [initialXC, 1.2, initialXC]

    clientes = []
    for cdata in initial_clientes_data:
        cliente = Cliente()
        cliente.position = [cdata['pos'][0] * 3, 1.2, cdata['pos'][1] * 3]
        clientes.append(cliente)

    running = True
    clock = pygame.time.Clock()
    
    
    frame_counter = 0
    API_UPDATE_INTERVAL = 10  # Cada cuantos frames se actualiza el api
    
    while running:
        frame_counter += 1
        
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

        # Se actualiza el api
        if frame_counter % API_UPDATE_INTERVAL == 0:
            try:
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
                
                EPS = 0.2

                # MESERO
                if len(data.get('mesero', [])) > 0:
                    try:
                        m = data['mesero'][0]
                        mesero_new_pos_x = m['pos'][0] * 3
                        mesero_new_pos_z = m['pos'][1] * 3

                        # Se pone la interpolación
                        if interpolation_data['mesero']['target'] is None:
                            interpolation_data['mesero']['start'] = [mesero.position[0], mesero.position[2]]
                        else:
                            interpolation_data['mesero']['start'] = interpolation_data['mesero']['target']
                        
                        interpolation_data['mesero']['target'] = [mesero_new_pos_x, mesero_new_pos_z]
                        interpolation_data['mesero']['current_step'] = 0

                        # Se calcula la dirección para la rotación
                        dx = mesero_new_pos_x - mesero.position[0]
                        dz = mesero_new_pos_z - mesero.position[2]

                        if abs(dx) >= EPS or abs(dz) >= EPS:
                            if abs(dx) > abs(dz):
                                new_dir = "R" if dx > 0 else "L"
                            else:
                                new_dir = "D" if dz > 0 else "U"

                            key = (getattr(mesero, 'last_direction', 'U'), new_dir)
                            if key in ROTATION_RULES:
                                rot = ROTATION_RULES[key]
                                if rot == "R":
                                    mesero.rotate("R")
                                elif rot == "L":
                                    mesero.rotate("L")
                                elif rot == "RR":
                                    mesero.rotate("R"); mesero.rotate("R")

                            mesero.last_direction = new_dir

                        mesero.isitMoving = bool(m.get('isMoving', False))
                        
                        # Se guardan los status
                        interpolation_data['mesero']['pending_status'] = m.get('status', '')
                        interpolation_data['mesero']['pending_data'] = m

                    except Exception as e:
                        print(f"[MESERO] Error procesando mesero: {e}")

                # BARTENDER
                if len(data.get('bartender', [])) > 0:
                    try:
                        b = data['bartender'][0]
                        bartender_new_pos_x = b['pos'][0] * 3
                        bartender_new_pos_z = b['pos'][1] * 3

                        # Se pone la interpolación
                        if interpolation_data['bartender']['target'] is None:
                            interpolation_data['bartender']['start'] = [bartender.position[0], bartender.position[2]]
                        else:
                            interpolation_data['bartender']['start'] = interpolation_data['bartender']['target']
                        
                        interpolation_data['bartender']['target'] = [bartender_new_pos_x, bartender_new_pos_z]
                        interpolation_data['bartender']['current_step'] = 0

                        dx = bartender_new_pos_x - bartender.position[0]
                        dz = bartender_new_pos_z - bartender.position[2]

                        if abs(dx) >= EPS or abs(dz) >= EPS:
                            if abs(dx) > abs(dz):
                                new_dir = "R" if dx > 0 else "L"
                            else:
                                new_dir = "D" if dz > 0 else "U"

                            key = (getattr(bartender, 'last_direction', 'U'), new_dir)
                            if key in ROTATION_RULES:
                                rot = ROTATION_RULES[key]
                                if rot == "R":
                                    bartender.rotate("R")
                                elif rot == "L":
                                    bartender.rotate("L")
                                elif rot == "RR":
                                    bartender.rotate("R"); bartender.rotate("R")

                            bartender.last_direction = new_dir

                        bartender.isitMoving = bool(b.get('isMoving', False))
                        
                        # Se gusrasm los status
                        interpolation_data['bartender']['pending_status'] = b.get('status', '')
                        interpolation_data['bartender']['pending_data'] = b

                    except Exception as e:
                        print(f"[BARTENDER] Error procesando bartender: {e}")

                # COCINERO
                if len(data.get('cocinero', [])) > 0:
                    try:
                        cc = data['cocinero'][0]
                        cocinero_new_pos_x = cc['pos'][0] * 3
                        cocinero_new_pos_z = cc['pos'][1] * 3

                        # Interpolación
                        if interpolation_data['cocinero']['target'] is None:
                            interpolation_data['cocinero']['start'] = [cocinero.position[0], cocinero.position[2]]
                        else:
                            interpolation_data['cocinero']['start'] = interpolation_data['cocinero']['target']
                        
                        interpolation_data['cocinero']['target'] = [cocinero_new_pos_x, cocinero_new_pos_z]
                        interpolation_data['cocinero']['current_step'] = 0

                        dx = cocinero_new_pos_x - cocinero.position[0]
                        dz = cocinero_new_pos_z - cocinero.position[2]

                        if abs(dx) >= EPS or abs(dz) >= EPS:
                            if abs(dx) > abs(dz):
                                new_dir = "R" if dx > 0 else "L"
                            else:
                                new_dir = "D" if dz > 0 else "U"

                            key = (getattr(cocinero, 'last_direction', 'U'), new_dir)
                            if key in ROTATION_RULES:
                                rot = ROTATION_RULES[key]
                                if rot == "R":
                                    cocinero.rotate("R")
                                elif rot == "L":
                                    cocinero.rotate("L")
                                elif rot == "RR":
                                    cocinero.rotate("R"); cocinero.rotate("R")

                            cocinero.last_direction = new_dir

                        cocinero.isitMoving = bool(cc.get('isMoving', False))
                        
                        # colocar status
                        interpolation_data['cocinero']['pending_status'] = cc.get('status', '')
                        interpolation_data['cocinero']['pending_data'] = cc

                    except Exception as e:
                        print(f"[COCINERO] Error procesando cocinero: {e}")

                # CLIENTES
                clientes_actualizados = []
                try:
                    for i, cdata in enumerate(data.get('cliente', [])):
                        if i >= len(clientes):
                            nuevo_cliente = Cliente()
                            nuevo_cliente.position = [cdata['pos'][0] * 3, 1.2, cdata['pos'][1] * 3]
                            clientes.append(nuevo_cliente)

                        cliente = clientes[i]
                        cliente_new_pos_x = cdata['pos'][0] * 3
                        cliente_new_pos_z = cdata['pos'][1] * 3

                        # Interpolación
                        if i not in interpolation_data['clientes']:
                            interpolation_data['clientes'][i] = {'target': None, 'current_step': 0, 'start': None, 'pending_status': None, 'pending_data': None}
                        
                        if interpolation_data['clientes'][i]['target'] is None:
                            interpolation_data['clientes'][i]['start'] = [cliente.position[0], cliente.position[2]]
                        else:
                            interpolation_data['clientes'][i]['start'] = interpolation_data['clientes'][i]['target']
                        
                        interpolation_data['clientes'][i]['target'] = [cliente_new_pos_x, cliente_new_pos_z]
                        interpolation_data['clientes'][i]['current_step'] = 0
                        
                        # Se pone los status
                        interpolation_data['clientes'][i]['pending_status'] = cdata.get('status', '')
                        interpolation_data['clientes'][i]['pending_data'] = cdata

                        # manejo del sentarse
                        if cliente.sitting:
                            if cliente.last_direction == "U":
                                cliente.rotate("R"); cliente.last_direction = "R"
                            elif cliente.last_direction == "D":
                                cliente.rotate("R"); cliente.last_direction = "R"
                        else:
                            dx = cliente_new_pos_x - cliente.position[0]
                            dz = cliente_new_pos_z - cliente.position[2]

                            if abs(dx) >= EPS or abs(dz) >= EPS:
                                if abs(dx) > abs(dz):
                                    new_dir = "R" if dx > 0 else "L"
                                else:
                                    new_dir = "D" if dz > 0 else "U"

                                key = (getattr(cliente, 'last_direction', 'U'), new_dir)
                                if key in ROTATION_RULES:
                                    rot = ROTATION_RULES[key]
                                    if rot == "R":
                                        cliente.rotate("R")
                                    elif rot == "L":
                                        cliente.rotate("L")
                                    elif rot == "RR":
                                        cliente.rotate("R"); cliente.rotate("R")

                                cliente.last_direction = new_dir

                        cliente.isitMoving = bool(cdata.get('isMoving', False))

                        if cdata.get('isMoving', False) and cliente.sitting:
                            cliente.sit()

                        clientes_actualizados.append(cliente)
                except Exception as e:
                    print(f"[CLIENTES] Error procesando clientes: {e}")

                clientes = clientes_actualizados

                # COMIDA
                comida_data.clear() 
                if 'comida' in data and len(data['comida']) > 0:
                    for c in data['comida']:
                        status = c['status']
                        if status != "orden" and status != "preparando":
                            tipo = c['nombre']
                            n_comida = c['tipo_plato']
                            x = c['posicion'][0] * 3
                            y = 2.5
                            z = c['posicion'][1] * 3
                            status = c['status']
                            comida_data.append({'tipo': tipo, 'n_comida':n_comida ,'x': x, 'y': y, 'z': z, 'status': status})

            except Exception as e:
                print(f"[API] Error al obtener datos del servidor: {e}")

        # MESERO
        if interpolation_data['mesero']['target'] is not None:
            interp = interpolation_data['mesero']
            if interp['current_step'] < INTERPOLATION_STEPS:
                t = (interp['current_step'] + 1) / INTERPOLATION_STEPS
                new_x = interp['start'][0] + (interp['target'][0] - interp['start'][0]) * t
                new_z = interp['start'][1] + (interp['target'][1] - interp['start'][1]) * t
                mesero.update(new_x, new_z)
                interp['current_step'] += 1
                
                # Se ponen animaciones
                if interp['current_step'] >= INTERPOLATION_STEPS:
                    status = interp['pending_status']
                    if status == 'tomaOrden':
                        mesero.grabcont = 0
                    elif status == 'agarraOrden':
                        if getattr(mesero, 'grabcont', 0) < 2:
                            mesero.grab(); mesero.grabcont = getattr(mesero, 'grabcont', 0) + 1
                    elif status == 'mandaOrden':
                        mesero.servecont = 0
                    elif status == 'ordenEntregada':
                        if getattr(mesero, 'servecont', 0) < 2:
                            mesero.serve(); mesero.servecont = getattr(mesero, 'servecont', 0) + 1

        # BARTENDER
        if interpolation_data['bartender']['target'] is not None:
            interp = interpolation_data['bartender']
            if interp['current_step'] < INTERPOLATION_STEPS:
                t = (interp['current_step'] + 1) / INTERPOLATION_STEPS
                new_x = interp['start'][0] + (interp['target'][0] - interp['start'][0]) * t
                new_z = interp['start'][1] + (interp['target'][1] - interp['start'][1]) * t
                bartender.update(new_x, new_z)
                interp['current_step'] += 1
                
                # Se ponen las animaciones
                if interp['current_step'] >= INTERPOLATION_STEPS:
                    status = interp['pending_status']
                    if status == 'preparaBebida':
                        bartender.bebida_showing = True
                        if getattr(bartender, 'shakecont', 0) < 8:
                            bartender.shake(); bartender.shakecont = getattr(bartender, 'shakecont', 0) + 1
                        else:
                            bartender.bebida_showing = False
                    elif status == 'bebidaEntregada':
                        if bartender.bebida_showing:
                            bartender.bebida_showing = False
                        if getattr(bartender, 'servecont', 0) < 2:
                            bartender.serve(); bartender.servecont = getattr(bartender, 'servecont', 0) + 1
                    elif status == 'recibeBebida':
                        bartender.servecont = 0
                        bartender.shakecont = 0
                    else:
                        bartender.bebida_showing = False

        # COCINERO
        if interpolation_data['cocinero']['target'] is not None:
            interp = interpolation_data['cocinero']
            if interp['current_step'] < INTERPOLATION_STEPS:
                t = (interp['current_step'] + 1) / INTERPOLATION_STEPS
                new_x = interp['start'][0] + (interp['target'][0] - interp['start'][0]) * t
                new_z = interp['start'][1] + (interp['target'][1] - interp['start'][1]) * t
                cocinero.update(new_x, new_z)
                interp['current_step'] += 1
                
                # EAnimaciones cuanyo ya se llegue al objetivo
                if interp['current_step'] >= INTERPOLATION_STEPS:
                    status = interp['pending_status']
                    cc = interp['pending_data']
                    if status == 'cocinaOrden':
                        cocinero.comida_showing = True
                        cocinero.tipo_comida = cc.get('tipo_comida', '') if cc else ''
                        print(cocinero.tipo_comida)
                        if getattr(cocinero, 'cookcont', 0) < 8:
                            cocinero.cook(); cocinero.cookcont = getattr(cocinero, 'cookcont', 0) + 1
                    else:
                        cocinero.comida_showing = False

        # CLIENTES
        for i, cliente in enumerate(clientes):
            if i in interpolation_data['clientes'] and interpolation_data['clientes'][i]['target'] is not None:
                interp = interpolation_data['clientes'][i]
                if interp['current_step'] < INTERPOLATION_STEPS:
                    t = (interp['current_step'] + 1) / INTERPOLATION_STEPS
                    new_x = interp['start'][0] + (interp['target'][0] - interp['start'][0]) * t
                    new_z = interp['start'][1] + (interp['target'][1] - interp['start'][1]) * t
                    cliente.update(new_x, new_z)
                    interp['current_step'] += 1
                    
                    # Animaciones cuando se llega al objetivo
                    if interp['current_step'] >= INTERPOLATION_STEPS:
                        status = interp['pending_status']
                        if status == 'sentarse':
                            if getattr(cliente, 'sitcont', 0) <= 1:
                                cliente.sit(); cliente.sitcont = getattr(cliente, 'sitcont', 0) + 1
                        elif status == 'comiendo':

                            comidacont = cliente.comidacont
                            cliente.comidacont += 1

                            cliente.sitcont = 0
                            if getattr(cliente, 'eatcont', 0) < 4:
                                cliente.eat(); cliente.eatcont = getattr(cliente, 'eatcont', 0) + 1

        display(mesero, bartender, clientes, cocinero, loaded_silla, sillas_data, ingredientes_data, snow_texture, ice_texture, comida_data, modelo_plato, modelo_plato2, modelo_bebida, mesa_model, comidacont, modelo_plato14, modelo_plato24, modelo_plato34)
        
        clock.tick(60)

    if loaded_silla: 
        loaded_silla.free()
        
    mesero.cleanup()
    for cliente in clientes:
        cliente.cleanup()
    pygame.quit()
    

if __name__ == "__main__":
    main()