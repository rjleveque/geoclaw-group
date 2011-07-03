#! /usr/bin/python

"""
Run several tests with different parameters, in this case different
values of d.
"""

from setrun import setrun
from setplot import setplot
from pyclaw.runclaw import runclaw
from pyclaw.plotters.plotclaw import plotclaw

for n in [1,2,4]:
    for d in [0.061, 0.080, 0.100, 0.120, 0.140, 0.149, 0.189]:
        rundata = setrun(d_param=d)
        mx = 72*n
        my = 18*n
        rundata.clawdata.mx = mx
        rundata.clawdata.my = my
        rundata.write()

        runclaw(xclawcmd = "xgeoclaw", outdir="_output_%s_my%s" % (d,my))

        setplot.d = d
        setplot.my = my
        plotclaw(outdir="_output_%s_my%s" % (d,my), \
                 plotdir="_plots_%s_my%s" % (d,my),\
                 setplot=setplot)


