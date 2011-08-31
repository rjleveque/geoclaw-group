
def box(s):
    from pylab import plot
    xy=s.split()
    x1 = float(xy[0])
    x2 = float(xy[1])
    y1 = float(xy[2])
    y2 = float(xy[3])
    plot([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1],'b-')

def boxfg(outdir="."):
    import os
    from pylab import plot,text,hstack
    from numpy import loadtxt
    try:
        fname = os.path.join(outdir,'setfixedgrids.data')
        fgrids = loadtxt(os.path.join(outdir,'setfixedgrids.data'),skiprows=7)
    except:
        print "*** problem loading ",fname

    if fgrids.ndim == 1:
        nfgrids = 1
    else:
        nfgrids = fgrids.shape[0]

    for irow in range(nfgrids):
        if fgrids.ndim == 1:
            fgrid = fgrids
        else:
            fgrid = fgrids[irow,:]
        x1 = fgrid[3]
        x2 = fgrid[4]
        y1 = fgrid[5]
        y2 = fgrid[6]
        plot([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1],'b-')
        text(x1-0.4*(x2-x1),y1,"FG %s" % str(irow+1))

if __name__=="__main__":
    box('139.427  139.43  42.092  42.095')
    box('139.428  139.431  42.0756  42.0786')
    box('139.425  139.428  42.1156  42.1186')
    box('139.423  139.426  42.0994  42.1024')

