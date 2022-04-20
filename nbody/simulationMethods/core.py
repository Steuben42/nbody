# -*- coding: utf-8 -*-
"""
nbody.simulationMethods.core
"""

import itertools
import numpy as np

from ..utilities import *

class particle:
    count = itertools.count().__next__ 

    loggables = {
        "id": 1,
        "mass": 2,
        "position": 1,
        "velocity": 1,
        "acceleration": 1,
        "color": 4,
        "artist": 3,
        "particleLike": 3,
        }

    def __init__(self, mass:int, pos:np.ndarrary, vel:np.ndarray, acc:np.ndarray, pl=False):
        if (not pl):
            self.id = particle.count()
        else:
            self.id = -1
        
        self.mass = mass
        self.position = pos
        self.velocity = vel
        self.acceleration = acc
        
        self.color = effects.color()

        self.artist = None
        self.particleLike = pl

        return
    
    def updateForce(self, pts:list, e=5e-4):
        for pt in pts:
            if (not (self.id == pt.id) ):
                self.acceleration = calculation.gravitation(self.mass, pt.mass, self.position, pt.position, e=e)
        
        return 
    
    def updateState(self, dt:float):
        self.position += self.velocity*dt 
        self.velocity += self.acceleration*dt 

        return 