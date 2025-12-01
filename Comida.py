import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *



import math
import os
import numpy as np
from OBJLoader import OBJ

class Comida:
    def __init__(self, tipo):
        # Posición y orientación
        self.position = [5, 2, 0]
        self.velocidad = 1
        self.theta = 0.0
        self.time = 0.0
        self.radio = 0.05
        self.rot = 0.0
        self.tipo = tipo
        self.jump = 0.0
        self.up = False
        
      
            
        
        # Cargar el objeto 3D usando la clase OBJ
        try:
            self.objeto = OBJ(os.path.join('objetos', 'happymeal.obj'), swapyz=True)
            print(f"Objeto cargado exitosamente COMIDA")
        except Exception as e:
            print(f"Error cargando objeto bebida: {e}")
            print("Error en COMIDA")
            self.objeto = None
        
      
    
    
    def draw(self):

        print("Dibujando comida  " )
        if self.objeto is None:
            return
            
        glPushMatrix() 
        glTranslatef(-1.5, 1.0, 0.0)
        #glTranslatef(self.position[0], self.position[1], self.position[2])

        glTranslatef(0.0, self.jump, 0.0)
        #glRotatef(270, 1, 0, 0)

        glScalef(2.5, 2.5, 2.5)
        
     
        self.objeto.render()


        glPopMatrix()




    def cleanup(self):
        """Liberar recursos OpenGL cuando se termine el juego"""
        if self.objeto:
            self.objeto.free()

