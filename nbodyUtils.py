# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 11:09:25 2022

Steven Shockley

nbodyUtils
"""

import numpy as np

import csv
import os

############################### SUPERFICIALS ##################################
def color(prim=None, primLoc=0.8, primScale=0.1, defLoc=0.5, defScale=0.4):
    """
    Generates a random color in RGB.

    Parameters
    ----------
    prim : Int, optional
        The favored primary color. The default is None.
    primLoc : Float, optional
        The mean for the favored color. The default is 0.8.
    primScale : Float, optional
        The standard deviation for the favored color. The default is 0.1.
    defLoc : Float, optional
        The default mean. The default is 0.5.
    defScale : Float, optional
        The default standard deviation. The default is 0.4.

    Returns
    -------
    Tuple
        An RGB value in the form of a tuple.

    """
    if prim==None:
        prim = np.random.randint(1,4)
    
    c = [0,0,0]
    for i in range(3):
        if i==prim:
            loc=primLoc
            scale=primScale
        else:
            loc=defLoc
            scale=defScale
        c[i] = -1.
        while c[i] > 1.0 or c[i] < 0.0:
            c[i] = np.random.normal(loc=loc, scale=scale)
    
    return tuple(c)

#################################### CALCULATIONS #############################
def gravitation(m, M, pos, POS, G=6.67e-11, e=5e-4):
    vec = POS - pos
    R = np.linalg.norm(vec)
    angle = np.arctan2(vec[1], vec[0])
    
    force = G*m*M/(R**2 + e**2)
    fx = force*np.cos(angle)
    fy = force*np.sin(angle)
    
    return np.array((fx, fy))

def barycenter(node):
    mass = 0
    barycenter = node.center.copy()
    if not node.membersObj:
        return mass,barycenter
    
    for pt in node.membersObj:
        mass += pt.mass
        barycenter += pt.position*pt.mass
    
    barycenter /= mass
        
    return mass,barycenter

def particleEnergy(pt,pts):
    POT = 0
    KE = 0
    for expt in pts:
        POT += np.linalg.norm(gravitation(pt.mass,expt.mass,pt.position,expt.position))*np.linalg.norm(pt.position - expt.position)
    
    KE = (0.5)*pt.mass*np.linalg.norm(pt.velocity)**2
    return POT + KE

#################################### SORTING ##################################
def getContained(bounds,pts):
    count = 0
    containedPts = []
    
    for pt in pts:
        if pt.position[0]<bounds[0][1] and pt.position[0]>bounds[0][0] and pt.position[1]<bounds[1][1] and pt.position[1]>bounds[1][0]:
            count += 1
            containedPts.append(pt)
            
    return count,containedPts

#################################### LOGGING ##################################
def log(level,):
    lvls = ['[!FATAL]','[ERROR]','(WARNING)','{INFO}']
    return

def initCSV():
    with open('dataLog.csv', 'w', newline='') as file:
            w = csv.writer(file)
            w.writerow([None])
    return

def CSVentry(frame,obj,detailLevel=1):
    with open('dataLog.csv', 'a', newline='') as file:
        
        w = csv.writer(file)
        
        entry = [str(frame),str(type(obj))]
        
        for l in obj.loggables:
            if obj.loggables[l] <= detailLevel:
                entry.append(l + ': ' + str(getattr(obj,l)))
                
        w.writerow(entry)
    return