from SR import SR
import random

image = SR()
image.glInit()
image.glCreateWindow(1500, 1500)
image.aim((-1,3,5), (0,0,0), (0,1,0))
image.glViewPort(0,0,1500,1500)
image.setfname("proyecto.bmp")

def mt(x, y):
	image.loadOBJ("mt.obj", translate=(x,y,-0.30), scale=(0.08,0.08,0.08), rotate=(0.40,0.25,-0.1), fill=True)

for x in range(random.randint(300, 500)):
	x = random.uniform(-1,1)
	y = random.uniform(-1,1)
	image.glVertexPro(x,y)

for x in range(random.randint(1,5)):
	mt(random.uniform(0,1), random.uniform(0,1))
"""
image.loadOBJ("./models/tr.obj", translate=(0.25,-0.75,0.3), scale=(0.08,0.08,0.08), rotate=(0.25,0.8,-0.25), fill=True)
image.loadOBJ("./models/ast.obj", translate=(0.80,-1,0), scale=(0.05,0.05,0.05), rotate=(-1,0.5,0), fill=True)
image.loadOBJ("./models/ss.obj", translate=(-0.30,-0.20,-0.25), scale=(0.16,0.16,0.16), rotate=(-1.50,-0.80,1), fill=True)
image.loadOBJ("./models/planetN.obj", translate=(0.50,0.75,0), scale=(0.12,0.12,0.12),fill=True)#shader=gourad)
#image.loadOBJ("./models/planetN.obj", translate=(0,0,0), scale=(0.3,0.3,0.3), rotate=(1,1,1),shader=shader2)
"""

image.glFinish()
