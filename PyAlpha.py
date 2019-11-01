import copy
import math
import random
import pandas
import numpy
class Vector ():
    def __init__ (self,x,y):
        self.x = x
        self.y = y
    def __add__ (self,other):
        self.x += other.x
        self.y+= other.y
        return self
def rand (a,b):
    return int(random.random()*(b-a)+a)
def dist (a,b,distance = True,c =None):
    dists = Vector (abs(a.x-b.x),abs(a.y-b.y))
    if not (distance) and c == None:
        return dists
    else:
        dist = math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)
        if distance and c == None:
            return dist
        elif c != None:
            if dist>c:
                return False
            else :
                return True
def vectorfinder (start,point):
    v = dist (start,point,False)
    if point.x < start.x:
        v.x*= -1
    if point.y < start.y :
        v.y*= -1
    return v
def pathfinder (start,point,step):
    if step == 0:
        return Vector(0,0)
    v = vectorfinder (start,point)
    d = dist (start,point,False)
    if d.x < step and d.y < step:
        return v
    if d.x >= d.y:
        t = d.x/step
        if v.x < 0:
            step *= -1
        return Vector(step,v.y/t)
    else :
        t = d.y/step
        if v.y < 0:
            step *= -1
        return Vector (v.x/t,step)
def closest (me,where,typ = tuple()):
    target = None
    for l in where:
        for en in l:
            if not str (en) in typ and len (typ) !=0 :
                continue
            if target == None:
                target = en
            else :
                if dist (me,en,True,dist(me,target)):
                    target = en
    return target
def notn (a):
    if a != None:
        return True
    return False

def spread (p,s):
    return rand (p-s,p+s)
def ty (en,typ):
    if typ == None:
        return True
    return str(en) == typ
def prob (n):
    if rand(0,n) == 1:
        return True
    return False

def closes (me,where,dis,typ = tuple (),exc = tuple ()):
    for w in where:
        for en in w:
            if dist (me,en.center,True,dis) and (str(en) in typ or len (typ) == 0) and not str (en) in exc:
                yield en

def dictopd (dictionary):
    df = pd.DataFrame()
    for en in dictionary.keys():
        df[en] = dictionary[en]
    return df














class MM ():
    def __init__(self,M,act = 0):
        self.timer = act
        self.max = M
    def full (self):
        return self.timer >= self.max
    def add (self,n=1):
        for _ in range (n):
            self.inc()
    def inc (self):
        if self.timer < self.max:
            self.timer +=1



