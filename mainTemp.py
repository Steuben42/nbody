# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 23:16:15 2022

Steven Shockley
"""

import numpy as np
import matplotlib.pyplot as plt

import nbody 
import nbodyUtils as util

N = 100
dt = 0.1
pts = []

fig = plt.figure("N Body")
fig.clf()
ax = fig.gca()

ax.set_xlim(-100.,100.)
ax.set_ylim(-100.,100.)

#for i in range(N):
    #pts.append(nbody.particle(10e13,200*np.random.random((2,)) - 100,np.array([0.,0.]),np.array([0.,0.])))
    
masses = [10e12,10e5,10e5]
r = [0.,56.318,22.527]
v = [0.,1.088,1.721]
energies = [np.zeros(10000),np.zeros(10000),np.zeros(10000)]

for i in range(3):
    pts.append(nbody.particle(masses[i],np.array([r[i]+1,1.]),np.array([0.,v[i]]),np.array([0.,0.])))
    
n = nbody.node(0,1,((-200,200),(-200,200)),pts)
n.populate(pts)

util.initCSV()

for i in range(10000):
    for pt in pts:
        pt.mplRender(ax)
        pt.updateForceBH(pts,n)
        pt.updateState(dt)
        energies[pt.id][i] += util.particleEnergy(pt, pts)
        if pt.id == 1:
            util.CSVentry(i,pt,detailLevel=2)
        
    #if i > 63:
        #breakpoint()
        
    plt.pause(0.1)
    n.refresh(pts)
    
    plt.show()