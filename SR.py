#SR
#Universidad del Valle de Guatemala
#Raúl Monzon 17014
# -*- coding: utf-8 -*-

import struct
from math import *
from Funciones import ClaseBMP
from Funciones import OBJCTF
from Funciones import Texture
from MTX import MTX


"""
Clase con función del rendering
Toma la clase BMP para el bitmap
"""
class SR(object):
    #Inicializa el rendering
    def glInit(self):
        self.drawing =ClaseBMP(0,0)
        self.Portsize=(0,0)
        self.PortStart=(0,0)
        self.name="dibujo.bmp"
        #Colocamos el color blanco como default
        self.color=self.drawing.color(255,255,255)
        self.obj=None
        self.text=None
    """
    Crea imagen 
    """
    def glFinish(self):
        self.drawing.write(self.name)
    """
    Define el tamaño donde estara dentro la imagen
    parametros:
    width: ancho del cuadro
    height alto del cuadro
    """
    def glCreateWindow(self,width,height):
        self.drawing=ClaseBMP(width,height)
        self.Portsize=(width,height)

    """
    Cambia el color predeterminado
    parametros:
    valores rgb
    """
    def glColor(self,r,g,b):
        self.color=self.drawing.color(int(r*255),int(g*255),int(b*255))
        return self.color

    """
    Define el tamaño de la imagen
    parametros:
    x: donde empezara el eje x (este valor se guarda en el portstart)
    y: donde empezara el eje y (este valor se guarda en el portstart)
    width: ancho del cuadro
    height: altura del cuadro
    """
    def glViewPort(self,x,y,width,height):
        self.PortStart=(x,y)
        self.Portsize=(width,height)

    """
    Colorea todo de un solo color
    """
    def glClear(self):
        self.drawing.clear()

    """
    Cambia el color predeterminado para glClear
    """
    def glClearColor(self,r,g,b):
        self.drawing.clear(r,g,b)

    """
    Cambia de color un pixel
    parametros:
    x: coordenada en el eje x donde se encuentra el punto
    y: coordenada en el eje y donde se encuentra el punto
    """
    def glVertex(self,x,y):
        coorx=int(self.Portsize[0]*(x+1)*(1/2)*self.PortStart[0])
        coory=int(self.Portsize[1]*(y+1)*(1/2)*self.PortStart[1])
        self.drawing.point(coorx,coory,self.color)
    
    """
    Cambia de color un pixel
    parametros:
    x: coordenada en el eje x donde se encuentra el punto
    y: coordenada en el eje y donde se encuentra el punto
    """
    def glVertexPro(self,x,y):
        coorx=int(self.Portsize[0]*(x+1)*(1/2)*self.PortStart[0])
        coory=int(self.Portsize[1]*(y+1)*(1/2)*self.PortStart[1])
        self.drawing.point(coorx,coory,self.color)
        self.drawing.point(coorx,coory+1,self.color)
        self.drawing.point(coorx+1,coory,self.color)
        self.drawing.point(coorx+1,coory+1,self.color)
                    
    
    """
    Encuentra la coordenada x y y respectivamente
    
    def calculateCoordxVert(x):
        a=int(self.Portsize[0]*(x+1)*(1/2)*self.PortStart[0])
        return a
    def calculateCoordyVert(y):
        return int(self.Portsize[1]*(y+1)*(1/2)*self.PortStart[1])
    """
    def norm(self,v0):
        v=self.length(v0)
        if not v:
            return [0,0,0]
        return[v0[0]/v, v0[1]/v, v0[2]/v]

    """
    Calcular coordenadas baricentricas
    """
    def bar(self,a,b,c,x,y):
        vertice1=(c[0]-a[0], b[0]-a[0],a[0]-x)
        vertice2=(c[1]-a[1], b[1]-a[1],a[1]-y)
        bari=self.calculateCross(vertice1,vertice2)
        if abs(bari[2])<1:
            return -1,-1,-1
        return ( 1 - (bari[0] + bari[1]) / bari[2], bari[1] / bari[2], bari[0] / bari[2])

    """
    Dibujar triangulos
    parametros:
    puntos ABC del triangulo
    color
    textura
    coordenadas de la textura
    intensiadd
    shader
    color base
    """
    def triangulo(self,a,b,c,color=None, texture=None,  txtcoor=(),intensity=1, normals=None, shader=None,baseColor=(1,1,1)):
        limitadormin,limitadormax=self.limitB(a,b,c)
        for x in range(limitadormin[0],limitadormax[0]+1):
            for y in range(limitadormin[1], limitadormax[1] + 1):
                m,n,o=self.bar(a,b,c,x,y)
                if m <0 or n<0 or o<0:
                    continue
                if texture:
                    Texturea=txtcoor
                    Textureb=txtcoor
                    Texturec=txtcoor
                    tx=Texturea[0] * m + Textureb[0] * n + Texturec[0] * o
                    ty=Texturea[1] * m + Textureb[1] * n + Texturec[1] * o
                    color=self.text.getColor(tx,ty,intensity)
                elif shader:
                    color = shader(self,bar(b,n,o),Vnormals=normals, baseColor=baseColor)
                q=a[2]*m+b[2]*n+c[2]*o
                if x<0 or y<0:
                    continue
                if q>self.drawing.getZBValue(x,y):
                	self.drawing.point(x,y,color)
                	self.drawing.setZBValue(x,y,q)
                    
    """
    Definir un cuadro delimitador
    """
    def limitB(self,*listV):
        xs= [vertex[0] for vertex in listV] 
        ys= [vertex[1] for vertex in listV]
        xs.sort()
        ys.sort()
        return (xs[0],ys[0]),(xs[-1],ys[-1])

    """
    Calcular producto punto
    parametros:
    V0:primer vector
    v1:segundo vector
    """
    def calculateDot(self,v0,v1):
        return v0[0]*v1[0] + v0[1] * v1[1] + v0[2] * v1[2]

    """
    Calcular producto cruz
    parametros:
    V0:primer vector
    v1:segundo vector
    """
    def calculateCross(self,v0,v1):
        return [v0[1] * v1[2] - v0[2] * v1[1], v0[2] * v1[0] - v0[0] * v1[2], v0[0] * v1[1] - v0[1] * v1[0]]

    def length(self,v0):
        return (v0[0]**2 + v0[1]**2 + v0[2]**2)**0.5
    def sub(self,v0,v1):
        return [v0[0] - v1[0], v0[1] - v1[1], v0[2] - v1[2]]
    

    """
    Calcular vector PQ
    parametros:
    P:primer vector
    Q:segundo vector
    """
    def calculatePQ(self,p,q):
        return [q[0]-p[0],q[1]-p[1],q[2]-p[2]]
    """
    Cargar obj
    """
    def loadOBJ(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), fill=True, textured=None, rotate=(0, 0, 0), shader=None):
        self.obj= OBJCTF(filename)
        self.obj.load()
        self.modelm(translate,scale,rotate)
        light=(0,0,1)
        faces=self.obj.getFacesL()
        vertex=self.obj.getVertexL()
        vn=self.obj.getVertexNormalL()
        materials=self.obj.getMaterials()
        mtlFaces=self.obj.getMaterialF()
        tVertex=self.obj.getTVertex()
        self.text=Texture(textured)
        if materials:
            for mats in mtlFaces:
                inicio,final=mats[0]
                color=materials[mats[1]].difuseColor
                for index in range (inicio,final):
                    face =faces[index]
                    cont=len(face)
                    if cont==3:
                        c1=face[0][0]-1
                        c2=face[1][0]-1
                        c3=face[2][0]-1
                        a=self.trans(vertex[c1])
                        b=self.trans(vertex[c2])
                        c=self.trans(vertex[c3])
                        if shader:
                            sa=vn[f1]
                            sb=vn[f1]
                            sc=vn[f1]
                            self.triangulo(a, b, c, baseColor=color, shader=shader,normals=(sa, sb, sc))
                        else:
                            normal=self.norm(self.calculateCross(self.sub(b,a),self.sub(c,a)))
                            intensity=self.calculateDot(normal,light)
                            if not(self.text.textured()):
                                if intensity<0:
                                    continue
                                self.triangulo(a,b,c,color=self.glColor(color[0]*intensity, color[1]*intensity, color[2]*intensity))
        else:
            print("No se encontraron materiales para "+filename)
            for face in faces:
                cont=len(face)
                if cont==3:
                    c1=face[0][0]-1
                    c2=face[1][0]-1
                    c3=face[2][0]-1
                    a=self.trans(vertex[c1])
                    b=self.trans(vertex[c2])
                    c=self.trans(vertex[c3])
                    if shader:
                        sa=vn[f1]
                        sb=vn[f2]
                        sc=vn[f3]
                        self.triangulo(a, b, c, baseColor=color, shader=shader,normals=(sa, sb, sc))
                    else:
                        nl=self.norm(self.calculateCross(self.sub(b,a), self.sub(c,a)))
                        intensity=self.calculateDot(nl,light)

                        if not self.text.textured():
                            if intensity>0:
                                continue
                            self.triangulo(a, b, c,color=self.glColor(intensity, intensity, intensity))
                        else:
                            if self.text.textured():
                                txt1 = face[0][-1]-1
                                txt2 = face[1][-1]-1
                                txt3 = face[2][-1]-1
                                txta = tVertex[txt1]
                                txtb = tVertex[txt2]
                                txtc = tVertex[txt3]
                                self.triangulo(a, b, c, texture=self.text.isTextured(), texture_coords=(ta,tb,tc), intensity=intensity)
                else:
                    txt1 = face[0][-1]-1
                    txt2 = face[1][-1]-1
                    txt3 = face[2][-1]-1
                    txt4 = face[3][-1]-1
                    listV=[self.trans(vertex[f1]),self.trans(vertex[f2]),self.trans(vertex[f3]),self.trans(vertex[f4])]
                    nl=self.norm(self.calculateCross(self.sub(listV[0], listV[1]), self.sub(listV[1], listV[2])))
                    intensity=self.calculateDot(nl,light)
                    a=listv
                    b=listv
                    c=listv
                    d=listv
                    if not textured:
                        if intensity<0:
                            continue
                        self.triangulo(a,b,c,color=self.glColor(intensity, intensity, intensity))
                        self.triangulo(a,b,d,color=self.glColor(intensity, intensity, intensity))
                    if textured:
                        if self.text.textured():
                            t1=face[0][-1]-1
                            t2=face[1][-1]-1
                            t3=face[2][-1]-1
                            t4=face[3][-1]-1
                            ta=tVertex[t1]
                            tb=tVertex[t2]
                            tc=tVertex[t3]
                            td=tVertex[t4]
                            self.triangulo(a,b,c,texture=self.text.isTextured(), texture_coords=(ta, tb, tc), intensity=intensity)
                            self.triangulo(a,b,d,texture=self.text.isTextured(), texture_coords=(ta, tb, td), intensity=intensity)

    def modelm(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        translation_MTX = MTX([[1, 0, 0, translate[0]],[0, 1, 0, translate[1]],[0, 0, 1, translate[2]],[0, 0, 0, 1],])
        a = rotate[0]
        rotation_MTX_x = MTX([[1, 0, 0, 0],[0, cos(a), -sin(a), 0],[0, sin(a),  cos(a), 0],[0, 0, 0, 1]])
        a = rotate[1]
        rotation_MTX_y = MTX([[cos(a), 0,  sin(a), 0],[     0, 1,       0, 0],[-sin(a), 0,  cos(a), 0],[     0, 0,       0, 1]])
        a = rotate[2]
        rotation_MTX_z = MTX([[cos(a), -sin(a), 0, 0],[sin(a),  cos(a), 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
        rotation_MTX = rotation_MTX_x * rotation_MTX_y * rotation_MTX_z
        scale_MTX = MTX([[scale[0], 0, 0, 0],[0, scale[1], 0, 0],[0, 0, scale[2], 0],[0, 0, 0, 1],])
        self.Model = translation_MTX * rotation_MTX * scale_MTX

    def viewm(self, x, y, z, center):
        m = MTX([[x[0], x[1], x[2],  0],[y[0], y[1], y[2], 0],[z[0], z[1], z[2], 0],[0,0,0,1]])
        o = MTX([[1, 0, 0, -center[0]],[0, 1, 0, -center[1]],[0, 0, 1, -center[2]],[0, 0, 0, 1]])
        self.View = m * o

    def projectionm(self, coeff):
       	self.Projection = MTX([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, coeff, 1]])

    def viewportm(self, x=0, y =0):
       	self.Viewport =  MTX([[self.drawing.width/2, 0, 0, x + self.drawing.width/2],[0, self.drawing.height/2, 0, y + self.drawing.height/2],[0, 0, 128, 128],[0, 0, 0, 1]])
        
    def aim(self, eye, center, up):
       	z = self.norm(self.sub(eye, center))
       	x = self.norm(self.calculateCross(up, z))
       	y = self.norm(self.calculateCross(z,x))
       	self.viewm(x, y, z, center)
       	self.projectionm(-1/self.length(self.sub(eye, center)))
       	self.viewportm()

    def trans(self, vertex):
       	agv = MTX([[vertex[0]],[vertex[1]],[vertex[2]],[1]])
       	transformed_vertex = self.Viewport * self.Projection * self.View * self.Model * agv
       	transformed_vertex = transformed_vertex.getData()
       	tra = [round(transformed_vertex[0][0]/transformed_vertex[3][0]), round(transformed_vertex[1][0]/transformed_vertex[3][0]), round(transformed_vertex[2][0]/transformed_vertex[3][0])]
       	return tra

    """
    TERMINA USO DE MATRICES
    """

    """
    Sets
    """
    def setfname(self,filename):
        self.name=filename
        
        
        
        
    


    


    
            
    
    
                
        
