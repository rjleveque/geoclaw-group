
"""
Download the Monai Valley model bathymetry and massage the data to
produce a topo file with topotype=2 for use in GeoClaw.

Note:
The data file has a first row that must be skipped and the data in the wrong
order for standard GeoClaw input styles described at
begin_html
[http://www.clawpack.org/users/topo.html]
end_html

"""
import os, numpy
from pyclaw.geotools import topotools
import urllib

def maketopo():
    infile = 'MonaiValley_Bathymetry.txt'
    url ='http://nctr.pmel.noaa.gov/benchmark/Laboratory/Laboratory_MonaiValley'
    
    # Retrieve the topo file if it's not already here:
    if not os.path.exists(infile):
        print "Retrieving remote file ", infile
        print "      from ", url
        try:
            remote_file = os.path.join(url, infile)
            urllib.urlretrieve(remote_file, infile)
        except:
            raise Exception("urlretrieve failed")

    print "Fixing topo file"
    x,y,z = numpy.loadtxt(infile, skiprows=1, unpack=True)


    # Reshape to proper array:
    mx = 393
    my = 244
    X = numpy.reshape(x,(mx,my))
    Y = numpy.reshape(y,(mx,my))
    Z = numpy.reshape(z,(mx,my))
    #import pdb; pdb.set_trace()


    # Negate the topo values since GeoClaw expects negative for bathy below sea
    # level.
    Z = -Z  

    # create output file:
    outfile = 'MonaiValley.tt2'
    xlower = X[0,0]
    xupper = X[-1,-1]
    ylower = Y[0,0]
    yupper = Y[-1,-1]
    dx = (xupper - xlower) / mx
    dy = (yupper - ylower) / my
    if abs(dx-dy) > 1e-6:
        print "*** dx and dy are not equal!"
        print "*** dx = %s,  dy = %s" %(dx,dy)
    cellsize = dx
    
    ofile = open(outfile, 'w')
    ofile.write('%s ncols\n' % mx)
    ofile.write('%s nrows\n' % my)
    ofile.write('%s xll\n' % xlower)
    ofile.write('%s yll\n' % ylower)
    ofile.write('%s cellsize\n' % cellsize)
    ofile.write('9999 nodata_value\n')

    for jj in range(my):
        j = my-1-jj
        for i in range(mx):
            ofile.write('%20.12e\n' % Z[i,j])

    ofile.close()
    print "Created ",outfile


if __name__=="__main__":
    maketopo()
