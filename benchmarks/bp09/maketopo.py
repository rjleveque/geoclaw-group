"""
Create topo files needed for this example:
    
"""

from pyclaw.geotools import topotools
import os,sys

def gettopo():
    """
    Retrieve the topo file from the GeoClaw repository.
    """

    remote_directory = 'http://kingkong.amath.washington.edu/topo/okushiri'
    files = "AO15.tt1  MO01.tt1  OK03.tt1   OK24.tt1 MB05.tt1 OK08.tt1 HNO1993.txyz \
           OK24T.tt1 OK24R.tt1 OK24B.tt1 OK24L.tt1".split()

    for file in files:
        topotools.get_topo(file, remote_directory)


if __name__=='__main__':
    gettopo()
