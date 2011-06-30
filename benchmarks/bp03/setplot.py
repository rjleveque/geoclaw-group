
"""
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.

Dave George's version.

"""

from pyclaw.geotools import topotools
from pyclaw.data import Data
from pylab import loadtxt
import matplotlib
#matplotlib.rc('text', usetex=True)
#import pdb
import os

datadir = os.path.abspath('.')  # this directory

d = None  # may be set in script that loops over test cases

def read_lab_data(d=None):
    if d==None:
        probdata = Data(os.path.join(datadir,'setprob.data'))
        d = probdata.d
    
    if d==0.061: fname = 'd61g1234-new.txt'
    if d==0.080: fname = 'd80g1234-new.txt'
    if d==0.100: fname = 'd100g124-new.txt'
    if d==0.120: fname = 'd120g124-new.txt'
    if d==0.140: fname = 'd140g1234-new.txt'
    if d==0.149: fname = 'd149g124-new.txt'
    if d==0.189: fname = 'd189g1234-new.txt'
    
    try:
        print "Reading gauge data from ",fname
    except:
        print "*** No gauge data for d = ",d
    
    try:
        fname = os.path.join(datadir,fname)
        gaugedata = loadtxt(fname)
    except:
        raise Exception( "*** Cannot read file %s ",fname)
    gauget = gaugedata[:,0]
    gauge_ave = {}
    for gaugeno in [1,2,3,4]:
        try:
            gauge_ave[gaugeno] = gaugedata[:,3*gaugeno] * 0.001
        except:
            gauge_ave[3] = None
            gauge_ave[4] = gaugedata[:,9] * 0.001

    return gauget, gauge_ave
        
    

#--------------------------
def setplot(plotdata):
#--------------------------

    """
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.

    """


    from pyclaw.plotters import colormaps, geoplot
    from numpy import linspace

    plotdata.clearfigures()  # clear any old figures,axes,items data

    def set_drytol(current_data):
        # The drytol parameter is used in masking land and water and
        # affects what color map is used for cells with small water depth h.
        # The cell will be plotted as dry if h < drytol.
        # The best value to use often depends on the application and can
        # be set here (measured in meters):
        current_data.user.drytol = 1.e-3

    plotdata.beforeframe = set_drytol

    # To plot gauge locations on imshow or contour plot, use this as
    # an afteraxis function:

    figkwargs = dict(figsize=(18,9),dpi=800)
    #-----------------------------------------
    # Figure for imshow plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='imshow', figno=0)
    plotfigure.show = True
    #plotfigure.kwargs = figkwargs
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('imshow')
    plotaxes.title = 'Case 1'
    plotaxes.scaled = True

    def addgauges(current_data,fnt=14):
        from pyclaw.plotters import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
                gaugenos='all', format_string='ko', add_labels=True,markersize=8,fontsize=fnt)

    def fixup(current_data):
        import pylab
        t = current_data.t
        pylab.title('Case 1: surface at %4.2f seconds' % t, fontsize=14)
        #pylab.xticks([141.0325-.03,141.0325,141.0325+.03],fontsize=15)
        #pylab.yticks(fontsize=15)
        #pylab.plot([139.7],[35.6],'wo',markersize=10)
        #pylab.text(138.2,35.9,'Tokyo',color='w',fontsize=25)
        #x_fukushima = 141.0325
        #y_fukushima = 37.421389
        #pylab.plot([x_fukushima],[y_fukushima],'wo',markersize=8)
        #pylab.text(x_fukushima-.015,y_fukushima+.004,'Fukushima',color='w',fontsize=15)
        addgauges(current_data)

    plotaxes.afteraxes = fixup

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.show = True
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.imshow_cmap = geoplot.tsunami_colormap
    plotitem.imshow_cmin = -.02
    plotitem.imshow_cmax = .02
    plotitem.add_colorbar = True
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.gridedges_show = 1

    # Add contour lines of bathymetry:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    from numpy import arange, linspace
    plotitem.contour_levels = arange(-2.5, 1, .01)
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid'}
    plotitem.amr_contour_show = [2]  # show contours only on finest level
    plotitem.gridlines_show = 0
    plotitem.gridedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.show = True
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land1_colormap
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 1.0
    plotitem.add_colorbar = False
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.gridedges_show = 1
    #dx2 = .04
    #dy2 = .08

    plotaxes.xlimits = [-1.0,3.0]
#    plotaxes.xlimits = [-1.0,2.0]

    plotaxes.ylimits = [0,1.]
#    plotaxes.ylimits = [-1.,1.]

    #-----------------------------------------
    # Figure for line plot
    #-----------------------------------------
#    plotfigure = plotdata.new_plotfigure(name='line', figno=500)

    # Set up for axes in this figure:
#    plotaxes = plotfigure.new_plotaxes()
#    plotaxes.xlimits = [-12,12]
#    plotaxes.ylimits = [-12, 12]
#    plotaxes.title = 'Surface'

    # Plot surface as blue curve:
#    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
#    plotitem.plotstyle = 'b-'

    # Plot Runup
#    t,x1,x2 = loadtxt('_output/fort.runup',unpack=True)
#    plot(t,x1)
#    plot(t,x2)

    #-----------------------------------------
    # Figure for cross section of surface
    #-----------------------------------------

#    plotfigure = plotdata.new_plotfigure(name='surface', figno=200)
#    plotaxes = plotfigure.new_plotaxes('surface')
#    plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
#    def crosssec(current_data):
#        q = current_data.q
#        x = current_data.x
#        return x[:,50], q[:,50,3]

#    plotitem.map_2d_to_1d = crosssec
#    def plot_beach(current_data):
#        import pylab
#        x = current_data.x[:,50]
#        pylab.plot(x, -0.5*x,'k')

#    plotaxes.ylimits = [-0.5,0.5]
#    plotaxes.afteraxes = plot_beach
    

    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
                    type='each_gauge')

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [0,5.0]
    #plotaxes.ylimits = [-0.03,0.03]
    plotaxes.title = 'Surface'

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

    # Plot fine grid as red curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.show = False
    #plotitem.outdir = '_output_fine'
    plotitem.plot_var = 3
    plotitem.plotstyle = '-'
    plotitem.color = 'r'

    # Plot topo as green curve:
    #plotitem = plotaxes.new_plotitem(plot_type='1d_plot')


    def gaugetopo(current_data):
        q = current_data.q
        h = q[:,0]
        eta = q[:,3]
        topo = eta - h
        return eta

    plotitem.plot_var = gaugetopo
    plotitem.clf_each_gauge = False
    plotitem.plotstyle = 'b-'

    def add_zeroline(current_data):
        from pylab import plot, legend, xticks, floor
        t = current_data.t
        #legend(('surface','topography'),loc='lower left')
        plot(t, 0*t, 'k')
        #n = floor(t.max()/3600.) + 2
        xticks([range(10)])
    #plotaxes.afteraxes = add_zeroline

    def plot_labData(current_data):
        import pylab
        gaugeno = current_data.gaugeno
        gauget, gauge_ave = read_lab_data(d)
        try:
            pylab.plot(gauget,gauge_ave[gaugeno],'k')
            pylab.legend(('GeoClaw', 'Lab Data'), loc='lower right')
            #pylab.legend(('GeoClaw coarse', 'GeoClaw fine', 'Lab Data'), loc='lower right')
        except:
            print "No data for gauge ",gaugeno
        #gaugeTime
    plotaxes.afteraxes = plot_labData

    def add_tankdata(datafile):
        from pylab import plot
        import numpy as np
        ts = np.loadtxt(datafile)
        plot(ts[:,0],ts[:,1], 'k-')

    #-----------------------------------------

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = [0]             # list of frames to print
    plotdata.print_gaugenos = 'all'        # list of gauges to print
    plotdata.print_fignos = [300]            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = False                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

