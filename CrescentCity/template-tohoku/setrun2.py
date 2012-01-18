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
    clawdata.xlower = 132.
    clawdata.xupper = 238.

    clawdata.ylower = 30
    clawdata.yupper = 50.


    # Number of grid cells:
    clawdata.mx = 53
    clawdata.my = 10


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

    clawdata.restart = True
    clawdata.outstyle = 2

    if clawdata.outstyle==1:
        # Output nout frames at equally spaced times up to tfinal:
        clawdata.nout = 5
        clawdata.tfinal = 120.
        #clawdata.nout = 28
        #clawdata.tfinal = 14.*3600.

    elif clawdata.outstyle == 2:
        # Specify a list of output times.
        from numpy import arange, linspace
        #clawdata.tout = list(linspace(100,200,3))
        clawdata.tout = list(linspace(3600,3600*9,9)) + \
                 list(linspace(3600*9.5,3600*11.5,25))
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
    clawdata.verbosity = 2



    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==1: variable time steps used based on cfl_desired,
    # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
    clawdata.dt_variable = 1

    # Initial time step for variable dt.
    # If dt_variable==0 then dt=dt_initial for all steps:
    clawdata.dt_initial = 1

    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99

    # Desired Courant number if variable dt used, and max to allow without
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.75
    clawdata.cfl_max = 1.0

    # Maximum number of time steps to allow between output times:
    clawdata.max_steps = 5000




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
    mxnest = 6

    clawdata.mxnest = -mxnest   # negative ==> anisotropic refinement in x,y,t

    # List of refinement ratios at each level (length at least mxnest-1)
    clawdata.inratx = [4,4,5,5,54]
    clawdata.inraty = [4,4,5,5,54]
    clawdata.inratt = [4,4,5,2,4]


    # Specify type of each aux variable in clawdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    clawdata.auxtype = ['center','capacity','yleft']


    clawdata.tol = -1.0     # negative ==> don't use Richardson estimator
    clawdata.tolsp = 0.5    # used in default flag2refine subroutine
                            # (Not used in geoclaw!)

    clawdata.kcheck = 3     # how often to regrid (every kcheck steps)
    clawdata.ibuff  = 2     # width of buffer zone around flagged points

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
    geodata.wavetolerance = 2.e-2
    geodata.depthdeep = 1.e2
    geodata.maxleveldeep = 4
    geodata.ifriction = 1
    geodata.coeffmanning =.025
    geodata.frictiondepth = 100.

# Topography/Bathymetry
    # == settopo.data values ==
    geodata.topofiles = []
    # for topography, append lines of the form
    #    [topotype, minlevel, maxlevel, t1, t2, fname]

    import os
    homedir = os.environ['HOME']
    honshu_dir = homedir + '/svn/tsunami-benchmarks/honshu'
    geodata.topofiles.append([3, 1, 1, 0., 1.e10, \
                              honshu_dir + '/topo/etopo1min139E147E34N41N.asc'])
    geodata.topofiles.append([3, 1, 1, 0., 1.e10, \
                              honshu_dir + '/topo/etopo4min120E72W40S60N.asc']) 

    geodata.topofiles.append([-3, 1, 1, 32000, 1.e10, \
                              honshu_dir + '/topo/ca_north36secm.asc'])  
    geodata.topofiles.append([-3, 1, 1, 32000, 1.e10, '../CC/cc-1sec-c.asc'])
    geodata.topofiles.append([-3, 1, 1, 32000, 1.e10, '../CC/cc-1_3sec-c.asc'])


    # Earthquake from my deformation files
    # == setdtopo.data values ==
    geodata.dtopofiles = []
    # for moving topography, append lines of the form :   (<= 1 allowed for now!)
    #    [minlevel, maxlevel, fname]
    dtopodir = honshu_dir + '/sources'
    #dtopofname = open('dtopofname.txt','r').read().strip()
    #fname = dtopodir + '/honshu-ucsb3.tt1'
    fname = '/home/tohoku/sources/Fujii.txydz'
    print 'dtopo file: ',fname
    geodata.dtopofiles.append([1,3,3,fname])

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
    geodata.regions.append([1, 1, 0., 1e9, 0, 360, -90, 90]) #whole world
    geodata.regions.append([3, 3, 0., 1800, 140, 146, 30, 42]) #earthquake source
    geodata.regions.append([1, 3, 0, 7200, 140, 245, 25, 50]) 
    geodata.regions.append([1, 3, 0, 15000, 155, 245, 25, 50]) 
    geodata.regions.append([1, 3, 15000, 21000, 170, 245, 25, 50]) 
    geodata.regions.append([1, 3, 21000, 27000, 180, 245, 25, 50]) 
    geodata.regions.append([1, 3, 27000, 1e9, 200, 245, 25, 50]) 
    geodata.regions.append([2, 4, 27000, 33000., 200, 245, 35, 43]) 
    geodata.regions.append([2, 4, 33000, 1e9, 228, 236, 39, 42]) 
    #geodata.regions.append([2, 4, 33000, 1e9, 230, 245, 35, 43]) 
    #geodata.regions.append([4, 4, 33000, 1e9, 235, 236, 41, 42]) 

#    geodata.regions.append([3, 4, 33000., 1e9, 228, 238, 41, 42]) # between shelf and CC
#    geodata.regions.append([4, 4, 33000., 1e9, 235, 236, 41, 42]) #CC_B6s04-5853 data 
    geodata.regions.append([5, 5, 33000., 1e9, 235.5,235.83,41.6,41.8]) #only harbor 
    geodata.regions.append([6, 6, 35000., 1e9, 235.795116,235.826887,41.734963,41.752605]) #only harbor 

    
 # == setgauges.data values ==
    geodata.gauges = []
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]
    if 1:
        geodata.gauges.append([19750, 235.8162, 41.745616, 33000., 1.e10]) ##tide gauge E
        geodata.gauges.append([197501, 235.81581, 41.745928, 33000., 1.e10]) ##tide gauge W
    if 0:
        geodata.gauges.append([14, 235.8026, 41.7473, 33000., 1.e10]) ##
        geodata.gauges.append([13, 235.794395, 41.747373, 33000., 1.e10]) ##
        geodata.gauges.append([12, 235.786731, 41.749752, 33000., 1.e10]) ##
        geodata.gauges.append([11, 235.782618, 41.752068, 33000., 1.e10]) ##
        geodata.gauges.append([15, 235.810934, 41.749294, 33000., 1.e10]) ##
        geodata.gauges.append([16, 235.821507, 41.745058, 33000., 1.e10]) ##
        geodata.gauges.append([19, 235.836509, 41.737021, 33000., 1.e10]) ##
        geodata.gauges.append([17, 235.8366, 41.7373, 33000., 1.e10]) ##
        geodata.gauges.append([18, 235.832411, 41.741187, 33000., 1.e10]) ##
        geodata.gauges.append([20, 235.839508, 41.73508, 33000., 1.e10]) ##
        geodata.gauges.append([10, 235.776861, 41.7756324, 33000., 1.e10]) ##
        geodata.gauges.append([9, 235.773796, 41.761252, 33000., 1.e10]) ##
        geodata.gauges.append([8, 235.768043, 41.7646, 33000., 1.e10]) ##

   ## The next part set up ngauges gauges along a transect between (x1,y1) and (x2,y2):
    if 1:
        from numpy import linspace
        ngauges = 8
        sarray = linspace(0,1,ngauges)
        x1 = 235
        y1 = 37.
        x2 = 235
        y2 = 44.
        dx = x2 - x1
        dy = y2 - y1
        for gaugeno in range(ngauges):
            s = sarray[gaugeno]
            geodata.gauges.append([gaugeno, x1+s*dx, y1+s*dy, 32000., 1.e10])


    # == setfixedgrids.data values ==
    geodata.fixedgrids = []
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]
    geodata.fixedgrids.append([9.5*3600.,11.5*3600., 121, 235.8,235.82,\
       41.735,41.755,217,217,0,1])
    

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

