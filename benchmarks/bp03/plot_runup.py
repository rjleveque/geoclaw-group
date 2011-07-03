from pylab import *

def plot_runup(d,my_list):
    figure(350)
    clf()

    for my in my_list:
        outdir = "_output_%s_my%s" %(d,my)
        t,x1,x2 = loadtxt('%s/fort.runup' % outdir,unpack=True)
        plot(t,-x1)

    legend_list = []
    for my in my_list:
        legend_list.append("my = %s" % my)
    axis([0,5,-.015,.015])
    legend(legend_list, loc='upper left')
    title("Runup for d = %5.3f" % d, fontsize=20)


if __name__=="__main__":
    my_list = [18,36,72]
    for d in [0.061, 0.080, 0.100, 0.120, 0.140, 0.149, 0.189]:
        plot_runup(d,my_list)
        fname = 'runup-d%s.png' % d
        fname = fname.replace('0.','0-')
        savefig(fname)
        print "Created %s" % fname
