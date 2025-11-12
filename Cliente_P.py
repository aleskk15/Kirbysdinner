import pygame
from pygame.locals import *

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
        self.mtl = {} 
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
                
                valid_face = True
                for i, vertex_idx in enumerate(vertices):
                    if vertex_idx < 1 or vertex_idx > len(self.vertices):
                        print(f"Índice de vértice inválido: {vertex_idx}")
                        valid_face = False
                        break
                    
                    if normals[i] > 0 and (normals[i] < 1 or normals[i] > len(self.normals)):
                        print(f"Índice de normal inválido: {normals[i]}")
                        valid_face = False
                        break
                    
                    if texture_coords[i] > 0 and (texture_coords[i] < 1 or texture_coords[i] > len(self.texcoords)):
                        print(f"Índice de texcoord inválido: {texture_coords[i]}")
                        valid_face = False
                        break
                
                if not valid_face:
                    continue
                if material and material in self.mtl:
                    mtl = self.mtl[material]
                    
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
                            shininess = mtl['Ns'][0] if isinstance(mtl['Ns'], list) else mtl['Ns']
                            shininess = max(0.0, min(128.0, float(shininess)))  
                            glMaterialf(GL_FRONT, GL_SHININESS, shininess)
                        
                        if 'texture_Kd' in mtl:
                            glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
                        else:
                            glBindTexture(GL_TEXTURE_2D, 0) 
                            if 'Kd' in mtl and len(mtl['Kd']) >= 3:
                                glColor3f(*mtl['Kd'][:3])
                    except Exception as e:
                        print(f"Error aplicando material {material}: {e}")
                        glBindTexture(GL_TEXTURE_2D, 0)
                        glColor3f(0.8, 0.8, 0.8)
                else:
                    glBindTexture(GL_TEXTURE_2D, 0)
                    glColor3f(0.8, 0.8, 0.8) 
                if len(vertices) == 3:
                    glBegin(GL_TRIANGLES)
                elif len(vertices) == 4:
                    glBegin(GL_QUADS)
                else:
                    glBegin(GL_POLYGON)
                
                try:
                    for i in range(len(vertices)):
                        if normals[i] > 0 and normals[i] <= len(self.normals):
                            glNormal3fv(self.normals[normals[i] - 1])
                        
                        if texture_coords[i] > 0 and texture_coords[i] <= len(self.texcoords):
                            glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                        
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
            print("Intentando recrear display list...")
            self.generate()

    def free(self):
        if self.gl_list > 0:
            glDeleteLists(self.gl_list, 1)
            self.gl_list = 0

class Cliente_P:
    def __init__(self, objeto_archivo="kirby/Pata2.obj", swap_yz=False, position = [0.0, 0.0, 0.0], direction = "L"):
        self.position = position
        self.velocidad = 1
        self.theta = 0.0
        self.direction = direction
        self.time = 0.0
        self.rot = 0.0
        self.offset = 1
        if self.direction == "L":
            self.rot_dir = 1
        else:
            self.rot_dir = -1

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

        px = self.position[0]
        py = self.position[1]
        pz = self.position[2]

        of = self.offset
        ro = self.rot


        sinr = math.sin(math.radians(ro))
        cosr = math.cos(math.radians(ro))
        sino = math.sin(math.radians(of))
        coso = math.cos(math.radians(of))
        #glTranslatef(self.position[0], self.position[1], self.position[2])

        #glTranslatef(0.0, self.offset, 0.0)   

        #glRotatef(self.rot, 1, 0, 0)

        #glTranslatef(0.0, -self.offset, 0.0)

        #glScalef(0.7, 0.7, 0.7)

        MC_T = np.array([
            [0.7, 0, 0, 0],
            [0, 0.7*cosr, 0.7*sinr, 0],
            [0, -0.7*sinr, 0.7*cosr, 0],
            [px, -of*cosr + py + of, pz - of*sinr, 1]
        ])

        matriz_act = glGetFloatv(GL_MODELVIEW_MATRIX) 
        m = matriz_act.flatten() 
        m0,m1,m2,m3, m4,m5,m6,m7, m8,m9,m10,m11, m12,m13,m14,m15 = m


        #result = np.dot(MC_T, matriz_act)

        result = [
            [   
                0.7*m0 + 0*m4 + 0*m8 + 0*m12,
                0.7*m1 + 0*m5 + 0*m9 + 0*m13,
                0.7*m2 + 0*m6 + 0*m10 + 0*m14,
                0.7*m3 + 0*m7 + 0*m11 + 0*m15
            ],
            [   
                0*m0 + 0.7*cosr*m4 + 0.7*sinr*m8 + 0*m12,
                0*m1 + 0.7*cosr*m5 + 0.7*sinr*m9 + 0*m13,
                0*m2 + 0.7*cosr*m6 + 0.7*sinr*m10 + 0*m14,
                0*m3 + 0.7*cosr*m7 + 0.7*sinr*m11 + 0*m15
            ],
            [   
                0*m0 + -0.7*sinr*m4 + 0.7*cosr*m8 + 0*m12,
                0*m1 + -0.7*sinr*m5 + 0.7*cosr*m9 + 0*m13,
                0*m2 + -0.7*sinr*m6 + 0.7*cosr*m10 + 0*m14,
                0*m3 + -0.7*sinr*m7 + 0.7*cosr*m11 + 0*m15
            ],
            [   
                px*m0 + (-of*cosr + py + of)*m4 + (pz - of*sinr)*m8 + 1*m12,
                px*m1 + (-of*cosr + py + of)*m5 + (pz - of*sinr)*m9 + 1*m13,
                px*m2 + (-of*cosr + py + of)*m6 + (pz - of*sinr)*m10 + 1*m14,
                px*m3 + (-of*cosr + py + of)*m7 + (pz - of*sinr)*m11 + 1*m15
            ]
        ]


        glLoadMatrixf(result) 


        self.objeto.render()
        glPopMatrix()



    def cleanup(self):
        """Liberar recursos OpenGL cuando se termine el juego"""
        if self.objeto:
            self.objeto.free()
