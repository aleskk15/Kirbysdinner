import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *



import math
import os
import numpy as np

from Cliente_M import Cliente_M
from Cliente_P import Cliente_P

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
                            shininess = max(0.0, min(128.0, float(shininess)))  # Limitar rango
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

class Cliente:
    def __init__(self, objeto_archivo="princefluff/fluffCuerpo.obj", swap_yz=False):

        self.position = [0, 0, 0]
        self.direction = [1.0, 0.0, 0.0]  
        self.velocidad = 1
        self.wabble = 0.0 
        self.rotacion = 0.0
        self.time = 0.0
        self.sitting = False

        self.eating = False 
        self.rotServing = 0.0
        self.isitMoving = False 
        self.sitcont = 0
        self.eatcont = 0
        self.last_direction = "R"
        self.lastposition = [0, 0, 0]
        self.sitRotcont = 0
        self.comidacont = 0

        
        try:
            self.objeto = OBJ(objeto_archivo, swapyz=swap_yz)
            print(f"Objeto cargado exitosamente: {objeto_archivo}")
        except Exception as e:
            print(f"Error cargando objeto {objeto_archivo}: {e}")
            self.objeto = None

        self.manos = [
            Cliente_M(position =[1.5, 0.1, 0.0], direction = "R"),
            Cliente_M(position =[-1.5, 0.1, 0.0], direction = "L")
        ]

        self.pies = [
            Cliente_P(position =[0.5, -1.7, 0.0], direction = "R"),
            Cliente_P(position =[-0.8, -1.7, 0.0], direction = "L")
        ]
    
    
    def draw(self):
        if self.objeto is None:
            return

        glPushMatrix()
        px = self.position[0]
        py = self.position[1]
        pz = self.position[2]

        ro = self.rotacion
        wa = self.wabble

        sinr = math.sin(math.radians(ro))
        cosr = math.cos(math.radians(ro))
        sinw = math.sin(math.radians(wa))
        cosw = math.cos(math.radians(wa))

        #glTranslatef(self.position[0], self.position[1], self.position[2])
        #glRotatef(270, 0, 1, 0)
        #glRotatef(self.rotacion, 0, 1, 0)
        #glRotatef(self.wabble, 0, 0, 1)
        #glScalef(0.5, 0.5, 0.5)

        MC_T = np.array([
            [0.5*sinr*cosw, 0.5*sinw, 0.5*cosr*cosw, 0],
            [-0.5*sinr*sinw, 0.5*cosw, -0.5*cosr*sinw, 0],
            [-0.5*cosr, 0, 0.5*sinr, 0],
            [px, py, pz, 1]
        ])
        
        matriz_act = glGetFloatv(GL_MODELVIEW_MATRIX) 
        m = matriz_act.flatten() 
        m0,m1,m2,m3, m4,m5,m6,m7, m8,m9,m10,m11, m12,m13,m14,m15 = m

        result = [
            [
                0.5*sinr*cosw*m0  + 0.5*sinw*m4  + 0.5*cosr*cosw*m8  + 0*m12,
                0.5*sinr*cosw*m1  + 0.5*sinw*m5  + 0.5*cosr*cosw*m9  + 0*m13,
                0.5*sinr*cosw*m2  + 0.5*sinw*m6  + 0.5*cosr*cosw*m10 + 0*m14,
                0.5*sinr*cosw*m3  + 0.5*sinw*m7  + 0.5*cosr*cosw*m11 + 0*m15
            ],
            [
                -0.5*sinr*sinw*m0 + 0.5*cosw*m4  + -0.5*cosr*sinw*m8  + 0*m12,
                -0.5*sinr*sinw*m1 + 0.5*cosw*m5  + -0.5*cosr*sinw*m9  + 0*m13,
                -0.5*sinr*sinw*m2 + 0.5*cosw*m6  + -0.5*cosr*sinw*m10 + 0*m14,
                -0.5*sinr*sinw*m3 + 0.5*cosw*m7  + -0.5*cosr*sinw*m11 + 0*m15
            ],
            [
                -0.5*cosr*m0 + 0*m4 + 0.5*sinr*m8 + 0*m12,
                -0.5*cosr*m1 + 0*m5 + 0.5*sinr*m9 + 0*m13,
                -0.5*cosr*m2 + 0*m6 + 0.5*sinr*m10 + 0*m14,
                -0.5*cosr*m3 + 0*m7 + 0.5*sinr*m11 + 0*m15
            ],
            [
                px*m0 + py*m4 + pz*m8  + 1*m12,
                px*m1 + py*m5 + pz*m9  + 1*m13,
                px*m2 + py*m6 + pz*m10 + 1*m14,
                px*m3 + py*m7 + pz*m11 + 1*m15
            ]
        ]

        #result = np.dot(MC_T, matriz_act)

        glLoadMatrixf(result) 
                


        for mano in self.manos:
            mano.draw()
        for pie in self.pies:
            pie.draw()


        self.objeto.render()



        glPopMatrix()

        #glPushMatrix()
        #glColor3f(1, 1, 0)
        #glBegin(GL_LINES)
        #glVertex3f(self.position[0], self.position[1], self.position[2])
        #glVertex3f(
        #    self.position[0] + self.direction[0] * 3,
        #    self.position[1],
        #    self.position[2] + self.direction[2] * 3
        #)
        #glEnd()
        #glPopMatrix()



    
    def update(self, pos_x, pos_z):
        self.position[0] = pos_x
        self.position[2] = pos_z

        if self.isitMoving and not self.sitting and not self.eating:
            self.position[1] = 1.2
            for mano in self.manos:
                mano.moving = True
                mano.time += 2
            for pie in self.pies:
                if pie.rot_dir == 1:  
                    pie.rot += 5
                    if pie.rot >= 15:
                        pie.rot = 15
                        pie.rot_dir = -1
                else:  
                    pie.rot -= 5
                    if pie.rot <= -15:
                        pie.rot = -15
                        pie.rot_dir = 1

  
            self.time += 0.5
            self.wabble = 5.0 * math.sin(self.time)
        else:
            for mano in self.manos:
                mano.moving = False
                mano.time = 0.0
            for pie in self.pies:
                if not self.sitting and self.eating:
                    pie.rot = 0.0
            self.wabble = 0.0
            self.time = 0.0


    def rotate(self, direction):
        if direction == "R":
            self.rotacion -= 90
        elif direction == "L":
            self.rotacion += 90
        
    def sit(self):
        for pie in self.pies:
            if pie.rot == 0:
                self.sitting = True
                self.position[1] = 2.0
                pie.rot = 90
            else:
                pie.rot = 0
                self.sitting = False
            
    
    def eat(self):
        for mano in self.manos:
            if mano.rot == 0:
                mano.eating = True
                for i in range(90):
                    mano.rot +=1
            else:
                for i in range(90):
                    mano.rot -=1
                mano.eating = False
        


    def cleanup(self):
        """Liberar recursos OpenGL cuando se termine el juego"""
        if self.objeto:
            self.objeto.free()


