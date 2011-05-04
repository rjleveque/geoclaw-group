begin_html  [use: doc/doc.css] [use:jsMath]
<!--   For a more readable version of this file, execute
                  unix>  make htmls
       in this directory and then point your browser to README.html 
     --------------------------------------------------------------  -->

<h2>
Monai Valley Wave Tank Benchmark
</h2>

This is a test of the wave tank experiment summarized at the 

<b>benchmark site</b>:
[http://nctr.pmel.noaa.gov/benchmark/Laboratory/Laboratory_MonaiValley/index.html]

The bathymetry is downloaded from that site and put into the form needed by
GeoClaw by the function maketopo in [code: maketopo.py].

The initial data is taken to be stationary water with surface $\eta = 0$ over
the domain shown in Figure 2 on the benchmark site.  The surface and velocity
are set in ghost cells in such a way that a pure incoming wave is generated
with this surface elevation.

The local routine [code: bc2amr_geo.f] implements boundary conditions so that the
depth at $x=0$ agrees with the gauge data shown in Figure 3 on the benchmark
site.  This data  is in [link: wave.txt].


The results are compared against the gauge data shown in Figure 4 on the
benchmark site.  
This data has been converted from the Excel spreadsheet provided on the
benchmark site to the ASCII file [link: WaveGages.txt].


To run the code, see [link: #instructions Instructions]

<h4>
Plots of results
</h4>
After running this code and creating plots via "make .plots", you should be
able to view the plots in [link: _plots/_PlotIndex.html].


<h4>
Fortran files
</h4>


<dl>
<dt>[code: Makefile]
<dd> Determines which version of fortran files
are used when compiling the code with make and specifies where output and
plots should be directed.  Type "make .help" at the Unix prompt for options.


<dt>[code: setprob_geo.f]
<dd>
Modified version of the library routine that reads in the data needed for the
boundary conditions.


<dt>[code: bc2amr_geo.f]
<dd>
Modified version of the library routine that reads sets the inflow boundary
conditions at $x=0$ up to time $t=22$ and then switches to nonreflecting
boundary conditions (extrapolation).

</dl>

<h4>
Python files
</h4>
<dl>

<dt>[code: maketopo.py]
<dd> Used to download and create topo file.

<dt>[code: setrun.py]
<dd> This file contains a function that 
specifies what run-time parameters will be used.

<dt>[code: setplot.py]
<dd> This file contains a function that 
specifies what plots will be done and
sets various plotting parameters. 

</dl>


<h4>
Data files
</h4>

The .data files are automatically generated using the information in 
[code: setrun.py].


[name:  instructions]
<h4>
Instructions
</h4>


To make topo and qinit data files:
{{{
  $ make topo
}}}

To make all data files, edit setrun.py and then
{{{
  $ make .data
}}}

To run code:

You may need to type
{{{
  $ make new 
}}}
to make sure the modules are accessible.

Then run the code with
{{{
  $ make .output
}}}

To plot results, either generate html pages via:
{{{
  $ make .plots
}}}
or view interactively using ipython and Iplotclaw.

end_html

