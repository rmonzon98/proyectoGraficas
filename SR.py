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
        self.color=self.drawing.color(r,g,b)

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
    Renderizar la rejilla de la textura
    """
    def glTexturedGrid(self,filename=None,newfile=True,translate=(0, 0), scale=(1, 1)):
        if self.obj:
            tvertex=self.obj.getTVertex()
            materials=self.obj.geMaterials()
            faces=self.obj.getFacesL()
            if (filename and newfile):
                square=SR()
                square.glInit()
                square.glCreateWindow(self.drawing.width,self.drawing.height)
                square.glViewPort(self.PortStart[0],self.PortStart[1], self.Portsize[0], self.Portsize[1])
                square.setfname(filename)
            else:
                square =self
            if materials:
                indice=self.obj.getMaterialF()
                for mat in indice:
                    dc=materials[mat[1]].difuseColor
                    for j in range(mat[0][0], mat[0][1]):
                        textc=[]
                        for face in faces[j]:
                            if len(face)>2:
                                txt=((tvertex[face[2]-1][0]+ translate[0]) * scale[0], (tvertex[face[2]-1][1]+ translate[1]) * scale[1], 0)
                                textc.append(txt)
                            if len(textc)>2:
                                square.glPolygon(textCoo)
            else:
                for face in faces:
                    textc=[]
                    for c in face:
                        if len(c)>2:
                            txt=((tvertex[c[2]-1][0]+ translate[0]) * scale[0], (tvertex[c[2]-1][1]+ translate[1]) * scale[1],0)
                            textc.append(txt)
                        if len(textc)>2:
                            square.glPolygon(textc)
            return square
                    
    
    """
    Encuentra la coordenada x y y respectivamente
    
    def calculateCoordxVert(x):
        a=int(self.Portsize[0]*(x+1)*(1/2)*self.PortStart[0])
        return a
    def calculateCoordyVert(y):
        return int(self.Portsize[1]*(y+1)*(1/2)*self.PortStart[1])
    """
    """
    Dibuja una linea
    Parametros:
    x0: punto x inicial
    y0: punto y inicial
    x1: punto x final
    y1: punto y final
    """
    def glLine(self,x0,y0,x1,y1):
        a=self.PortStart[0]
        b=self.PortStart[1]
        a1=self.Portsize[0]*(1/2)
        b1=self.Portsize[1]*(1/2)
        px1=int(a1*(x0+1)+a)
        py1=int(b1*(y0+1)+b)
        px2=int(a1*(x1+1)+a)
        py2=int(a1*(y1+1)+b)
        dy=abs(y2-y1)
        dx=abs(x2-x1)
        if (dy>dx):
            px1,py1=py1,px1
            px2,py2=py2,px2
        else:
            px1,px2=px2,px1
            py1,py2=py2,py1
        dy=abs(y2-y1)
        dx=abs(x2-x1)
        temp=0
        temp2=dx
        y=py1
        for x in range(px1,px2+1):
            if (dy>dx):
                self.drawing.point(y,x,self.color)
            else:
                self.drawing.point(x,y,self.color)
            temp += dy*2
            if temp >= temp2:
                y +=1 if py1<py2 else -1
                temp2 += 2 * dx
    """
    Normalizar coordenadas en x y y respectivamente
    """
    def glnormalX(self,x):
        return ((2*x)/self.Portsize[0]) - self.PortStart[0] - 1
    def glnormalY(self,y):
        return ((2*y)/self.Portsize[1]) - self.PortStart[1] - 1

    def norInvX(self,x):
        return int(self.viewPortsize[0] * (x+1) * (1/2) + self.viewPortStart[0])
    def norInvY(self,y):
        return int(self.viewPortsize[0] * (y+1) * (1/2) + self.viewPortStart[0])

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
        return ( 1 - (bar[0] + bar[1]) / bar[2], bar[1] / bar[2], bar[0] / bar[2])

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
                if z>self.drawing.getZBValue(x,y):
                    self.drawing.point(x,y,color)
                    self.drawing.setZBValue(x,y,z)
                    
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
    Dibujar poligono
    Recibe lista de vertices
    """
    def glPolygon(self,listV):
        for i in range(len(listV)):
            if i==len(listV)-1:
                st=listV[i]
                fi=listV[i+1]
            else:
                st=listV[i]
                fi=listV[0]
            self.glLine(fi[0],fi[1],st[0],st[1])
            
    """
    Verifica si un punto esta dentro del poligono dibujado,
    basado en el algoritmo encontrado en http://www.eecs.umich.edu/courses/eecs380/HANDOUTS/PROJ2/InsidePoly.html
    solucion 1 (2D)
    """
    def glPointInside(self,listV,x,y):
        contador=0
        point1=listV[0]
        n=len(listV)
        for i in range(n+1):
            point2= listV[i%n]
            if(y>min(point1[1],point2[1])):
               if (y<=max(point1[1],point2[1])):
                   if(point1[1] != point2[1]):
                       pointxint = (y-point1[1])*(point2[0]-point1[0])/(point2[1]-point1[1])+point1[0]
                       if(point1[0] == point2[0] or x <= pointxint):
                           contador+=1
        if(contador%2==0):
            return False
        else:
            return True
        
    """
    Rellenar poligono
    parametros:
    listV:lista de vertices
    color
    texture
    intensity
    txtcoor=coordenadas de la textura
    """
    def glFill(self, listV, color=None, texture=None, intensity=1, txtcoor = (), zVal=True):
        intensidad=intensity
        if not texture:
            if color==None:
                color=self.color
            else:
                color=self.drawing.color(int(color[0]),int(color[1]),int(color[2]))
        else:
            if self.text==None:
                text=Texture(texture)
                self.text=text
            else:
                text=self.text
        startX = sorted(listV, key=lambda tup: tup[0])[0][0]
        finishX = sorted(listV, key=lambda tup: tup[0], reverse = True)[0][0]
        startY = sorted(listV, key=lambda tup: tup[1])[0][1]
        finishY = sorted(listV, key=lambda tup: tup[1], reverse=True)[0][1]
        startX = int(self.Portsize[0] * (startX+1) * (1/2) + self.PortStart[0])
        finishX = int(self.Portsize[0] * (finishX+1) * (1/2) + self.PortStart[0])
        startY = int(self.Portsize[0] * (startY+1) * (1/2) + self.PortStart[0])
        finishY = int(self.Portsize[0] * (finishY+1) * (1/2) + self.PortStart[0])
        for x in range(startX,finishX+1):
            for y in range(startX,finishX+1):
                dentro=self.glPointInside(listV,self.glnormalX(x), self.glnormalY(y))
                if dentro:
                    if texture:
                        r=self.norInvX(listV[0][0]),self.norInvX(listV[0][1])
                        a=self.norInvX(listV[1][0]),self.norInvX(listV[1][1])
                        u=self.norInvX(listV[2][0]),self.norInvX(listV[2][1])
                        l,m,o=self.bar(r,a,u,x,y)
                        r=txtcoor[0]
                        a=txtcoor[1]
                        u=txtcoor[2]
                        tx=r[0]*l+a[0]*m+u[0]*o
                        ty=r[1]*l+a[1]*m+u[1]*o
                    z=self.glPLaneZ(listV, x, y)
                    if z>self.drawing.getZBValue(x,y):
                        self.drawing.point(x,y,color)
                        self.drawing.setZBValue(x,y,z)

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
    coordenada z en el punto (x,y,z)
    """
    def glPlaneZ(self,vertecList,x,y):
        pq=self.calculatePQ(vertexList[0],vertexList[1])
        prs=self.calculatePQ(vertexList[0],vertexList[2])
        normal=self.calculateCross(pq,pr)
        if normal[2]:
            return ((normal[0]*(x-vertexList[0][0])) + (normal[1]*(y-vertexList[0][1])) - (normal[2]*vertexList[0][2]))/(-normal[2])
        else:
            return -float("inf")

    """
    """
    def glRenderZBuffer(self,namef=None):
        if namef==None:
            namef=self.namef.split(".")[0]+"ZBuffer.bmp"
        self.drawing.write(namef,zbuffer=True)

    """
    Cargar obj
    """
    def loadOBJ(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), fill=True, textured=None, rotate=(0, 0, 0), shader=None):
        self.obj= OBJCTF(filename)
        self.obj.load()
        self.model(translate,scale,rotate)
        light=self.norm((0,0,1))
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
                for index in range (start,stop):
                    face =faces[index]
                    cont=len(face)
                    if con==3:
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
                                self.triangulo(a,b,c,color=color.self.glColor(color[0]*intensity, color[1]*intensity, color[2]*intensity))
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

    """
    USO DE LAS MATRICES
    Multiplicacion de matrices
    parametros:
    m1,m2: matrices
    """
    def matMul(self,m1,m2):
        if len(m1[0])==len(m2):
            result=[]
            rows1=len(m1)
            rows2=len(m2)
            col1=len(m1[0])
            col2=len(m2[0])
            for i in range(rows1):
                resultado.append([0]*col2)
            for i in range(rows1):
                for j in range(col2):
                    for k in range(col1):
                        resutlado[i][j]=m1[i][k]*m2[k][j]
            return resultado
        else:
            print ("Error al multiplicar matrices")
            return 0

    """
    generar proyeccion
    """
    def projMTX(self,c):
        self.Projection=MTX([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, c, 1]])
        
    """
    generar vista
    """
    def viewMTX4(self,x,y,z,center):
        n=MTX([[x[0], x[1], x[2],  0],[y[0], y[1], y[2], 0],[z[0], z[1], z[2], 0],[0,0,0,1]])
        m=MTX([[1, 0, 0, -center[0]],[0, 1, 0, -center[1]],[0, 0, 1, -center[2]],[0, 0, 0, 1]])
        self.View=n*m
    
    """
    generar viewport Matrix
    """
    def viewMTX(self,x=0,y=0):
        self.Viewport =MTX([[self.drawing.width/2, 0, 0, x + self.drawing.width/2],[0, self.drawing.height/2, 0, y + self.drawing.height/2],[0, 0, 128, 128],[0, 0, 0, 1]])
    """
    generar modelo
    """
    def model(self,translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        transMTX=MTX([[1, 0, 0, translate[0]],[0, 1, 0, translate[1]],[0, 0, 1, translate[2]],[0, 0, 0, 1],])
        a=rotate[0]
        rotMTXAxisX=MTX([[1,0,0,0],[0, cos(a), -sin(a), 0],[0, sin(a),cos(a),0],[0, 0, 0, 1]])
        a=rotate[1]
        rotMTXAxisy=MTX([[cos(a),0, sin(a),0],[0, 1,0, 0],[-sin(a), 0,  cos(a), 0],[0,0,0,1]])
        a=rotate[2]
        rotMTXAxisz=MTX([[cos(a), -sin(a), 0, 0],[sin(a),  cos(a), 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
        result=  rotMTXAxisz* rotMTXAxisy* rotMTXAxisX
        scaleMTX=MTX([[scale[0], 0, 0, 0],[0, scale[1], 0, 0],[0, 0, scale[2], 0],[0, 0, 0, 1],])
        self.Model=result*transMTX*scaleMTX        
        
    """
    transformar matriz
    """
    def trans(self,v):
        a=MTX([[v[0]],[v[1]],[v[2]],[1]])
        vTrans=self.Viewport * self.Projection * self.View * self.Model * a
        vTrans=vTrans.getData()
        transform=[round(vTrans[0][0]/vTrans[3][0]), round(vTrans[1][0]/vTrans[3][0]), round(vTrans[2][0]/vTrans[3][0])]
        return transform

    """
    Ver en una parte en especifica de la matriz
    """
    def aim(self,eye,up,cent):
        z=self.norm(self.sub(eye,cent))
        x=self.norm(self.calculateCross(up,z))
        y=self.norm(self.calculateCross(z,x))
        self.projMTX(-1/self.length(self.sub(eye, cent)))
        self.viewMTX4(x, y, z, cent)
        self.viewMTX()

    """
    TERMINA USO DE MATRICES
    """

    """
    Sets
    """
    def setfname(self,filename):
        self.name=filename
        
        
        
        
    


    


    
            
    
    
                
        
