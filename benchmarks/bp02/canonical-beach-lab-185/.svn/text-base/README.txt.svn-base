begin_html  [use: doc/doc.css] [use:jsMath]
<!--   For a more readable version of this file, execute
                  unix>  make htmls
       in this directory and then point your browser to README.html 
     --------------------------------------------------------------  -->

<h2>
Solitary Wave on Canonical Bathymetry Benchmark
</h2>

This is a test of the wave tank experiment summarized at the 

<b>benchmark site</b>:
[http://nctr.pmel.noaa.gov/benchmark/Laboratory/Laboratory_CanonicalBathymetry/index.html]

The bathymetry and initial wave are created by [code: maketopo.py].


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

To make all the plots shown in the benchmarks workshop, you first need to run the
code with mx = 150, 300, 600, 1200 and move outputs to _output_300 etc.  

end_html

