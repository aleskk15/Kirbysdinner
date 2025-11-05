import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *



import math
import os
import numpy as np

class OBJ:
    generate_on_init = True
    @classmethod
    def loadTexture(cls, imagefile):
        surf = pygame.image.load(imagefile)
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        return texid

    @classmethod
    def loadMaterial(cls, filename):
        contents = {}
        mtl = None
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'newmtl':
                mtl = contents[values[1]] = {}
            elif mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")
            elif values[0] == 'map_Kd':
                # load the texture referred to by this declaration
                mtl[values[0]] = values[1]
                imagefile = os.path.join(dirname, mtl['map_Kd'])
                mtl['texture_Kd'] = cls.loadTexture(imagefile)
            else:
                mtl[values[0]] = list(map(float, values[1:]))
        return contents

    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        self.mtl = {}  # Inicializar diccionario de materiales
        dirname = os.path.dirname(filename)

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                try:
                    self.mtl = self.loadMaterial(os.path.join(dirname, values[1]))
                    print(f"Materiales cargados: {list(self.mtl.keys())}")
                except Exception as e:
                    print(f"Error cargando MTL: {e}")
                    self.mtl = {}
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
        
        print(f"Objeto cargado: {len(self.vertices)} vértices, {len(self.faces)} caras")
        if self.generate_on_init:
            self.generate()

    
        
    def generate(self):
        try:
            # Verificar que tenemos datos válidos
            if not self.vertices or not self.faces:
                print("Error: No hay vértices o caras para renderizar")
                return
            
            self.gl_list = glGenLists(1)
            if self.gl_list == 0:
                print("Error: No se pudo crear la display list")
                return
            
            glNewList(self.gl_list, GL_COMPILE)
            glEnable(GL_TEXTURE_2D)
            glFrontFace(GL_CCW)
            
            for face in self.faces:
                vertices, normals, texture_coords, material = face
                
                # Verificar que todos los índices son válidos
                valid_face = True
                for i, vertex_idx in enumerate(vertices):
                    if vertex_idx < 1 or vertex_idx > len(self.vertices):
                        print(f"Índice de vértice inválido: {vertex_idx}")
                        valid_face = False
                        break
                    
                    # Verificar normales si existen
                    if normals[i] > 0 and (normals[i] < 1 or normals[i] > len(self.normals)):
                        print(f"Índice de normal inválido: {normals[i]}")
                        valid_face = False
                        break
                    
                    # Verificar coordenadas de textura si existen
                    if texture_coords[i] > 0 and (texture_coords[i] < 1 or texture_coords[i] > len(self.texcoords)):
                        print(f"Índice de texcoord inválido: {texture_coords[i]}")
                        valid_face = False
                        break
                
                if not valid_face:
                    continue
                
                # Manejar caso donde no hay material definido
                if material and material in self.mtl:
                    mtl = self.mtl[material]
                    
                    # Aplicar propiedades del material con validación
                    try:
                        if 'Ka' in mtl and len(mtl['Ka']) >= 3:
                            ambient = mtl['Ka'][:3] + [1.0]
                            glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
                        
                        if 'Kd' in mtl and len(mtl['Kd']) >= 3:
                            diffuse = mtl['Kd'][:3] + [1.0]
                            glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
                        
                        if 'Ks' in mtl and len(mtl['Ks']) >= 3:
                            specular = mtl['Ks'][:3] + [1.0]
                            glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
                        
                        if 'Ns' in mtl:
                            # Asegurar que Ns sea un float válido
                            shininess = mtl['Ns'][0] if isinstance(mtl['Ns'], list) else mtl['Ns']
                            shininess = max(0.0, min(128.0, float(shininess)))  # Limitar rango
                            glMaterialf(GL_FRONT, GL_SHININESS, shininess)
                        
                        if 'texture_Kd' in mtl:
                            # use diffuse texmap
                            glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
                        else:
                            # just use diffuse colour
                            glBindTexture(GL_TEXTURE_2D, 0)  # Desactivar textura
                            if 'Kd' in mtl and len(mtl['Kd']) >= 3:
                                glColor3f(*mtl['Kd'][:3])
                    except Exception as e:
                        print(f"Error aplicando material {material}: {e}")
                        # Usar material por defecto
                        glBindTexture(GL_TEXTURE_2D, 0)
                        glColor3f(0.8, 0.8, 0.8)
                else:
                    # Material por defecto
                    glBindTexture(GL_TEXTURE_2D, 0)
                    glColor3f(0.8, 0.8, 0.8)  # Gris por defecto

                # Usar GL_TRIANGLES en lugar de GL_POLYGON para mayor compatibilidad
                if len(vertices) == 3:
                    glBegin(GL_TRIANGLES)
                elif len(vertices) == 4:
                    glBegin(GL_QUADS)
                else:
                    glBegin(GL_POLYGON)
                
                try:
                    for i in range(len(vertices)):
                        # Aplicar normal si existe (índices en OBJ empiezan en 1)
                        if normals[i] > 0 and normals[i] <= len(self.normals):
                            glNormal3fv(self.normals[normals[i] - 1])
                        
                        # Aplicar coordenadas de textura si existen
                        if texture_coords[i] > 0 and texture_coords[i] <= len(self.texcoords):
                            glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                        
                        # Aplicar vértice (índices en OBJ empiezan en 1)
                        if vertices[i] > 0 and vertices[i] <= len(self.vertices):
                            glVertex3fv(self.vertices[vertices[i] - 1])
                        
                except Exception as e:
                    print(f"Error renderizando cara: {e}")
                    glEnd()
                    continue
                
                glEnd()
            
            glDisable(GL_TEXTURE_2D)
            glEndList()
            print(f"Display list creada exitosamente: {self.gl_list}")
            
        except Exception as e:
            print(f"Error en generate(): {e}")
            if self.gl_list > 0:
                glDeleteLists(self.gl_list, 1)
                self.gl_list = 0

    def render(self):
        # Verificar que la display list sea válida antes de usarla
        if self.gl_list == 0:
            print("Error: Display list no válida")
            return
        
        if not glIsList(self.gl_list):
            print(f"Error: Display list {self.gl_list} no es válida")
            return
        
        try:
            glCallList(self.gl_list)
        except Exception as e:
            print(f"Error al renderizar: {e}")
            # Intentar recrear la display list
            print("Intentando recrear display list...")
            self.generate()

    def free(self):
        if self.gl_list > 0:
            glDeleteLists(self.gl_list, 1)
            self.gl_list = 0

class Mesero_M:
    def __init__(self, objeto_archivo="kirby/manos.obj", swap_yz=False, position = [0.0, 0.0, 0.0], direction = "L", moving= False):
        # Posición y orientación
        self.position = position
        self.velocidad = 1
        self.theta = 0.0
        self.direction = direction
        self.time = 0.0
        self.radio = 0.05
        self.moving = moving
        self.grabbing = False
        self.rot = 0.0

        
        
        # Cargar el objeto 3D usando la clase OBJ
        try:
            self.objeto = OBJ(objeto_archivo, swapyz=swap_yz)
            print(f"Objeto cargado exitosamente: {objeto_archivo}")
        except Exception as e:
            print(f"Error cargando objeto {objeto_archivo}: {e}")
            self.objeto = None
        
      
    
    
    def draw(self):
        if self.objeto is None:
            return
            
        glPushMatrix() 
        glTranslatef(self.position[0], self.position[1], self.position[2])
        if self.direction == "R":
            glRotatef(180, 0, 1, 0)   

        if self.moving:  
            glTranslate(0, math.cos(self.time)*self.radio, math.sin(self.time)*self.radio) 
        else:
            pass

        if self.grabbing: 
            if self.direction == "R":
                glRotate(-self.rot, 1, 0, 0)
            else:
                glRotatef(self.rot, 1, 0, 0)
            if self.direction == "L":
                glRotatef(-90, 0, 1, 0)
            else:
                glRotatef(90, 0, 1, 0)


        glScalef(0.7, 0.7, 0.7)
        
        self.objeto.render()


        glPopMatrix()




    def cleanup(self):
        """Liberar recursos OpenGL cuando se termine el juego"""
        if self.objeto:
            self.objeto.free()

