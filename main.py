import pygame
import math
import copy
from random import random
import json
from PyAlpha import *
import numpy as np
from matplotlib import pyplot as plt
import time
from sklearn.preprocessing import MinMaxScaler
ai = bool(int(input("mode: ")))
if ai:
    from tensorflow import keras
mindist = 550
ep = 700
show = True
fast = False
envoirment = []
values = []
players = []
deleter = set()
preductions = []
with open ("saves.txt","r") as f:
    data = json.loads(f.read())
if False:
    model = keras.Sequential([keras.layers.Dense(units= 1,input_shape = [1])])
    model.compile (optimizer = "adam",loss = "mean_squared_error", metrics = ["accuracy"])
    xs = np.array(data["dis"],dtype = float)
    ys = np.array(data["jumped"],dtype = int)
    model.fit(xs,ys,epochs = ep)
def rectangle (item,w,h,color,shift = True,out = False):
    if shift:
        item = rel(item)
    item.x = round(item.x)
    item.y = round(item.y)
    pygame.draw.rect(win,color,(item.x,item.y,w,h),out)
def circle (item,r,color,shift=True,out = False):
    if shift:
        item = rel(item)
    item.x = round(item.x)
    item.y = round(item.y)
    pygame.draw.circle(win,color,(item.x,item.y),r,out) 
def rel (p,inv = False):
    global player
    if not inv:
        return Vector( p.x- (player.x - dis[0]//2), p.y- (player.y - dis[1]//2))
    return Vector( p.x+ (player.x - dis[0]//2), p.y+ (player.y - dis[1]//2))
def line (start,point,color,r = True):
    if r :
        start = rel (start)
        point =  rel (point)
    pygame.draw.aaline(win,color,(start.x,start.y),(point.x,point.y)) 
def Scaler (a):
    scaler = MinMaxScaler (feature_range = (0,1))
    return scaler.fit_transform(a)
class Player ():
    def __init__ (self,coll = True):
        global data
        self.x = -500
        self.collisions = coll
        self.y = 0
        self.vy = 0
        self.jumping = False
        self.dis = data["dis"]
        self.jumped = data["jumped"]
        self.oh = data["oh"]
        self.ow = data["ow"]
    def update (self):
        global ai
        for _ in range (8):
            self.x+=2
            self.checkcollisions ()
        if not ai:
            self.draw()
        self.vy+= 5
        self.y+= self.vy
        if self.y>0:
            self.y = 0
            self.vy = 0
            self.jumping = False
    def jump (self):
        if not self.jumping:
            self.jumping = True
            self.vy-=39
        clos = None
        for en in envoirment:
            if en.x< player.x:
                continue
            if clos == None:
                clos = en
            else :
                if clos.x>en.x:
                    clos = en
        if clos!=None:
            player.dis.append (clos.x-player.x)
            player.jumped.append(int(player.jumping))
            player.oh.append(clos.h)
            player.ow.append(clos.w)

    def draw(self):
        rectangle(Vector(self.x -10,self.y-20),20,20,(100,100,100))
    def checkcollisions(self):
        global run
        if self.collisions:
            points = [self,Vector(self.x+20,self.y),Vector(self.x,self.y+20),Vector(self.x+20,self.y+2)]
            for en in envoirment:
                for point in points :
                    if point.x > en.x and point.x < en.x+en.w and point.y > en.y and point.y < en.y + en.h:
                        run = False
                        print ("You Lost")
                        break
class Gamer ():
    def __init__(self,name,posx,posy,coll,color,model,trained = None,red = False):
        self.name = name
        self.collisions = coll
        self.x = posx
        self.y = posy
        self.red = red
        self._color = color
        self.vy = 0
        self._w = 20
        self.defcolor = color
        self._h = 20
        self.jumping = False
        self.max = None
        self.min = None
        self.values = []
        self.preductions = []
        if trained == None:
            self.model = copy.copy(model)
            with open (self.name + ".txt","r") as f:
                data = json.loads(f.read())
            self.model.compile (optimizer = "rmsprop",loss = "mean_squared_error")
            xs = np.array(data["dis"],dtype = float)
            ys = np.array(data["jumped"],dtype = int)
            xx = np.array(data["oh"],dtype = int)
            xw = np.array(data["ow"],dtype = int)
            #get the numbers to scale
            self.max = [max(xs),max(xx),max(xw)]
            self.min = [min(xs),min(xx),min(xw)]
            merged = np.stack([xs,xx,xw],axis = 1)
            if self.red:
                merged = Scaler(merged)
            print (merged)
            print (self.name)
            self.model.fit(merged,ys,epochs = 50, verbose = 1)
        else :
            if trained == "":
                self.model = keras.models.load_model(self.name+".h5")
            else :
                self.model = trained
            print (self.name+" has been loaded")
    def jump (self):
        self._color = (255,0,0)
        if not self.jumping:
            self.jumping = True
            self.vy-=39
    def draw (self):
        rectangle(Vector(self.x-20,self.y-20),self._w,self._h,self._color)
    def c (self):
        return self._color
    def update (self):
        for _ in range (8):
            self.x+=2
            self.checkcollisions ()
        self.vy+= 5
        self.y+= self.vy
        if self.y>0:
            self.y = 0
            self.vy = 0
            self.jumping = False
        self.behave ()
        self.draw()
        self._color = self.defcolor
    def checkcollisions(self):
        if self.collisions:
            points = [self,Vector(self.x+20,self.y),Vector(self.x,self.y+20),Vector(self.x+20,self.y+20)]
            for en in envoirment:
                for point in points :
                    if point.x > en.x and point.x < en.x+en.w and point.y > en.y and point.y < en.y + en.h:
                        self.death ()
                        break
    def death (self):
        deleter.add (self)
    def behave (self):
        global envoirment
        global say
        global show
        clos = None
        for en in envoirment:
            if en.x< self.x:
                continue
            if clos == None:
                clos = en
            else :
                if clos.x>en.x:
                    clos = en
        if clos!=None:
            if show:
                line (self,clos,(0,0,0))
                line (self,Vector(clos.x,clos.y+clos.h-20),(0,0,0))
            merged = np.stack([[clos.x-self.x],[clos.h],[clos.w]],axis = 1)
            l = copy.copy (merged)
            if self.red:
                merged = np.append([self.max,self.min],merged,axis = 0)
                merged = Scaler(merged)
                merged = np.array([merged[2]])
            prediction = self.model.predict(merged)
            if show:
                say +="\n"+ self.name + "\n"
                say+= str(merged) + "    "
                say+= str(prediction) 
            merged = list(map(float,merged[0]))
            self.values.append(merged)
            self.preductions.append(float(prediction[0][0]))
            if prediction[0][0] >= 0.5:
                self.jump()



class Square ():
    def __init__ (self,x,y,w = 20,h = 40):
        self.x = x
        self.y =y - h
        self.w = w
        self.h = h
    def update (self):
        self.draw()
    def draw (self):
        rectangle(Vector(self.x-20,self.y-20),self.w,self.h,(255,0,0))
def events (keys):
    if keys[ pygame.K_UP] or keys[ pygame.K_SPACE] and not ai:
        player.jump()
    if keys[pygame.K_s]:
        for en in players:
            en.model.save (en.name+".h5")

player = Player(False)
for i in range (100):
    h = rand(40,91)
    if h < 45:
        w = rand (18,43)
    elif h < 59:
        w = rand (18,38)
    else :
        w = rand (18,27)
    envoirment.append(Square(i*mindist + rand(-35,120),20,w,h))


pygame.init()
clock = pygame.time.Clock() 
dis = (1366,768)
win = pygame.display.set_mode(dis)
pygame.display.set_caption("Game")
timer = 0
run = True
back = (255,255,255)
liner = {
    "start":Vector (-1100,0),
    "end":Vector(10**10,0)
}
screen = MM(2)
def modell():
    model = keras.Sequential()
    model.add(keras.layers.Dense(3,input_dim = 3))
    model.add(keras.layers.Dense(5,activation = "relu"))
    model.add(keras.layers.Dense(1,activation = "relu"))
    return copy.copy(model)
if ai:
    bat = 3
    for i in range (bat):
        players.append(Gamer("saves",-520 - i*35,0,True,(0,0,255),copy.copy(modell()),red = True))
    for i in range (0):
        players.append(Gamer("ale",-520-i*49,0,True,(0,255,255),copy.copy(modell()),red = True))
    #players.append(Gamer("bb",-500,0,True,(0,0,0),copy.copy(modell()),""))
    #players.append(Gamer("ale",-200,0,True,(0,255,180),copy.copy(modell()),red = True))
    #players.append(Gamer("ale",-700,0,True,(0,255,180),copy.copy(modell()),red = True))
    #players.append(Gamer("babbo",-6,0,True,(0,255,180),copy.copy(modell()),red = True))
    
    
if ai:
    #input("press")
    pass
while run :
    say = ""
    pygame.display.update()
    win.fill(back)
    line (liner["start"],liner["end"],(0,0,0))
    if not fast:
        clock.tick(25)
    events(pygame.key.get_pressed())
    player.update ()
    for event in pygame.event.get():
        if  event.type == pygame.QUIT:
            run = False
    remover = []
    for i in envoirment:
        if not (i.x > player.x + 4000 or i.x < player.x - 4000 or i.y > player.y + 3000 or i.y < player.y-3000):
            i.update()
        else:
            if i.x<player.x:
                remover.append (i)
    for en in remover:
        envoirment.remove (en)
    screen.inc()
    if screen.full  ():
        screen.timer = 0
        clos = None
        for en in envoirment:
            if en.x< player.x:
                continue
            if clos == None:
                clos = en
            else :
                if clos.x>en.x:
                    clos = en
        if clos!=None and not player.jumping:
            player.dis.append (clos.x-player.x)
            player.jumped.append(int(player.jumping))
            player.oh.append(clos.h)
            player.ow.append(clos.w)
    for en in players:
        en.update()
        if show:
            for tar in players:
                line(en,tar,en.c())
    for en in deleter:
        players.remove(en)
    deleter = set()
    if say and show:
        print (say)
if not ai:
    r = {
    "jumped":player.jumped,
    "dis":player.dis,
    "oh":player.oh,
    "ow":player.ow
    }

    with open ("saves.txt","w") as f:
        json.dump(r,f)

else :
    for en in players:
        with open (en.name + "load.txt","w") as f:
            json.dump({"data":en.values,"jumped":en.preductions},f)

pygame.quit()