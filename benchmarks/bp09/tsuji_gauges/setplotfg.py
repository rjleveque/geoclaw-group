"""
Set up data for plotting fixed grids.
This is used in setplot.py.

To use interactively:
    >>> fgdata = setplotfg(fgno, outdir)  # for grid number fgno 
    >>> fgdata.fgloop()          # to loop through frames "
    >>> fgdata.plotfg(frameno)   # to plot one frame"
    >>> fgdata.fg2html('all')    # to make html files of all plots"

"""

def setplotfg(fgno=1, outdir='_output'):
    from pyclaw.plotters import plotfg, colormaps, geoplot
    from numpy import arange

    fgdata = plotfg.ClawPlotFGData()

    # Set attributes as desired:

    fgdata.outdir = outdir
    fgdata.plotdir = '.'

    # Fixed grid to display:
    fgdata.fgno = fgno

    if fgno>0:

        # Plot parameters for Fixed Grid 1.
        # Repeat as needed for other fixed grids.
        # Contour levels for all plots:
        fgdata.clines = arange(-20,32,2)

        # For plot of surface eta each frame:
        fgdata.eta_show = True
        my_cmap_surface = colormaps.make_colormap({-1.0: [0.0,0.0,1.0], \
                                              -0.02: [0.75,0.75,1.0], \
                                               0.0: [1.0,1.0,1.0], \
                                               0.02: [1.0,0.75,0.75], \
                                               1.0: [1.0,0.0,0.0]})
        fgdata.water_cmap =  my_cmap_surface
        fgdata.water_clim = (-20,20)

        fgdata.land_cmap =  geoplot.land_colors
        fgdata.land_clim = (0,40)

        # For plot of inundation region:
        fgdata.inundated_show = True
        fgdata.inundated_cmap =  colormaps.make_colormap({0:[0,0.3,1],\
                1:[0,1,1],1.01:[0,1,1], 4:[0,1,0], 10:[1,0.2,0.2]})
        fgdata.inundated_clim =(0,10)

        # For plot of exposed seafloor:
        fgdata.seafloor_show = False
        fgdata.seafloor_cmap =  geoplot.seafloor_colormap
        fgdata.seafloor_clim = (-1,0)

        fgdata.save_png = False

        fgdata.drytol = 1.e-2
        fgdata.exposed_tol = 1.e-2



    return fgdata
