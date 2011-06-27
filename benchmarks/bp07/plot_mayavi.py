import os
from pylab import *
from enthought.mayavi import mlab
from pyclaw.plotters.data import ClawPlotData
from setplot import setplot
from html_movie import make_movie


def plotframe(frameno,level=1):

    plotdata = ClawPlotData()
    plotdata.outdir = "_output"
    print "Plotting solution from ",plotdata.outdir
    plotdata = setplot(plotdata)
    try:
        frame = plotdata.getframe(frameno)
    except:
        print "Unable to get frame"
        return
    mlab.figure(1,bgcolor=(1,1,1),size=(700,600))
    mlab.clf()
    for grid in frame.grids:
        if grid.level <= level:

            y = grid.c_center[1]
            x = grid.c_center[0]
            q = grid.q
            eta = q[:,:,3]
            h = q[:,:,0]
            #return x,y,eta
            #eta = where(q[:,:,0] > 1.,eta,nan)
            #import pdb; pdb.set_trace()
        
            topo = eta - h
            cutoff = 0.5
            #cutoff2 = -500.
            shift = 0.
            scale = 10.
            topo1 = scale*where(topo<cutoff, topo-shift, cutoff-shift)
            #topo1 = scale*where(topo>cutoff2, topo1, nan)
            eta1 = scale*where(eta<cutoff, eta-shift, cutoff-shift)
            water1 = where(h>=1.e-3, eta1, nan)
            mlab.mesh(x,y,topo1,colormap='Greens',vmin=-1.0, vmax=0.8)
            mlab.mesh(x,y,water1,colormap='Blues',vmin=-0.8, vmax=0.8)
            #mlab.surf(x,y,topo1,colormap='Greens',warp_scale=10,vmin=-0.8,vmax=0.5)
            #mlab.surf(x,y,water1,colormap='Blues',warp_scale=10,vmin=-0.8,vmax=0.5)
            V = (150.95115856920216,\
             80.12676623482308,\
             13.359093592227218,\
             array([ 2.744     ,  1.70099999, -0.04745156]))
             
            V =  (-108.612973405259,\
              62.96905073871072,\
              13.359093592227456,\
              array([ 2.744     ,  1.70099999, -0.04745156]))
 
            mlab.view(*V)
    t = frame.t
    mlab.title('Time = %5.2f' % t,color=(0,0,0),height=0.1,size=0.5)
    
def make_all_frames(figno):
  
    frames = range(85)
    plotfiles = []
    for frameno in frames:
        plotframe(frameno)
        frstring = str(int(frameno)).zfill(3)
        name = "monai-%s-frame%s.png" % (figno,frstring)
        plotfiles.append(name)
        mlab.savefig("monai-%s-frame%s.png" % (figno,frstring))
        make_movie(plotfiles, moviename='monai-%s.html' % figno)
        
        #os.system("convert island-%s-frame%s.png island-%s-frame%s.eps" \
         #   % (figno,frstring,figno,frstring))