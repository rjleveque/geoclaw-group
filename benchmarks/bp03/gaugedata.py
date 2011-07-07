#!/usr/bin/python
"""
gaugedata
=========
   Provides routines for analyzing gauge data
   as output from Geoclaw files: fort.gauge.

   see:
      gaugedata.fortgaugeread
      gaugedata.plotgauge
      gaugedata.plotfortgauge
      gaugedata.writegdata
      gaugedata.readgdata
      gaugedata.fortgauge2gdata
      gaugedata.samplesinglegauge
"""

from numpy import *
from scipy import *
from matplotlib import *
import matplotlib.mlab as mlab
import matplotlib.pyplot as pyplot
import os
import string

from datatools import *


#========================================================================
def fortgaugeread (datafile="fort.gauge",setgaugefile="setgauges.data"):
    """
    fortgaugeread (datafile="fort.gauge",setgaugefile="setgauges.data"):
    Read data from fort.gauge files output by GeoClaw.

    Reads the gauge data and returns a list of dictionaries, with mgauge elements.
    Each element of the list is a dictionary containing the data for a particular gauge.
    Each dictionary has keys for each variable: t,h,hu,hv,eta,x,y,gauge.

    example:

    for N gauges: allgaugedata=[dictionary_1,...,dictionary_N] where
    dictionary_n = {'t': (one-dimensional numpy array), 'h': (one-dimensional numpy array), ...,}
    """

    fid=open(setgaugefile)
    inp='#'
    while inp == '#':
        inpl=fid.readline()
        inp=inpl[0]

    inp = fid.readline()
    mgauges=int(inp.split()[0])
    gaugelocs=[]
    linesread=0
    while linesread < mgauges :
        row=string.split(fid.readline())
        if row!=[]:
           gaugelocs.append(row)
           linesread=linesread+1

    fid.close()

    data=loadtxt(datafile)

    allgaugedata=[]
    for n in xrange(mgauges) :
        dict={}
        dict['gauge']=int(gaugelocs[n][0])
        dict['x']=float(gaugelocs[n][1])
        dict['y']=float(gaugelocs[n][2])
        onegaugedata=data[mlab.find(data[:,0]==dict['gauge'])]
        dict['level']=onegaugedata[:,1]
        dict['t']=onegaugedata[:,2]
        dict['mq'] = len(onegaugedata[0])-2
        for m in xrange(1, dict['mq']) :
            dict['q'+str(m)]=onegaugedata[:,2 + m]

        allgaugedata.append(dict)
    return allgaugedata
    # end fortgaugeread ======================================================

#=============================================================================
def plotfortgauge (gaugenumber, allgaugedata=[],gaugevar1='t',gaugevar2='q1',\
                   datafile="fort.gauge",setgaugefile="setgauges.data"):
    """
    plot the data output in fort.gauge files output by GeoClaw
    """

    if allgaugedata==[]:
        allgaugedata=fortgaugeread(datafile,setgaugefile)
    for g in xrange(len(allgaugedata)):
        gnumber == allgaugedata[g]['gauge']
        if gnumber==gaugenumber:
            gg = g
    try:
        plotdata = allgaugedata[gg]
    except:
        print 'Gauge number %i does not exist in %s' % (gaugenumber,datafile)

    plotdata1=plotdata[gaugevar1]

    if gaugevar2=='b':
        plotdata2=plotdata['q4']-plotdata['q1']
    elif gaugevar2=='eta':
        plotdata2=plotdata['q4']
    else:
        plotdata2=plotdata[gaugevar2]

    lines=pyplot.plot(plotdata1,plotdata2)
    return lines

#=============================================================================
def selectgauge (gaugenumber, allgaugedata=[], datafile="fort.gauge", \
    setgaugefile="setgauges.data"):
    """
    select a single in fort.gauge files output by GeoClaw
    """

    if allgaugedata==[]:
        allgaugedata=fortgaugeread(datafile,setgaugefile)
    for g in xrange(len(allgaugedata)):
        gnumber = allgaugedata[g]['gauge']
        if gnumber==gaugenumber:
            gg = g
    try:
        gaugedata = allgaugedata[gg]
    except:
        print 'Gauge number %i does not exist in %s' % (gaugenumber,datafile)

    return gaugedata

#=====================================================================================
def plotgauge (ingauge,var1='t',var2='q1'):

    """
    plot the gauge data in ingauge.
    indata may be a file name for a .gdata file or a gaugedata dictionary
    """

    if type(ingauge)==str:
        gaugedata=readgdata(ingauge)
    else:
        gaugedata=ingauge
    handle=pyplot.plot(gaugedata[var1],gaugedata[var2])
    return handle

#====================================================================================
def writegdata (gaugedata,fname=''):

    """
    given dictionary gaugedata for data at a single gauge write a file in .gdata format
        ie. with header:
         int 'gauge#'
         float 'x'
         float 'y'
         't,h,hu,hv,eta,b'
    """

    dict=gaugedata

    if fname=='':
        fname= '%s%03i.%s' % ('gauge',dict['gauge'],'gdata')
        #fname='gauge'+str(dict['gauge'])+'.gdata'

    fid=open(fname,'w')
    keystrlist=['gauge','x','y']
    varstrlist=['t','h','hu','hv','eta','b']

    for stri in keystrlist:
        fid.write("%s %s \n" % (dict[stri],stri))
    sep='   '
    fid.write(sep.join(varstrlist))
    fid.write('\n')

    for tp in xrange(len(dict['t'])):
        fid.write(" %012.6e %012.6e %012.6e %012.6e %012.6e %012.6e \n" % (dict['t'][tp],dict['h'][tp],dict['hu'][tp],dict['hv'][tp],dict['eta'][tp],dict['b'][tp]))

    fid.close()
    return

#=====================================================================================
def readgdata (fname):

    """
    read the data from a file containing gauge data in the .gdata format
        ie. with header:
         int 'gauge#'
         float 'x'
         float 'y'
         't,h,hu,hv,eta,b'
    """

    gaugedata={}
    fid=open(fname,'r')

    row = string.split(fid.readline())
    gaugedata['gauge'] = int(row[0])
    row = string.split(fid.readline())
    gaugedata['x'] = float(row[0])
    row = string.split(fid.readline())
    gaugedata['y'] = float(row[0])
    row = string.split(fid.readline())

    fid.close()

    data=iotools.datafile2array(fname,skiplines=4)
    keylist=['t','h','hu','hv','eta','b']
    for i in xrange(len(keylist)) :
        gaugedata[keylist[i]]=data[:,i]

    fid.close()
    return gaugedata


#================================================================================
def fortgauge2gdata (indatafile="fort.gauge",setgaugefile="setgauges.data"):

    """
    write out data in fort.gauge into separate files in the .gdata format
        ie. with headers:
         int 'gauge#'
         float 'x'
         float 'y'
         't,h,hu,hv,eta,b'
    """

    allgaugedata = fortgaugeread (indatafile,setgaugefile)

    N=len(allgaugedata)

    for ig in xrange(N):
        writegdata(allgaugedata[ig])
    return

#================================================================================
def samplesinglegauge (ingauge,ntimes,t0=-inf,tend=+inf,output=True,outname=''):

    """
    subsample the data in ingauge to return a new dictionary
    with output only at ntimes equally spaced points between t0 and tend
    data is linearly interpolated to times.
    ingauge may be a dictionary of gauge data, or an input file name for a .gdata file
    if output is True, a new file is written.
    """

    if type(ingauge)==str:
        gaugedata=readgdata(ingauge)
    else:
        gaugedata=ingauge

    sampledat={}
    sampledat['gauge']=gaugedata['gauge']
    sampledat['x']=gaugedata['x']
    sampledat['y']=gaugedata['y']

    sampledat['t']=[]
    keylist=['h','hu','hv','eta','b']
    for key in keylist:
        sampledat[key]=[]

    if t0==-inf:
        t0=gaugedata['t'][0]
    if tend==inf:
        tend=gaugedata['t'][-1]

    t=linspace(t0,tend,ntimes)
    for tn in t:
        sampledat['t'].append(tn)
        if (tn<gaugedata['t'][0])|(tn>gaugedata['t'][-1]):
            for key in keylist :
                sampledat[key].append(nan)
        elif (tn==gaugedata['t'][0]):
            for key in keylist :
                sampledat[key].append(gaugedata[key][0])
        elif (tn==gaugedata['t'][-1]):
            for key in keylist :
                sampledat[key].append(gaugedata[key][-1])
        else:
            itm=mlab.find(gaugedata['t']<tn)[-1]
            itp = itm + 1
            tm=gaugedata['t'][itm]
            tp=gaugedata['t'][itp]
            delt=tp-tm
            for key in keylist:
                dely=gaugedata[key][itp]-gaugedata[key][itm]
                slope=dely/delt
                sampledat[key].append(gaugedata[key][itm] + slope*(tn-tm))

    if output:
        if outname=='':
            outname= '%s%03i_%i_.%s' % ('gauge',sampledat['gauge'],ntimes,'gdata')
        writegdata(sampledat,outname)

    if type(ingauge)==str:
        return
    else:
        return sampledat









