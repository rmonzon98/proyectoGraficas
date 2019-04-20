#Funciones
#Universidad del Valle de Guatemala
#Raúl Monzon 17014
# -*- coding: utf-8 -*-


import struct


"""
Clase que representa archivo Bitmap
"""
class ClaseBMP(object):

        def write(self, filename):
                file = open(filename, "bw")
                ancho_t = self.padding(4,self.width)
                altura_t = self.padding(4,self.height)
                file.write(self.char("B"))
                file.write(self.char("M"))
                file.write(self.dword(14 + 40 + ancho_t * altura_t))
                file.write(self.dword(0))
                file.write(self.dword(14+40))
                file.write(self.dword(40))
                file.write(self.dword(self.width))
                file.write(self.dword(self.height))
                file.write(self.word(1))
                file.write(self.word(24))
                file.write(self.dword(0))
                file.write(self.dword(ancho_t*altura_t))
                file.write(self.dword(0))
                file.write(self.dword(0))
                file.write(self.dword(0))
                file.write(self.dword(0))
                for x in range(ancho_t):
                        for y in range(self.height):
                                if (x<self.width and y<self.height):
                                        file.write(self.framebuffer[y][x])
                                else:
                                        file.write(self.char("c"))
                file.close()
                
        def char(self,c):
                return struct.pack("c", c.encode("ascii"))
        
        def word(self,c):
                return struct.pack("h", c)
        
        def dword(self,c):
                return struct.pack("l", c)

        def padding(self, base,c):
                if(c % base== 0):
                        return c
                else:
                        while (c%base):
                                c +=1
                        return c

        """
        Inicializa valores del archivo (constructor)
        """
        def __init__(self, width, height):
                self.width = abs(int(width))
                self.height = abs(int(height))
                self.framebuffer = []
                self.zbuffer=[]
                self.clear()

        """
        "pinta" el bitmap de un color
        """
        def clear(self, r=0, b=139, g=0):
                self.framebuffer =[
                        [
                                self.color(r,g,b)
                                        for x in range(self.width)
                        ]
                        for y in range(self.height)
                ]
                self.zbuffer= [ [-float('inf') for x in range(self.width)] for y in range(self.height)]

        """
        Define bytes del color.
        """
        def color(self, r=0, g=0, b=0):
                if (r > 255 or g > 255 or b > 255 or r < 0 or g < 0 or b <0):
                        r = 0
                        g = 0
                        b = 0
                return bytes([b,g,r])

        """
        Cambia color de un pixel en especifico que esta dentro de los limites
        Si esta fuera de los limites no realiza ninguna acción
        """
        def point(self,x,y,color):
                if(x < self.width and y < self.height):
                        self.framebuffer[x][y] =color

        """
        sets
        """
        def setZBValue(self, x,y,value):
                if x<self.width and y<self.height:
                        self.zbuffer[x][y]=value
        """
        gets
        """
        def getZBValue(self,x,y):
                if x<self.width and y<self.height:
                        return self.zbuffer[x][y]
                else:
                	return -float("inf")
                

"""
Clase que representa el .obj
"""
class OBJCTF(object):

        """
        Constructor
        """
        def __init__(self, filename):
                self.filename=filename
                self.faces=[]
                self.vertex=[]
                self.nvertex=[]
                self.materials=None
                self.tvert=[]
                self.materialF=[]

        """
        Cargar documento .obj
        """
        def load(self):
                #Abrimos archivo
                doc = open(self.filename,"r")
                faces=[]
                contFaces=0
                mtlActual="default"
                mtlAnterior=mtlActual
                indice=[]
                #archivamos todas las lineas del documento
                lineas=doc.readlines()
                print("Cargando archivo .obj :)")
                #Inspeccionamos archivo linea por linea
                for line in  lineas:
                        #Arreglamos el valor de line de manera que sea más fácil inspeccionar y podamos tomar lo que nos importa 
                        line=line.rstrip().split(" ")

                        #Encontramos material library heading
                        if line[0] =="mtllib":
                                mtlFile = class_MTL(line[1])
                                if mtlFile.isFileO():
                                        mtlFile.load()
                                        self.materials=mtlFile.materials
                                else:
                                        self.faces=[]

                        #encontramos vertices                
                        elif line[0] == "v":
                                line.pop(0)
                                if line[0]=="":
                                        i=1
                                else:
                                        i=0
                                self.vertex.append((float(line[i]), float(line[i+1]), float(line[i+2])))

                        #Encontramos materials      
                        elif line[0] == "usemtl":
                                if self.materials:
                                        mtlAnterior=mtlActual
                                        mtlActual= line[1]
                                        indice.append(contFaces)
                                        if len(indice)==2:
                                                self.materialF.append((indice,mtlAnterior))
                                                indice=[indice[1]+1]
                                        
                        #Encontramos caras
                        elif line[0] == "f":
                                line.pop(0)
                                face = []
                                for i in line:
                                        i = i.split("/")
                                        if i[1]=="":
                                                face.append((int(i[0]),int(i[-1])))
                                        else:
                                                face.append((int(i[0]),int(i[-1]),int(i[1])))
                                contFaces=contFaces+1
                                self.faces.append(face)
                                
                                
			#Encontramos vertices normalizados			
                        elif line[0] == "vn":
                                line.pop(0)
                                if line[0]=="":
                                        i=1
                                else:
                                        i=0
                                self.nvertex.append((float(line[i]), float(line[i+1]), float(line[i+2])))
                        #Encontramos texture vertices
                        elif line[0]=="vt":
                                line.pop(0)
                                self.tvert.append((float(line[0]), float(line[1])))
                if len(indice)<2 and self.materials:
                        indice.append(contFaces)
                        self.materialF.append((indice,mtlActual))
                        indice=[indice[1]+1]
                print("Archivo .obj analizado!!! :)")
                doc.close()
                


                        
        """
        gets
        """
        def getFacesL(self):#Faces
                return self.faces
        def getVertexL(self):#Vertex
                return self.vertex
        def getVertexNormalL(self):
                return self.nvertex
        def getMaterials(self):
                return self.materials
        def getMaterialF(self):
                return self.materialF
        def getTVertex(self):
                return self.tvert


"""
Clase que representa objeto .MTL
"""
class class_MTL(object):

        """
        Constructor
        """
        def __init__(self,nombreArchivo):
                self.nombreArchivo=nombreArchivo
                self.readMTL()
                self.materials={}
                self.archivo=self.readMTL()

        """
        Verifica que el doc con el .obj este abierto
        """
        def isFileO(self):
                return self.mtldoc
        
        """
        lee archivo .MTL
        """
        def readMTL(self):
        	try:
        		file = open(self.nombreArchivo,"r")
        		self.mtldoc= True
        		return file
        	except Exception as e:
        		self.mtldoc=False

        """
        Analiza el archivo .mtl y guarda los materiales
        """
        def load(self):
                #Verificamos que el archivo fue encontrado
                print("Cargando archivo .mtl :)")
                if self.isFileO():
                        materialActual= None
                        opticalD,ambientColor,emissiveC,shini,difuseColor,trans,ill,ds=0,0,0,0,0,0,0,0
                        #Analizamos el archivo linea por linea
                        for linea in self.archivo.readlines():
                                linea=linea.split(" ")
                                #encontramos optical density
                                if linea[0]=="Ni":
                                        opticalD=float(linea[1])
                                #encontramos ambient color
                                elif linea[0]=="Ka":
                                        ambientColor=(float(linea[1]), float(linea[2]), float(linea[3]))
                                #Encontramos emissive coeficient
                                elif linea[0]=="Ke":
                                        emissiveC=(float(linea[1]), float(linea[2]), float(linea[3]))
                                #Encontramos Shininess
                                elif linea[0]=="Ns":
                                        shini=float(linea[1])
                                #Encontramos difuse color
                                elif linea[0]=="Kd":
                                        difuseColor= (float(linea[1]), float(linea[2]), float(linea[3]))
                                #Encontramos difuse color
                                elif linea[0] == "d" or linea[0] == "Tr":
                                        trans=(float(linea[1]), linea[0])
                                #Encontramos illumination
                                elif linea[0]=="illum":
                                        ill=int(linea[1])
                                #Encontramos un material nuevo
                                elif linea[0]=="newmtl":
                                        materialActual=linea[1].rstrip()
                                #Encontramos specular color
                                elif linea[0] == "ks":
                                        ds=(float(line[1]), float(line[2]), float(line[3]))
                                        
                                elif materialActual:
                                        self.materials[materialActual]=MaterialClase(materialActual,ambientColor,difuseColor,ds,emissiveC,trans,ill,opticalD)
                        if materialActual not in self.materials.keys():
                                self.materials[materialActual]=MaterialClase(materialActual,ambientColor,difuseColor,ds,emissiveC,trans,ill,opticalD)

"""
Clase que representa un material
"""
class MaterialClase(object):

        """
        Constructor
        """
        def __init__(self,materialActual,ambientColor,difuseColor,ds,emissiveC,trans,ill,opticalD):
               self.name=materialActual.rstrip()
               self.ambientColor=ambientColor
               self.difuseColor=difuseColor
               self.ds=ds
               self.emissiveC=emissiveC
               self.trans=trans
               self.ill=ill
               self.opticalD=opticalD

"""
Clase para Texturas
"""
class Texture(object):

        """
        Constructor
        """
        def __init__(self,nombreA):
                self.archivo=nombreA
                self.text=None
                self.load()
        """
        Abre archivo
        """
        def load(self):
                print("Cargando textura :)")
                self.texto=ClaseBMP(0,0)
                try:
                        self.text.load(self.archivo)
                except:
                        self.text=None

        def write(self):
                self.text.write(self.archivo[:len(self.archivo)-4]+"text.bmp")

        def textured(self):
                return True if self.text else False

        """
        Gets
        """
        def getColor(self, x,y, intensity=1):
                if y==1:
                        px= self.text.width-1
                else:
                        px=int (y*self.texto.width)
                if x==1:
                        py=self.text.height
                else:
                        py=int(x*self.text.height)
                return  bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, self.__text.framebuffer[py][px]))
        

