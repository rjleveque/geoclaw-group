"""
Plot fixed grid output.
fgno refers to the number of the fixed grid
Execute from Unix command line via:
    $ python plotfg.py 1
to plot fixed grid number 1, for example.
Specify output directory other than _output by adding the outdir to this line:
    $ python plotfg.py 1 _output-05

    
Or from within Python or IPython:
    >>> import plotfg
    >>> plotfg.fgloop(fgno=1, outdir='_output-05')
"""

from pylab import *
from pyclaw.plotters import geoplot, colormaps
import os
from numpy import ma

drytol = 1.e-2


def plotfg(fgno, frameno, outdir='_output'):
    fname = "fort.fg%s_%s" % (str(fgno).zfill(2), str(frameno).zfill(4))
    fname = os.path.join(outdir,fname)
    if not os.path.exists(fname):
        print "*** Did not find file ",fname," in directory ",outdir
        raise IOError("Missing fixed grid output file")
    
    print "Plotting ",fname

    # Read parameters from header:

    file = open(fname,'r')

    line = file.readline()
    t = float(line.split()[0])
    print 't = %s' % t

    line = file.readline()
    mx = int(line.split()[0])
    print 'mx = %s' % mx

    line = file.readline()
    my = int(line.split()[0])
    print 'my = %s' % my

    line = file.readline()
    xlow = float(line.split()[0])
    print 'xlow = %s' % xlow

    line = file.readline()
    ylow = float(line.split()[0])
    print 'ylow = %s' % ylow

    line = file.readline()
    xhi = float(line.split()[0])
    print 'xhi = %s' % xhi

    line = file.readline()
    yhi = float(line.split()[0])
    print 'yhi = %s' % yhi
    file.close()



    x = linspace(xlow,xhi,mx+1)
    y = linspace(ylow,yhi,my+1)
    dx = x[1]-x[0]
    dy = y[1]-y[0]
    xcenter = x[:-1] + dx/2.
    ycenter = y[:-1] + dy/2.

    d = loadtxt(fname, skiprows=8)

    h = reshape(d[:,0], (my,mx))
    B = reshape(d[:,3], (my,mx))
    eta = reshape(d[:,4], (my,mx))
    surface = ma.masked_where(isnan(eta),eta)
    land = ma.masked_where(h>drytol,B)


    # plot commands: 
    # ==============
    
    figure(150)
    clf()
    
    if ma.count(surface) != 0:
        pcolormesh(x,y,surface,cmap=geoplot.tsunami_colormap)
    clim((-0.03,0.03))
    colorbar()
    
    if ma.count(land) != 0:
        pcolormesh(x,y,land,cmap=geoplot.land_colors)
    
    contour(xcenter,ycenter,B,20,colors='k')
    contour(xcenter,ycenter,B,[0.],colors='w')
    
    
    #xlim((xlow,xhi))
    #ylim((ylow,yhi))

    ncols = d.shape[1]
    
    if ncols > 5:
        # Add red contour of maximum eta
        etamax = reshape(d[:,6], (my,mx))
        #etamax2 = where(B<0, 1., etamax)
        etamax2 = where(B<0, 1., etamax)
        
        contour(xcenter,ycenter,etamax2,[-drytol,0.],colors='r',linewidths=2)
        
        # Add blue contour of minimum eta
        etamin = reshape(d[:,5], (my,mx))
        #contour(xcenter,ycenter,etamin,[drytol, 0],colors='b',linewidths=2)
            
    axis('scaled')
            
    title('time = %8.5f' % t)
    
    return_fg = True  # return all the fg arrays for other purposes?
    if return_fg:
        fg = empty((my,mx,ncols), dtype=float)
        for col in range(ncols):
            fg[:,:,col] = reshape(d[:,col],(my,mx))
        return fg
        
    
def fgloop(fgno=1, outdir='_output'):
    for frameno in range(1,100):
        try:
            fg = plotfg(fgno, frameno, outdir)
        except IOError:
            break
        ans = raw_input("Hit return for next time, q to quit, s to savefig... ")
        if ans=='s':
            fname = 'FixedGrid%sFrame%s.png' %  (str(fgno).zfill(2), str(frameno).zfill(4))
            savefig(fname)
            print "Saved figure as ",fname
            ans = raw_input("Hit return for next time, q to quit, s to savefig... ")
            
        if ans=='q':
            break
            

if __name__ == "__main__":
    # if executed at the Unix command line....
    import sys
    args = sys.argv[1:]   # any command line arguments
    fgloop(*args)
