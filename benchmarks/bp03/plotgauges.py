#!/usr/bin/python

"""
make plots of gauge data for Benchmark 3-d landslide
"""

import numpy as np
import matplotlib
import gaugedata as gg
import os,string,pylab

figure= matplotlib.pyplot.figure
pp =  matplotlib.pyplot
plot = matplotlib.pyplot.plot

datadir = '_output/'
datafile = datadir+'fort.gauge'
sgfile = datadir+'setgauges.data'

gauges = [1,2,12,13]
data={}

dfile={}
dfile[1] = 'Delta_0025_WaveGage_1.txt'
dfile[2] = 'Delta_0025_WaveGage_2.txt'
dfile[12] = 'Delta_0025_RunupGage_2.txt'
dfile[13] = 'Delta_0025_RunupGage_3.txt'

axlimits = [0,10.,-.2,.2]

titlestr={}
titlestr[1] =  'Case 1: Wave Gage 1'
titlestr[2] =  'Case 1: Wave Gage 2'
titlestr[12] = 'Case 1: Runup Gage 2'
titlestr[13] = 'Case 1: Runup Gage 3'

fntsize = 20
for gauge in gauges:
    data[gauge]=gg.selectgauge(gauge,datafile=datafile,setgaugefile=sgfile)
    figure(gauge,figsize=(14,6))
    plot(data[gauge]['t'][0:-1],data[gauge]['q4'][0:-1],color='r',linestyle='-', label='GeoClaw')
    ts = np.loadtxt(dfile[gauge])
    plot(ts[:,0],ts[:,-1],color='b',linestyle='-',label='Wave Gage Data')
    gkey=gauge
    pylab.title(titlestr[gkey],fontsize=fntsize+2)
    pylab.xticks(range(0,10),fontsize=fntsize-2)
    pylab.yticks(range(-2,2),fontsize=fntsize-2)
    pylab.xlabel('Time (s)',fontsize=fntsize-2)
    pylab.ylabel('Water surface (m)',fontsize=fntsize-2)
    pylab.legend()
    pylab.axis([0.0,10.0,-.05, .05],'tight')
    pylab.savefig('gauge_'+str(gkey)+'.png',format='png')


matplotlib.pyplot.show()