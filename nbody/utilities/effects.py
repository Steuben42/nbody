# -*- coding: utf-8 -*-
"""
nbody.utilities.effects
"""

import numpy as np

### COLOR ###
def color(prim=None, primLoc=0.8, primScale=0.1, defLoc=0.5, defScale=0.4):
    if (prim == None):
        prim = np.random.randint(1, 4)
    
    c = [0, 0, 0,]

    for i in range(3):
        if (i == prim):
            loc = primLoc
            scale = primScale 
        else:
            loc = defLoc 
            scale = defScale 
        
        c[i] = -1.
        
        while ( (c[i] > 1.0) or (c[i] < 0.0) ):
            c[i] = np.random.normal(loc = loc, scale = scale)
        
    return tuple(c)