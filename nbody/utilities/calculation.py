# -*- coding: utf-8 -*-
"""
nbody.utilities.calculation
"""

import numpy as np

### GRAVITATION ###
def barycenter(posV, mV):
    assert(np.size(posV) == np.size(mV))

    mass = 0
    barycenter = np.zeros(np.size(posV[0]))

    for i in range(len(posV)):
        mass += mV[i]
        barycenter += posV[i]*mV[i]
    
    barycenter /= mass

    return [mass, barycenter]

def gravitation(m, M, pos, POS, G=6.67e-11, e=5e-4):
    vec = POS - pos
    R = np.linalg.norm(vec)
    angle = np.arctan2(vec[1], vec[0])

    force = G*m*M/(R**2 + e**2)
    fx = force*np.cos(angle)
    fy = force*np.sin(angle)

    return np.array((fx, fy))

### ENERGY ###
