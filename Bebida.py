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

class Bebida:
    def __init__(self):
        # Posición y orientación
        self.position = [5, 2, 0]
        self.velocidad = 1
        self.theta = 0.0
        self.time = 0.0
        self.radio = 0.05
        self.rot = 0.0
        
        
        # Cargar el objeto 3D usando la clase OBJ
        try:
            self.objeto = OBJ(os.path.join('objetos', 'drink.obj'), swapyz=True)
            print(f"Objeto cargado exitosamente BEBIDA")
        except Exception as e:
            print(f"Error cargando objeto bebida: {e}")
            print("Error en bebida")
            self.objeto = None
        
      
    
    
    def draw(self):
        if self.objeto is None:
            return
            
        glPushMatrix() 
        #glTranslatef(self.position[0], self.position[1], self.position[2])


        glScalef(0.08, 0.08, 0.08)
        
     
        self.objeto.render()


        glPopMatrix()




    def cleanup(self):
        """Liberar recursos OpenGL cuando se termine el juego"""
        if self.objeto:
            self.objeto.free()

