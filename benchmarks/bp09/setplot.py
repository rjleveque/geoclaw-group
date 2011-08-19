""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

from pyclaw.geotools import topotools
from pyclaw.data import Data
import pylab
import glob

Esashidata = pylab.loadtxt('Esashi.txt', skiprows=1)
Iwanaidata = pylab.loadtxt('Iwanai.txt', skiprows=1)

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

    # To plot gauge locations on imshow or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        from pyclaw.plotters import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos='all', format_string='ko', add_labels=True, fontsize=8)

    #-----------------------------------------
    # Figure for imshow plot
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name='full domain', figno=0)
    plotfigure.show = True  # Turn the imshow plot on or off (True or False) 

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('imshow')
    plotaxes.show = True  ### Turn on or off the full domain plot
    plotaxes.title = 'Surface'
    plotaxes.scaled = True

    def fixup(current_data):
        import pylab
        t = current_data.t
        # pylab.title('Surface at %4.2f seconds' % t, fontsize=20)       
        t = t / 60.  # minutes
        pylab.title('Surface at %4.2f minutes' % t, fontsize=20)
        pylab.xticks(fontsize=15)
        pylab.yticks(fontsize=15)
        #pylab.plot([205],[20],'wo',markersize=5)
        #pylab.text(201,22,'Hawaii',color='w',fontsize=15)
        # pylab.plot([139.7],[35.6],'wo',markersize=5)
        # pylab.text(135.2,35.9,'Tokyo',color='w',fontsize=15)
        # pylab.plot([235.81],[41.75],'wo',markersize=5)
        # pylab.text(235.9,42,'Crescent City',color='w',fontsize=15)
        addgauges(current_data)
    plotaxes.afteraxes = fixup
    
    plotaxes.xlimits = [137.57,141.41] # Full Domain
    plotaxes.ylimits = [39.67,44.15] # Full Domain
    # plotaxes.xlimits = [139., 140.] ## Okushiri Island (Large area)
    # plotaxes.ylimits = [41.5, 42.5]   ## Okushiri Island  (Large area)
    # plotaxes.xlimits = [139.43, 139.48] ## Aonae peninsula
    # plotaxes.ylimits = [42.03, 42.06]   ## Aonae peninsula
    # plotaxes.xlimits = [139.35, 139.6] ## Okushiri Island (Tight)
    # plotaxes.ylimits = [42.0, 42.25]   ## Okushiri Island (Tight)
    # plotaxes.xlimits = [139.41, 139.43] ## Monai Long Coast
    # plotaxes.ylimits = [42.08, 42.15]   ## Monai Long Coast
    # plotaxes.xlimits = [139.418, 139.426] ## Monai Short
    # plotaxes.ylimits = [42.096, 42.106]   ## Monai Short

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.show = True
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    # plotitem.imshow_cmap = geoplot.tsunami_colormap
    # plotitem.imshow_cmap = colormaps.blue_white_red
    # dictionary of [R,G,B] values at different levels:
    my_cmap_surface = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                      -0.02: [0.75,0.75,1.0], \
                                       0.0: [1.0,1.0,1.0], \
                                       0.02: [1.0,0.75,0.75], \
                                       1.0: [1.0,0.0,0.0]})
    plotitem.imshow_cmap = my_cmap_surface
    plotitem.imshow_cmin = -20.
    plotitem.imshow_cmax =  20.
    plotitem.add_colorbar = True
    plotitem.amr_gridlines_show = [0,0,0,0,0] # Turn off/0n = 0/1 gridlines for levels [1,2,3, ...]
    # plotitem.gridedges_show = 0
    #plotitem.amr_data_show = [1,1,1,1,0]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.show = True
    plotitem.plot_var = geoplot.land
    my_cmap_land = colormaps.make_colormap({ \
                                            0.0: [0.0,1.0,0.0], \
                                            1.0: [0.0,0.5,0.0] \
                                            })
    plotitem.imshow_cmap = my_cmap_land                                   
    # plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = True
    # plotitem.amr_gridlines_show = [0,0,0]
    # plotitem.gridedges_show = 0
    #plotitem.amr_data_show = [1,1,1,1,0]

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = linspace(-5000,-100,6)
    plotitem.amr_contour_colors = ['y']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':1}
    # plotitem.amr_contour_show = [0,0,0]  
    # plotitem.gridlines_show = 0
    # plotitem.gridedges_show = 0
    #plotitem.amr_data_show = [1,1,1,0]

    # Topo = Bathymetry and Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    # plotitem.imshow_cmap = geoplot.bathy3_colormap  #Try 1, 2 & 3
    
    my_cmap_topo = colormaps.make_colormap({ \
        -5000.0: [0,0,1], 0.0: [1,1,1], 100.0: [0.0,0.5,0.0] \
                                            })
    plotitem.imshow_cmap = my_cmap_topo
    
    plotitem.imshow_cmin = -5000.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = False
    # plotitem.amr_gridlines_show = [0,0,0]
    # plotitem.gridedges_show = 0
    #plotitem.amr_data_show = [1,1,1,1,0]

    # add contour lines of topo if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = linspace(-5000,-100,6)
    plotitem.amr_contour_colors = ['y']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':1}
    # plotitem.amr_contour_show = [0,0,0]  
    # plotitem.gridlines_show = 0
    # plotitem.gridedges_show = 0
    #plotitem.amr_data_show = [1,1,1,0]

    #-----------------------------------------
    # Figure for zoom plot  
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Zoom', figno=1)
    plotfigure.show = False  # Turn the zoom plot on or off (True or False) 

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('imshow')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    ## 
    # plotaxes.xlimits = [140.3, 140.5] ## Esashi Tide Gage
    # plotaxes.ylimits = [41.75, 41.95] ## Esashi Tide Gage
    # plotaxes.xlimits = [139.35, 139.6] ## Okushiri Island
    # plotaxes.ylimits = [42.0, 42.25]   ## Okushiri Island
    # plotaxes.xlimits = [139.43, 139.48] ## Aonae peninsula
    # plotaxes.ylimits = [42.03, 42.06]   ## Aonae peninsula
    # plotaxes.xlimits = [139.41, 139.43] ## Monai
    # plotaxes.ylimits = [42.08, 42.15]   ## Monai
    # plotaxes.xlimits = [139.41385190, 139.42639510] ## MB05 Monai grid
    # plotaxes.ylimits = [42.09458550, 42.10343920]   ## MB05 Monai grid
    plotaxes.xlimits = [139., 140.] ## Okushiri Island
    plotaxes.ylimits = [41.5, 42.5]   ## Okushiri Island

    # dx = 0.00005
    # dy = 0.00005
    # plotaxes.xlimits = [139.423714744650-dx, 139.423714744650+dx] ## Station 8, Monai valley
    # plotaxes.ylimits = [ 42.100414145210-dy,  42.100414145210+dy] ## Station 8, Monai valley

    def fixup(current_data):
        import pylab
        addgauges(current_data)
        t = current_data.t
        pylab.title('Surface at %4.2f seconds' % t, fontsize=20)       
        # t = t / 60.  # minutes
        # pylab.title('Surface at %4.2f minutes' % t, fontsize=20)       
#       pylab.plot([139.7],[35.6],'wo',markersize=10)
#       pylab.text(138.2,35.9,'Tokyo',color='w',fontsize=25)
    plotaxes.afteraxes = fixup

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    # plotitem.imshow_cmap = geoplot.tsunami_colormap 
    plotitem.imshow_cmap = colormaps.blue_white_red
    plotitem.imshow_cmin = -5.
    plotitem.imshow_cmax =  5.
    plotitem.add_colorbar = True
    plotitem.amr_gridlines_show = [0,0,0]  ##Levels of refinement
    plotitem.gridedges_show = 1
    
    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = True
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = linspace(-1000,100,11)
    plotitem.amr_contour_colors = ['y']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [1,0,0]  
    plotitem.gridlines_show = 1
    plotitem.gridedges_show = 1

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = geoplot.land
    plotitem.imshow_cmap = geoplot.land_colors
    plotitem.imshow_cmin = 0.0
    plotitem.imshow_cmax = 100.0
    plotitem.add_colorbar = True
    plotitem.amr_gridlines_show = [0,0,0]
    plotitem.gridedges_show = 1

    # add contour lines of land if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = True
    plotitem.plot_var = geoplot.land
    plotitem.contour_levels = linspace(0,100,10)
    plotitem.amr_contour_colors = ['y']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0]  
    plotitem.gridlines_show = 0
    plotitem.gridedges_show = 0

    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=2, \
                    type='each_gauge')
    plotfigure.clf_each_gauge = True     # Switch gauge figures on or off

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    # plotaxes.ylimits = 'auto'
    plotaxes.ylimits = [-20.,20.]
    plotaxes.title = 'Surface'

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'
    plotitem.kwargs = {'linewidth':2}

    # Plot topo as green curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.show = True

    def gaugetopo(current_data):
        q = current_data.q
        h = q[:,0]
        eta = q[:,3]
        topo = eta - h
        return topo
        
    plotitem.plot_var = gaugetopo
    plotitem.plotstyle = 'g-'
    
    def add_zeroline(current_data):
        from pylab import plot, legend, xticks, floor, xlim
        t = current_data.t
        dtaxis=60.  # Set the axis time increment, in seconds
        #t = t/dtaxis
        tmax = t.max()
	#print "tmax = ",tmax
        legend(('surface','topography'),loc='lower left')
        plot([0,tmax],[0,0],'k')
        n = int(floor(tmax) + 2)
        xticks([dtaxis*i for i in range(n)])
        xlim(0.,tmax)
    plotaxes.afteraxes = add_zeroline
    
    def plot_TG(current_data):
        import pylab
        gaugeno = current_data.gaugeno
        if gaugeno == 5000:
            try:
                pylab.plot(Esashidata[:,0],Esashidata[:,1],'k')
                pylab.legend(['GeoClaw','Esashi data'])
            except:
                pylab.legend(['GeoClaw'])
        if gaugeno == 6000:
            try:
                pylab.plot(Iwanaidata[:,0],Iwanaidata[:,1],'k')
                pylab.legend(['GeoClaw','Iwanai data'])
            except:
                pylab.legend(['GeoClaw'])
        add_zeroline(current_data)
    plotaxes.afteraxes = plot_TG

    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

# Figure Printing
    plotdata.printfigs = True                # All figures printed
    # plotdata.printfigs = False             # No figures printed
    plotdata.print_format = 'png'            # file format
# Frame Printing
    plotdata.print_framenos = 'all'          # All frame figures printed
    # plotdata.print_framenos = []               # No frame figures printed
    # plotdata.print_framenos = range(0,21)    # List of frame figures to print (n1:n2-1)
# Gauge Printing
    # plotdata.print_gaugenos = 'all'        # All gauge figures printed
    plotdata.print_gaugenos = []         # No gauge figures printed
    # plotdata.print_gaugenos = range(201,210) # List of gauge figures to print range(n1,n2-1)

# Print Figures (Both Frames and Gauges)
    plotdata.print_fignos = 'all'            # list of figures to print

# Create html or latex files
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?

# Specify Layout of Plots
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata
