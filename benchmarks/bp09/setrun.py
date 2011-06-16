"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

import os
from pyclaw import data
import numpy as np


#------------------------------
def setrun(claw_pkg='geoclaw'):
#------------------------------

    """
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "geoclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData

    """

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    ndim = 2
    rundata = data.ClawRunData(claw_pkg, ndim)

    #------------------------------------------------------------------
    # Problem-specific parameters to be written to setprob.data:
    #------------------------------------------------------------------

    #probdata = rundata.new_UserData(name='probdata',fname='setprob.data')

    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------

    rundata = setgeo(rundata)   # Defined below

    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amr2ez.data for AMR)
    #------------------------------------------------------------------

    clawdata = rundata.clawdata  # initialized when rundata instantiated


    # Set single grid parameters first.
    # See below for AMR parameters.


    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.ndim = ndim

    # Lower and upper edge of computational domain:
    clawdata.xlower = 130.  ##
    clawdata.xupper = 250.  ##

    clawdata.ylower = 20.  ##
    clawdata.yupper = 60.  ##


    # Number of grid cells:
    clawdata.mx = 60  ##
    clawdata.my = 20  ##


    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.meqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.maux = 3

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.mcapa = 2



    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0.0


    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.outstyle = 1 ##

    if clawdata.outstyle==1:
        # Output nout frames at equally spaced times up to tfinal:
        clawdata.nout =  18##
        clawdata.tfinal = 64800 ##
#        clawdata.nout =  1##
#        clawdata.tfinal = 1##
        
    elif clawdata.outstyle == 2:
        # Specify a list of output times.
        from numpy import arange,linspace
        #clawdata.tout = list(arange(0,3600,360)) + list(3600*arange(0,21,0.5))
#        clawdata.tout = list(linspace(0,32000,9)) + \
#                        list(linspace(32500,40000,16))
        clawdata.tout = list(linspace(0,4,2))
        clawdata.nout = len(clawdata.tout)

    elif clawdata.outstyle == 3:
        # Output every iout timesteps with a total of ntot time steps:
        iout = 1
        ntot = 1
        clawdata.iout = [iout, ntot]



    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 1



    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==1: variable time steps used based on cfl_desired,
    # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
    clawdata.dt_variable = 1

    # Initial time step for variable dt.
    # If dt_variable==0 then dt=dt_initial for all steps:
    clawdata.dt_initial = 0.016

    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99

    # Desired Courant number if variable dt used, and max to allow without
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.75
    clawdata.cfl_max = 1.0

    # Maximum number of time steps to allow between output times:
    clawdata.max_steps = 50000




    # ------------------
    # Method to be used:
    # ------------------

    # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
    clawdata.order = 2

    # Transverse order for 2d or 3d (not used in 1d):
    clawdata.order_trans = 2

    # Number of waves in the Riemann solution:
    clawdata.mwaves = 3

    # List of limiters to use for each wave family:
    # Required:  len(mthlim) == mwaves
    clawdata.mthlim = [3,3,3]

    # Source terms splitting:
    #   src_split == 0  => no source term (src routine never called)
    #   src_split == 1  => Godunov (1st order) splitting used,
    #   src_split == 2  => Strang (2nd order) splitting used,  not recommended.
    clawdata.src_split = 1


    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.mbc = 2

    # Choice of BCs at xlower and xupper:
    #   0 => user specified (must modify bcN.f to use this option)
    #   1 => extrapolation (non-reflecting outflow)
    #   2 => periodic (must specify this at both boundaries)
    #   3 => solid wall for systems where q(2) is normal velocity

    clawdata.mthbc_xlower = 1
    clawdata.mthbc_xupper = 1

    clawdata.mthbc_ylower = 1
    clawdata.mthbc_yupper = 1


    # ---------------
    # AMR parameters:
    # ---------------


    # max number of refinement levels:
    mxnest = 6 ##

    clawdata.mxnest = -mxnest   # negative ==> anisotropic refinement in x,y,t

    # List of refinement ratios at each level (length at least mxnest-1)
    clawdata.inratx = [4,6,2,10,15]  ##
    clawdata.inraty = [4,6,2,10,15]  ##
    clawdata.inratt = [1,1,1,1,1]  ##


    # Specify type of each aux variable in clawdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    clawdata.auxtype = ['center','capacity','yleft']


    clawdata.tol = -1.0     # negative ==> don't use Richardson estimator
    clawdata.tolsp = 0.5    # used in default flag2refine subroutine
                            # (Not used in geoclaw!)

    clawdata.kcheck = 3     # how often to regrid (every kcheck steps)
    clawdata.ibuff  = 2     # width of buffer zone around flagged points

    clawdata.tchk  = [33000., 35000.]   # when to checkpoint

    # More AMR parameters can be set -- see the defaults in pyclaw/data.py

    return rundata
    # end of function setrun
    # ----------------------


#-------------------
def setgeo(rundata):
#-------------------
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    try:
        geodata = rundata.geodata
    except:
        print "*** Error, this rundata has no geodata attribute"
        raise AttributeError("Missing geodata attribute")

    # == setgeo.data values ==
    geodata.variable_dt_refinement_ratios = True

    geodata.igravity = 1
    geodata.gravity = 9.81
    geodata.icoordsys = 2
    geodata.Rearth = 6367.5e3
    geodata.icoriolis = 0

    # == settsunami.data values ==
    geodata.sealevel = 0.
    geodata.drytolerance = 1.e-3
    geodata.wavetolerance = 1.e-2  ##
    geodata.depthdeep = 1.e2
    geodata.maxleveldeep = 4
    geodata.ifriction = 1
    geodata.coeffmanning =.025
    geodata.frictiondepth = 1.e6

    okushiri_dir = '/Users/FrankGonzalez/daily/modeling/tsunami-benchmarks/github/ \
      FrankGonzalez/geoclaw-group/benchmarks/bp09/bathytoposource' ##
    #honshu_dir = '/bulk/rjl/honshu/' ##
    
    # == settopo.data values ==
    geodata.topofiles = []
    # for topography, append lines of the form
    #   [topotype, minlevel, maxlevel, t1, t2, fname]
    geodata.topofiles.append([3, 1, 1, 0., 1.e10, \
        okushiri_dir + '/AO15.xyz'])  ## Dmitry N.'s version of Kansai U.
    geodata.topofiles.append([3, 1, 1, 0., 1.e10, \
        okushiri_dir + '/MB05.xyz'])  ## Dmitry N.'s version of Kansai U.
    geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
        okushiri_dir + '/M001.xyz'])  ## Dmitry N.'s version of Kansai U.
    geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
        okushiri_dir + '/OK03.xyz'])  ## Dmitry N.'s version of Kansai U.
    geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
        okushiri_dir + '/OK08.xyz'])  ## Dmitry N.'s version of Kansai U.
    geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
        okushiri_dir + '/OK24.xyz'])  ## Dmitry N.'s version of Kansai U.
    geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
        okushiri_dir + '/depth40_138.txt'])  ## JODC 500 m
    geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
        okushiri_dir + '/depth40_140.txt'])  ## JODC 500 m
    geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
        okushiri_dir + '/depth42_138.txt'])  ## JODC 500 m
    geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
        okushiri_dir + '/depth42_140.txt'])  ## JODC 500 m
                              
  # == setdtopo.data values ==
    geodata.dtopofiles = []
    # for moving topography, append lines of the form:  (<= 1 allowed for now!)
    #   [topotype, minlevel,maxlevel,fname]
    geodata.dtopofiles.append([1,2,3, okushiri_dir + '/HNO1993.xyz'])  ## Dmitry N.'s version of Kansai U.

    # == setqinit.data values ==
    geodata.iqinit = 0
    geodata.qinitfiles = []
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [minlev, maxlev, fname]
    #geodata.qinitfiles.append([1, 1, 'hump.xyz'])

    # == setregions.data values ==
    geodata.regions = []
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]
    geodata.regions.append([1, 2, 0., 1e9, 0, 360, -90, 90])  ##
    geodata.regions.append([1, 3, 0., 8000., 0., 360, -90, 90])  ##
    # restrict level 3 to follow closely behind leading wave:
    for t in range(8000,50000,4000):
        xmin = 140. + (t-8000.)/400.
        geodata.regions.append([1, 3, t, t+4000, xmin,360,30,60])  ##
    #geodata.regions.append([1, 3, 21600., 34000, 180,360,30,60])  ##
    #geodata.regions.append([1, 3, 34000., 1e9, 200,360,30,60])  ##
   # geodata.regions.append([3, 4, 34000., 1e9, 235.7,235.9,41.7,41.75])  ##
   # geodata.regions.append([3, 5, 34000., 1e9, 235.7,235.8,41.7,41.8])  ##
   # geodata.regions.append([3, 6, 35000, 1e9, 235.7964,235.8208,41.7333,41.7508])  ##
   # geodata.regions.append([4, 4, 0., 1e9, 235.7,235.9,41.7,41.75])  ##  Force level 4
   # geodata.regions.append([5, 5, 0., 1e9, 235.7,235.8,41.7,41.8])  ## Force level 5
   # geodata.regions.append([6, 6, 0, 1e9, 235.7964,235.8208,41.7333,41.7508])  ## Force level 6
    geodata.regions.append([4, 5, 0., 1e9, 235.,236.,40.,43.])  ##  6-sec grid extent
    geodata.regions.append([5, 6, 0, 1e9, 235.7655,235.8569,41.7165,41.7829])  ## 1-sec grid extent

    # == setgauges.data values ==
    geodata.gauges = []
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]
    
    geodata.gauges.append([19750, 235.817, 41.745, 30000., 1.e10]) ##
    
    ## The next part set up ngauges gauges along a transect between (x1,y1) and (x2,y2):
    from numpy import linspace
    ngauges = 10
    sarray = linspace(0,1,ngauges)
    x1 = 235.82917
    y1 = 41.72083
    x2 = 235.80833
    y2 = 41.74167
    dx = x2 - x1
    dy = y2 - y1
    for gaugeno in range(ngauges):
        s = sarray[gaugeno]
        geodata.gauges.append([gaugeno, x1+s*dx, y1+s*dy, 30000., 1.e10])

    # == setfixedgrids.data values ==
    geodata.fixedgrids = []
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]

    return rundata
    # end of function setgeo
    # ----------------------
    
if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    if len(sys.argv) == 2:
	rundata = setrun(sys.argv[1])
    else:
	rundata = setrun()

    rundata.write()

