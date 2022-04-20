# -*- coding: utf-8 -*-
"""
nbody.simulationMethods.barnesHut.nodes
"""

import itertools

import numpy as np

from ...utilities import *

class node:
    count = itertools.count().__next__

    loggables = {
        "order": 1,
        "nodeId": 1,
        "id": 1,
        "xlim": 2,
        "ylim": 2,
        "length": 3,
        "center": 3,
        "membersN": 2,
        "mass": 3,
        "com": 2,
        "children": 2,
        }

    def __init__(self, order:int, nodeId:int, bounds:tuple, pts:list, dynamicBounds=False):
        self.order = order
        self.nodeId = nodeId
        self.id = node.count()

        if (not dynamicBounds):
            self.xlim, self.ylim = bounds
        else:
            xs = []
            ys = []
            for pt in pts:
                xs.append(pt.position[0])
                ys.append(pt.position[1])
            
            self.xlim = np.array((min(xs), max(xs)))
            self.ylim = np.array((min(ys), max(ys)))

        self.length = self.xlim[1] - self.xlim[0]
        self.center = np.array((np.average(self.xlim), np.average(self.ylim)))

        self.membersN, self.membersObj = self.getContainedPts(pts)
        self.children = []

        self.com = self.center.copy()
        self.mass = 0.
        posV = massV = []
        for mempt in membersObj:
            posV.append(mempt.position)
            massV.append(mempt.mass)
        
        if (posV):
            self.mass, self.com = calculation.barycenter(posV, massV)

        return

    def populate(self, pts:list):
        N = self.membersN

        if (N > 1):
            xL, xU = self.xlim
            yL, yU = self.ylim
            xM, yM = self.center

            x = (xL, xM, xU)
            y = (yL, yM, yU)

            for i in range(4):
                self.children.append(
                    node(self.order + 1,
                    i,
                    (np.array((x[i % 2], x[(i + 1) % 2])), np.array((y[1 - (i // 2)], y[2 - (i // 2)]))),
                    pts)
                    )
                
            for child in self.children:
                child.populate(pts)
            
        return
    
    def refresh(self, pts:list):
        self.membersN, self.membersObj = self.getContainedPts(pts)

        self.mass, self.com = calculation.barycenter(self)

        self.populate(pts)

        return
    
    def getContainedPts(self, pts:list):
        count = 0
        containedPts = []

        for pt in pts:
            if (
                pt.position[0] < self.xlim[1] and
                pt.position[0] >= self.xlim[0] and
                pt.position[1] < self.ylim[1] and
                pt.position[1] >= self.ylim[0]
                ):
                count += 1
                containedPts.append(pt)

        return (count, containedPts)