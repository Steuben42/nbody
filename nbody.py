# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 11:37:03 2022

Steven Shockley
"""

import itertools
import numpy as np

import nbodyUtils as util

class particle:
    count = itertools.count().__next__ 
    
    def __init__(self, mass:int, pos:np.ndarray, vel:np.ndarray, acc:np.ndarray, pl=False):
        if not pl:
            self.id = particle.count()
        else:
            self.id = -1
        
        self.mass = mass
        self.position = pos
        self.velocity = vel
        self.acceleration = acc
        
        self.color = util.color()
        
        self.artist = None
        self.particleLike = pl
        
        self.loggables = {
            "id": 1,
            "mass": 2,
            "position": 1,
            "velocity": 1,
            "acceleration": 1,
            "color": 4,
            "artist": 3,
            "particleLike": 3,
            }
        return
    
    def updateState(self, dt):
        self.position += self.velocity*dt
        self.velocity += self.acceleration*dt
        return
    
    def updateForce(self, pts, e=5e-4):
        for pt in pts:
            if not self.id==pt.id:
                self.acceleration = util.gravitation(self.mass, pt.mass, self.position, pt.position, e=e)/self.mass
        return
    
    def updateForceBH(self, pts, node, z=0.5):
        if self not in node.membersObj:
            return
        
        o=1
        N=[]
        ptsN = node.membersN
        nodeTree = []
        currentNode = node
        while ptsN>1:
            for n in currentNode.children:
                if self in n.membersObj:
                    o = n.order 
                    N.append(n.node) 
                    ptsN = n.membersN
                    nodeTree.append(currentNode)
                    currentNode = n
        
        ptsLike = self.getPointsLike(pts, node, nodeTree, o, z)
        
        self.updateForce(ptsLike)
        return
    
    def getPointsLike(self, pts, node, nodeTree, o, z):
        ptsLike = []
        # get children of the current node
        #   if node is in the point's node tree
        #       if child node is not of the lowest node's order
        #           add points from this function entering the current child node
        #       skip current child node
        #
        #   if size of node over distance to COM is too big
        #       add points from func entering current child node
        #   or
        #       add particle like of this node
        for n in node.children:
            if n.membersN==0:
                continue
            
            if n in nodeTree:
                if n.order!=o:
                    ptsLike += self.getPointsLike(pts, n, nodeTree, o, z)
                continue
            
            if n.orderLength/np.linalg.norm(n.COM - self.position)>z:
                ptsLike += self.getPointsLike(pts, n, nodeTree, o, z)
            else:
                ptsLike.append(particle(n.mass, n.COM, np.array([0.,0.]), np.array([0.,0.]), pl=True))
        
        return ptsLike
    
    def mplRender(self, ax): 
        if self.artist!=None:
            self.artist.remove()
        
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        if self.position[0]>xlim[1] or self.position[0]<xlim[0] or self.position[1]>ylim[1] or self.position[1]<ylim[0]:
            self.artist = None
            return
        
        self.artist, = ax.plot(self.position[0], self.position[1], 'o', color=self.color)
        return

class node:
    def __init__(self,order,node,bounds,pts):
        self.order = order
        self.node = node
        self.xlim,self.ylim = bounds
        self.orderLength = self.xlim[1] - self.xlim[0]
        self.center = np.array((np.average(self.xlim),np.average(self.ylim)))
        
        self.membersN,self.membersObj = util.getContained((self.xlim,self.ylim),pts)
        
        self.mass,self.COM = util.barycenter(self)
        
        self.children = []
        
        self.loggables = {
            "order": 1,
            "node": 1,
            "xlim": 2,
            "ylim": 2,
            "orderLength": 3,
            "center": 3,
            "membersN": 2,
            "mass": 3,
            "COM": 2,
            "children": 2,
            }
        return
    
    def populate(self, pts):
        N = self.membersN
        
        if N>1:
            xL,xU = self.xlim
            yL,yU = self.ylim
            xM,yM = self.center
            
            self.children = [
                node(self.order+1,1,(np.array((xL,xM)),np.array((yM,yU))),pts),
                node(self.order+1,2,(np.array((xM,xU)),np.array((yM,yU))),pts),
                node(self.order+1,3,(np.array((xL,xM)),np.array((yL,yM))),pts),
                node(self.order+1,4,(np.array((xM,xU)),np.array((yL,yM))),pts)
                ]
            
            for child in self.children:
                child.populate(pts)
        
        #node(i,1,(np.array((n.xlim[0],n.center[0])),np.array((n.center[1],n.ylim[1]))),pts)
        #node(i,2,(np.array((n.center[0],n.xlim[1])),np.array((n.center[1],n.ylim[1]))),pts)
        #node(i,3,(np.array((n.xlim[0],n.center[0])),np.array((n.ylim[0],n.center[1]))),pts)
        #node(i,4,(np.array((n.center[0],n.xlim[1])),np.array((n.ylim[0],n.center[1]))),pts)
        return
    
    def refresh(self, pts):
        self.membersN,self.membersObj = util.getContained((self.xlim,self.ylim),pts)
        
        self.mass,self.COM = util.barycenter(self)
        
        self.populate(pts)
        return