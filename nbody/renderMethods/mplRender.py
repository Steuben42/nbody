# -*- coding: utf-8 -*-
"""
nbody.renderMethods.mplRender
"""

import matplotlib.pyplot as plt

def window(windowName, bounds=((-100., 100.), (-100., 100.))):
    fig = plt.figure(windowName)
    fig.clf()
    ax = fig.gca()

    ax.set_xlim(bounds[0])
    ax.set_ylim(bounds[1])

    return

def renderPoint(pos, ax, artist=None, color=(25,25,25)):
    if (artist != None):
        artist.remove()
    
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    if (
        pos[0] > xlim[1] or
        pos[0] < xlim[0] or
        pos[1] > ylim[1] or
        pos[1] < ylim[0]
        ):
        artist = None 
        return artist
    
    artist, = ax.plot(pos[0], pos[1], 'o', color=color)

    return artist