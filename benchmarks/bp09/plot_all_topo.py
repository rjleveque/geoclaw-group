
#from pyclaw.plotters import geoplot
import geoplot


topo_files = ['OK24.tt1', 'AO15.tt1', 'OK08.tt1', 'OK03.tt1', 'MB05.tt1', 'MO01.tt1']
fname = ['OK24.tt1',  'AO15.tt1']
for fname in topo_files:
    T = geoplot.TopoPlotData(fname)
    T.topotype=1
    T.plot()
    

