
"""
Module to create topo for this example.
Piecewise linear canonical beach and solitary wave.

"""

from pyclaw.geotools import topotools
import numpy as np

x0 = 19.85
slope = 1./x0
xs = 22.
H = 0.0185

nxpoints = 91
nypoints = 4
xlower = -20.e0
xupper = 60.e0
dx = (xupper-xlower)/(nxpoints-1)
ylower = 0.e0
yupper = (nypoints-1)*dx


def maketopo():
    """
    Output topography file for the entire domain
    """
    outfile= "beach.topotype2"     
    topotools.topo2writer(outfile,topo,xlower,xupper,ylower,yupper,nxpoints,nypoints)



def topo(x,y):
    """
    Piecewise linear beach
    """
    z = np.where(x<x0, -slope*x, -1.)
    
    return z


if __name__=='__main__':
    maketopo()
