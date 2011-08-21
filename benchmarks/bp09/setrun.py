## Randy:  This run took about 4 hours, as it is set up now.

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
    clawdata.restart = False   # Turn restart switch on or off

    # Set single grid parameters first.
    # See below for AMR parameters.

    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.ndim = ndim

    # Lower and upper edge of computational domain:
    # clawdata.xlower = 137.57  ##
    # clawdata.xupper = 141.41  ##
    # clawdata.ylower = 39.67  ##
    # clawdata.yupper = 44.15  ##
    
    # For OK08 grid:
    # clawdata.xlower = 138.5015  ##
    # clawdata.xupper = 140.541  ##
    # clawdata.ylower = 40.5215  ##
    # clawdata.yupper = 43.2988  ##
    
    clawdata.xlower = 139.  ##
    clawdata.xupper = 140. ##
    clawdata.ylower = 41.6  ##
    clawdata.yupper = 42.6  ##
    
    # # Number of grid cells:
    # clawdata.mx = 36  ##  3.84 deg/36 cells = 384 sec/cell = 16*24 sec/cell
    # clawdata.my = 42  ##  4.48 deg/42 cells = 384 sec/cell = 16*24 sec/cell
    # clawdata.mx = 576  ##  3.84 deg/576 cells = 24 sec/cell
    # clawdata.my = 672  ##  4.48 deg/672 cells = 24 sec/cell
    # clawdata.mx = 84  ##  8*24 sec/cell
    # clawdata.my = 72  ##  8*24 sec/cell
    clawdata.mx = 60  
    clawdata.my = 60  


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
        # Note:  Frame time intervals = (tfinal-t0)/nout
        clawdata.nout = 16 ## Number of frames (plus the t = 0.0 frame)
        clawdata.tfinal = 16.*60  ## End run time in Seconds
                
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

    clawdata.mthbc_xlower = 1  # Open Left BC
    clawdata.mthbc_xupper = 1  # Open Right BC

    clawdata.mthbc_ylower = 1  # Open Bottom BC
    clawdata.mthbc_yupper = 1  # Open Top BC

    # ---------------
    # AMR parameters:
    # ---------------

    # max number of refinement levels:
    mxnest = 5 ## 

    clawdata.mxnest = -mxnest   # negative ==> anisotropic refinement in x,y,t

    # List of refinement ratios at each level (length at least mxnest-1)
            ## Levels  2 3 4 5
    clawdata.inratx = [2,4,4,12] ## 
    clawdata.inraty = [2,4,4,12] ## 
    clawdata.inratt = [1,1,1,1] ##

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
    geodata.variable_dt_refinement_ratios = True  ## Overrides clawdata.inratt, above

    geodata.igravity = 1
    geodata.gravity = 9.81
    geodata.icoordsys = 2
    geodata.Rearth = 6367.5e3
    geodata.icoriolis = 0

    # == settsunami.data values ==
    geodata.sealevel = 0.
    geodata.drytolerance = 1.e-3
    geodata.wavetolerance = 1.e-2  ##
    geodata.depthdeep = 1.e6  ## Definition of "deep" water
    geodata.maxleveldeep = 10  ## Restriction on the number of deep water levels
    geodata.ifriction = 0 ## Friction switch.  0=off,  1=on
    geodata.coeffmanning =0.0
    # geodata.coeffmanning =.025
    geodata.frictiondepth = 1.e6  ## Apply friction at all depths

    #okushiri_dir = '/Users/FrankGonzalez/daily/modeling/tsunami-benchmarks/github/' \
      #+ 'FrankGonzalez/geoclaw-group/benchmarks/bp09' ##
    okushiri_dir = '../bp09'  ## this directory
    
    # == settopo.data values ==
    geodata.topofiles = []
    # for topography, append lines of the form
    #   [topotype, minlevel, maxlevel, t1, t2, fname]
    # geodata.topofiles.append([1, 1, 1, 0, 1.e10, \
    #     okushiri_dir + '/OK24.tt1'])  ## 24-s, ~550-740 m Entire Domain (Dmitry's version of Kansai U.)
    geodata.topofiles.append([1, 1, 1, 0, 1.e10, \
        okushiri_dir + '/OK08.tt1'])  ## 8-s, ~184-247 m Okushiri (Dmitry's version of Kansai U.)
    geodata.topofiles.append([1, 1, 1, 0, 1.e10, \
        okushiri_dir + '/OK03.tt1'])  ## 2.67 s (8/3s), ~61-82 m Okushiri (Dmitry's version of Kansai U.)
    geodata.topofiles.append([1, 1, 1, 0., 1.e10, \
        okushiri_dir + '/AO15.tt1'])  ## 0.53-0.89 s, ~16.5-20.4 m, Aonae (Dmitry's version of Kansai U.)
    # geodata.topofiles.append([1, 1, 1, 0, 1.e10, \
    #     okushiri_dir + '/MO01.tt1'])  ## 0.89 s, ~20-27 m, Monai (Dmitry's version of Kansai U.)
    # geodata.topofiles.append([1, 1, 1, 0., 1.e10, \
    #     okushiri_dir + '/MB05.tt1'])  ## 0.13-0.18 s, ~4 m Monai (Dmitry's version of Kansai U.)

    # geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
    #     okushiri_dir + '/depth40_138.txt'])  ## JODC 500 m
    # geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
    #     okushiri_dir + '/depth40_140.txt'])  ## JODC 500 m
    # geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
    #     okushiri_dir + '/depth42_138.txt'])  ## JODC 500 m
    # geodata.topofiles.append([-3, 1, 1, 0, 1.e10, \
    #     okushiri_dir + '/depth42_140.txt'])  ## JODC 500 m
                              
  # == setdtopo.data values ==
    geodata.dtopofiles = []
    # for moving topography, append lines of the form:  (<= 1 allowed for now!)
    #   [topotype, minlevel,maxlevel,fname]
    geodata.dtopofiles.append([1,2,3, okushiri_dir + '/HNO1993.txyz'])  ## Dmitry N.'s version of Kansai U.

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
    # Note:  Level 1 = 24 s & Levels [2,3,4,5] = RF [3,3,3,8] => Res of 8 sec to 8/3 sec to 8/9 to 1/9 sec/cell
    # Grid Limits
    #     Name    x1              x2              y1              y2
    #     OK24  137.53666670    141.53000000    39.53666670     44.26333330
    #     HNO   138.50000000    140.55000000    40.51666670     43.30000000
    #     OK08  138.50111110    140.55222220    40.52111110     43.29888890
    #     OK03  139.38925930    139.66407410    41.99592590     42.27074070
    #     AO15  139.43419750    139.49987650    42.03118520     42.07251850
    #     MO01  139.41123460    139.43320990    42.07790120     42.14580250
    #     MB05  139.41385190    139.42639510    42.09458550     42.10343920
        
    #geodata.regions.append([1, 1, 0., 1e9,   0.0,  360.0, -90.0,  90.0])  ## OK24: 24-s, ~550-740 m Entire Domain
    geodata.regions.append([1, 2, 0., 1e9, 138.5,  139.7,  41.4,  43.3])  ## OK08: 8-s, ~184-247 m Okushiri 
    geodata.regions.append([1, 3, 0., 1e9, 139.39, 139.6,  42.0,  42.25])  ## OK03: 2.67 s (8/3s), ~61-82 m Okushiri 
    # geodata.regions.append([1, 4, 0., 1e9, 139.42, 139.57, 42.03, 42.23])  ## AO15: 0.53-8/9 s, ~16.5-20.4 m, Aonae 
    geodata.regions.append([1, 4, 0., 1e9, 139.41, 139.49, 42.02, 42.08])  ## 
    
    geodata.regions.append([5, 5, 180., 1e9, 139.44,139.46,42.035,42.055])  ## Aonae 
    # geodata.regions.append([4, 4, 0., 1e9, 139.41, 139.43, 42.08, 42.15])  ## MO01: 8/9 s, ~20-27 m, Monai 
    # geodata.regions.append([5, 5, 0., 1e9, 139.41, 139.43, 42.095, 42.100])  ## MB05: 0.13-0.18 s, ~4 m Monai
    # geodata.regions.append([3,3, 0., 1e9, 139.40662684821325, 139.41794012636134, \
    #     42.158684332627985, 42.16622651806005])  ## Station 800
    # geodata.regions.append([5, 5, 0., 1e9, 139.42059926730784, 139.42538420014014, \
    #         42.098398121038485,42.101829739534381])  ## Runup Monai Valley
    #     geodata.regions.append([4, 4, 0., 1e9, 139.41999842833241,139.42598037189106, \
    #         42.103348313934944, 42.112653559470658])  ## Runup Tsuji Valley Tight
    #     MO01  139.41123460    139.43320990    42.07790120     42.14580250
    #     MB05  139.41385190    139.42639510    42.09458550     42.10343920

    # == setgauges.data values ==
    geodata.gauges = []
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]
    
    if 0:
        geodata.gauges.append([100,139.451539852594,42.044696547058,0.0,1e9]) ## Runup
        geodata.gauges.append([200,139.427853421935,42.065461519438,0.0,1e9]) ## Runup
        geodata.gauges.append([300,139.428901803617,42.076636582137,0.0,1e9]) ## Runup
        geodata.gauges.append([400,139.428035766149,42.093012384481,0.0,1e9]) ## Runup
        geodata.gauges.append([500,139.423714744650,42.100414145210,0.0,1e9]) ## Runup Monai
        geodata.gauges.append([600,139.426244998662,42.116554785296,0.0,1e9]) ## Runup
        geodata.gauges.append([700,139.418261206409,42.137404393442,0.0,1e9]) ## Runup
        geodata.gauges.append([800,139.411185686023,42.162762869034,0.0,1e9]) ## Runup
        # geodata.gauges.append([900,139.411185686023,42.162762869034,0.0,1e9]) ## Runup
        geodata.gauges.append([1000,139.429211710298,42.188181491811,0.0,1e9]) ## Runup
        # geodata.gauges.append([1100,139.429211710298,42.188181491811,0.0,1e9]) ## Runup
        geodata.gauges.append([1200,139.515046095129,42.215249086323,0.0,1e9]) ## Runup
        # geodata.gauges.append([1300,139.515046095129,42.215249086323,0.0,1e9]) ## Runup
        geodata.gauges.append([1400,139.554549379772,42.226981643110,0.0,1e9]) ## Runup
        # geodata.gauges.append([1500,139.554549379772,42.226981643110,0.0,1e9]) ## Runup
        geodata.gauges.append([1600,139.562524223190,42.211983687588,0.0,1e9]) ## Runup
        geodata.gauges.append([1700,139.547459850688,42.187448788669,0.0,1e9]) ## Runup
        geodata.gauges.append([1800,139.525898248343,42.171012210670,0.0,1e9]) ## Runup
        geodata.gauges.append([1900,139.521076578103,42.151376349400,0.0,1e9]) ## Runup
        # geodata.gauges.append([2000,139.521076578103,42.151376349400,0.0,1e9]) ## Runup
        geodata.gauges.append([2100,139.519099729509,42.113058045853,0.0,1e9]) ## Runup
        geodata.gauges.append([2200,139.493430734366,42.064501276365,0.0,1e9]) ## Runup
        geodata.gauges.append([2300,139.472013750592,42.058089880433,0.0,1e9]) ## Runup
        # geodata.gauges.append([2400,139.472013750592,42.058089880433,0.0,1e9]) ## Runup
        geodata.gauges.append([2500,139.456528443496,42.051692262353,0.0,1e9]) ## Runup
        # geodata.gauges.append([2600,139.456528443496,42.051692262353,0.0,1e9]) ## Runup
        geodata.gauges.append([5000,140.135000000000,41.867800000000,0.0,1e9]) ## Esashi TG
        geodata.gauges.append([6000,140.517500000000,42.984170000000,0.0,1e9]) ## Iwanai TG
        # geodata.gauges.append([7000,139.473888900000,42.068055600000,0.0,1e9]) ## Hamatsumae
        #     geodata.gauges.append([7100,139.42245953503144,42.103439671366239,0.0,1e9]) ## Runup Tsuji Valley
        #     geodata.gauges.append([7200,139.442222200000,42.054722200000,0.0,1e9]) ## Aonae
        #     geodata.gauges.append([7101,139.42294955819352, 42.103439671366239,390.0,1e9])## Tsuji V.
        #     geodata.gauges.append([7102,139.4226863452661, 42.103439671366239,0.0,1e9])## Tsuji V.
        #     geodata.gauges.append([7103,139.42321658580107, 42.103439671366239,0.0,1e9])## Tsuji V.
        #     geodata.gauges.append([7104,139.4233768023656, 42.103439671366239,0.0,1e9])## Tsuji V.
        #     geodata.gauges.append([7105,139.42220951025263, 42.103439671366239,0.0,1e9])## Tsuji V.

        ## The next part set up ngauges gauges along a transect between (x1,y1) and (x2,y2):
        # from numpy import linspace
        # ngauges = 10
        # sarray = linspace(0,1,ngauges)
        # x1 = 235.82917
        # y1 = 41.72083
        # x2 = 235.80833
        # y2 = 41.74167
        # dx = x2 - x1
        # dy = y2 - y1
        # for gaugeno in range(ngauges):
        #     s = sarray[gaugeno]
        #     geodata.gauges.append([gaugeno, x1+s*dx, y1+s*dy, 30000., 1.e10])

        from numpy import linspace

        gaugeno = 500 # Monai Runup
        nxgauges = 5
        nygauges = 5
        xgauges = linspace(139.42309065950826,139.42416180042954, nxgauges) # Monai Runup
        ygauges = linspace(42.099625599311729,42.100760429693182, nygauges) # Monai Runup
        for j in range(nygauges):
            for i in range(nxgauges):
                gaugeno = gaugeno + 1
                geodata.gauges.append([gaugeno, xgauges[i], ygauges[j], 0., 1.e10])

        gaugeno = 7100 # Tsuji Valley Runup
        nxgauges = 5
        nygauges = 5
        xgauges = linspace(139.41999842833241,139.42598037189106, nxgauges) # Tsuji Valley Runup
        ygauges = linspace(42.103348313934944, 42.112653559470658, nygauges) # Tsuji Valley Runup
        for j in range(nygauges):
            for i in range(nxgauges):
                gaugeno = gaugeno + 1
                geodata.gauges.append([gaugeno, xgauges[i], ygauges[j], 0., 1.e10])
            
        gaugeno = 800
        nxgauges = 7
        nygauges = 1
        xgauges = linspace(139.40865662629733,139.41321964848373, nxgauges) # Station 800
        ygauges = linspace(42.162762869034,42.162762869034, nygauges) # Station 800
        for j in range(nygauges):
            for i in range(nxgauges):
                gaugeno = gaugeno + 1
                geodata.gauges.append([gaugeno, xgauges[i], ygauges[j], 0., 1.e10])
  
    # == setfixedgrids.data values ==

    geodata.fixedgrids = []
# for fixed grids append lines of the form
# [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,ioutarrivaltimes,ioutsurfacemax]
    # set t1, t2 to the start and end times of the data collection
    # set noutput to the number of sample times
    #    * note that the sampling interval will be Dt = (t2-t1)/(noutput-1)
    # set x1, x2, y1, y2 to the lower left and upper right lat/long pairs
    # set xpoints, ypoints to the number of samples in the x & y directions
    # set iout* to 1 to output arrival time and/or surface max
    # at each output time, fixed grid output has columns for:
    # h, hu, hv, B, arrivaltime, surfacemax  
    # (max seen so far)  _output/fort.fg01_0001, ... fort.fgMM_NNNN.  M=grid number, N=time

    # geodata.fixedgrids.append([0.0,1200.0,5,139.42309065950826,139.42416180042954, \
    #     42.099625599311729,42.100760429693182,40,40,0,1]) ## Sta 500 Monae Runup
    
    # geodata.fixedgrids.append([0.0,21*60.,5,139.43,139.48, \
    #     42.035,42.065,22,34,0,1]) ## Aonae Peninsula Runup
    
    # geodata.fixedgrids.append([180.0,8*60.,14,139.42,139.48, \
    #         42.02,42.08,200,200,0,1]) ## Aonae Peninsula Runup
    geodata.fixedgrids.append([180.0,16*60.,27,139.44,139.46,42.035,42.055,200,200,0,1]) ## Aonae Peninsula Runup
            
        
    # geodata.fixedgrids.append([0.0,1200.0,5,139.41999842833241,139.42598037189106, \
    #     42.103348313934944, 42.112653559470658,215,335,0,1]) ## Tsuji Valley Runup
    
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
