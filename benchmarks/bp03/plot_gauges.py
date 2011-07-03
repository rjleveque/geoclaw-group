from pylab import *
from pyclaw.plotters.data import ClawPlotData

gaugenos = [1,2,3,4]


def plot_gauge(d,my_list,gaugeno):
    figure(360)
    clf()

    plotdata = ClawPlotData()
    d, gt, gv = read_lab_data(d)
    for my in my_list:
        outdir = "_output_%s_my%s" %(d,my)
        plotdata.outdir = outdir
        gs = plotdata.getgauge(gaugeno)
        plot(gs.t, gs.q[:,3], linewidth=1)
    legend_list = []
    for my in my_list:
        legend_list.append("my = %s" % my)
    if gv[gaugeno] is not None:
        plot(gt, gv[gaugeno],'k', linewidth=2)
        legend_list.append("Lab data")
    #axis([0,5,-.01,.02])
    legend(legend_list, loc='lower right')
    title("Gauge %s for d = %5.3f" % (gaugeno,d), fontsize=20)

def read_lab_data(d_param=None):
    #import pdb; pdb.set_trace()
    if d_param==None:
        probdata = Data(os.path.join(datadir,'setprob.data'))
        d_param = probdata.d
    
    print '+++ d_param = ',d_param
    if d_param==0.061: fname = 'd61g1234-new.txt'
    if d_param==0.080: fname = 'd80g1234-new.txt'
    if d_param==0.100: fname = 'd100g124-new.txt'
    if d_param==0.120: fname = 'd120g124-new.txt'
    if d_param==0.140: fname = 'd140g1234-new.txt'
    if d_param==0.149: fname = 'd149g124-new.txt'
    if d_param==0.189: fname = 'd189g1234-new.txt'
    
    try:
        print "Reading gauge data from ",fname
    except:
        print "*** No gauge data for d_param = ",d_param
    
    try:
        gaugedata = loadtxt(fname)
    except:
        raise Exception( "*** Cannot read file %s ",fname)
    gauget = gaugedata[:,0]
    gauge_ave = {}
    for gaugeno in [1,2,3,4]:
        try:
            gauge_ave[gaugeno] = gaugedata[:,3*gaugeno] * 0.001
        except:
            # If fails for gaugeno==4 then it is gauge 3 that's missing:
            gauge_ave[3] = None
            #import pdb; pdb.set_trace()
            try:
                gauge_ave[4] = gaugedata[:,9] * 0.001
            except:
                gauge_ave[2] = gaugedata[:,4] * 0.001
                gauge_ave[4] = gaugedata[:,5] * 0.001

    return d_param, gauget, gauge_ave
        


if __name__=="__main__":
    my_list = [18,36,72]
    for d in [0.061, 0.080, 0.100, 0.120, 0.140, 0.149, 0.189]:
        for gaugeno in gaugenos:
            plot_gauge(d,my_list,gaugeno)
            fname = 'gauge%s-d%s.png' % (gaugeno,d)
            fname = fname.replace('0.','0-')
            savefig(fname)
            print "Created %s" % fname
        
