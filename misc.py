# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:35:25 2022

Steven Shockley

"""

import itertools

import numpy as np

import matplotlib.pyplot as plt

class particle:
    index = itertools.count().__next__
    
    def __init__(self,mass,pos,vel,acc):
        self.mass = mass
        self.position = np.array(pos)
        self.velocity = np.array(vel)
        self.acceleration = np.array(acc)
        self.id = particle.index()
        
        self.artist = None
        
        ### Color
        prim = np.random.randint(1,4)
        primVal = -1.
        while primVal > 1.0 or primVal < 0.0:
            primVal = np.random.normal(loc=0.8,scale=0.1)
        
        val2 = -1.
        while val2 > 1.0 or val2 < 0.0:
            val2 = np.random.normal(loc=0.5,scale=0.4)
            
        val3 = -1.
        while val3 > 1.0 or val3 < 0.0:
            val3 = np.random.normal(loc=0.5,scale=0.4)
        
        c = [0,0,0]
        for i in range(3):
            if i == prim:
                c[i] = primVal
            elif not val2 in c:
                c[i] = val2
            else:
                c[i] = val3
        
        self.color = tuple(c)
        return
    
    def update(self,dt):
        self.position = self.position + self.velocity*dt
        self.velocity = self.velocity + self.acceleration*dt
        return
        
    def draw(self):
        if self.artist != None:
            self.artist.remove()
        
        self.artist, = plt.plot(self.position[0],self.position[1],'o',color=self.color)
        
        plt.xlim(-100,100)
        plt.ylim(-100,100)
        return
        
    def updateAcc(self,pts):
        Force = np.array([0.,0.])
        for pt in pts:
            if pt.id != self.id:
                Force += calcForce(self.mass,pt.mass,self.position,pt.position)
            else:
                continue
        self.acceleration = Force/self.mass
        return

def figInit():
    fig = plt.figure("N Body")
    
    fig.clf()
    
    plt.xlim(-100,100)
    plt.ylim(-100,100)
    return
figInit()

def calcForce(m,M,posm,posM):
    #G = 6.67e-11
    G = 100
    
    vec = posM - posm 
    R = np.linalg.norm(vec)
    angle = np.arctan2(vec[1],vec[0])
    
    Force = G*m*M/R**2
    return Force*np.cos(angle),Force*np.sin(angle)

N = 2
dt = 0.1
pts = []
for i in range(N):
    pts.append(particle(100,200*np.random.random((2,)) - 100,[0.,0.],[0.,0.]))

for i in range(100):
    for pt in pts:
        pt.draw()
        pt.updateAcc(pts)
        pt.update(dt)
    plt.pause(dt)
    
    plt.show()