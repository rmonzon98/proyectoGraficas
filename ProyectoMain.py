from SR import SR
import random

image = SR()
image.glInit()
image.glCreateWindow(800, 800)
image.aim((-1,3,5), (0,0,0), (0,1,0))
image.glViewPort(0,0,800,800)
image.setfname("proyecto.bmp")


#image.loadOBJ("char.obj", translate=(0.80,-1,0), scale=(0.4,0.4,0.4), rotate=(-1,0.5,0), fill=True)
#image.loadOBJ("Rock_1.obj", translate=(0,0,0), scale=(0.01,0.01,0.01), rotate=(0,0,0), fill=True)

image.loadOBJ("GoldFish.obj", translate=(-0.5,-0.5,0), scale=(0.05,0.05,0.05), rotate=(0,1,-0.25), fill=True)
image.loadOBJ("jelly.obj", translate=(-0.5,0.25,0), scale=(0.1,0.1,0.1), rotate=(0,0,0), fill=True)
image.loadOBJ("horse.obj", translate=(0.15,-0.90,0), scale=(0.15,0.15,0.15), rotate=(0,0,0), fill=True)
image.loadOBJ("shark.obj", translate=(0.25,-0.4,0), scale=(0.2,0.2,0.2), rotate=(0,0.5,0), fill=True)
image.loadOBJ("can.obj", translate=(0.5,0.5,0), scale=(0.1,0.1,0.1), rotate=(-0.1,0,0.4), fill=True)




image.glFinish()
