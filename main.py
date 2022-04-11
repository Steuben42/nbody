# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 23:16:15 2022

Steven Shockley
"""

import numpy as np
import matplotlib.pyplot as plt

import nbody 

N = 10
dt = 0.1
pts = []

fig = plt.figure("N Body")
fig.clf()
ax = fig.gca()

ax.set_xlim(-100.,100.)
ax.set_ylim(-100.,100.)

for i in range(N):
    pts.append(nbody.particle(10e13,200*np.random.random((2,)) - 100,np.array([0.,0.]),np.array([0.,0.])))

for i in range(100):
    for pt in pts:
        pt.mplRender(ax)
        pt.updateForce(pts)
        pt.updateState(dt)
    plt.pause(0.1)
    
    plt.show()

# testing
n = nbody.node(0,1,((-200,200),(-200,200)),pts)