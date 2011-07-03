
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

gaugeData1 = loadtxt('Delta_0025_WaveGage_1.txt',skiprows=0)
gaugeData2 = loadtxt('Delta_0025_WaveGage_2.txt',skiprows=0)
gaugeData3 = loadtxt('Delta_0025_RunupGage_2.txt',skiprows=0)
gaugeData4 = loadtxt('Delta_0025_RunupGage_3.txt',skiprows=0)
gaugeTime = {}
gaugeTime[1] = gaugeData1[:,0]
gaugeTime[2] = gaugeData2[:,0]
gaugeTime[12] = gaugeData3[:,0]
gaugeTime[13] = gaugeData4[:,0]
g = {}
g[1] = gaugeData1[:,1]
g[2] = gaugeData2[:,1]
g[12] = gaugeData3[:,1]
g[13] = gaugeData4[:,1]


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
                gaugenos=[1,2], format_string='ko', add_labels=True,markersize=8,fontsize=fnt)

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
    plotitem.imshow_cmin = -.1
    plotitem.imshow_cmax = .1
    plotitem.add_colorbar = False
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.gridedges_show = 1

    # Add contour lines of bathymetry:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    from numpy import arange, linspace
    plotitem.contour_levels = arange(-2.5, 1, .05)
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

    plotaxes.xlimits = [-1.0,5.0]
#    plotaxes.xlimits = [-1.0,2.0]

    plotaxes.ylimits = [0,1.85]
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
    plotaxes.xlimits = [0,10.0]
    plotaxes.ylimits = [-0.7,0.7]
    plotaxes.title = 'Surface'

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

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
        pylab.plot(gaugeTime[gaugeno],g[gaugeno],'k')
        pylab.legend(('GeoClaw', 'Lab Data'), loc='upper right')
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
    plotdata.print_framenos = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30] #'all'        # list of frames to print
    plotdata.print_gaugenos = 'all'        # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = False                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

