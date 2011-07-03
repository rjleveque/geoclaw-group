from pylab import *

def plot_runup(d,my_list):
    figure(350)
    clf()

    for my in my_list:
        outdir = "_output_%s_my%s" %(d,my)
        t,x1,x2 = loadtxt('%s/fort.runup' % outdir,unpack=True)
        plot(t,x1)

    legend_list = []
    for my in my_list:
        legend_list.append("my = %s" % my)
    axis([0,5,-.01,.02])
    legend(legend_list, loc='lower left')
    title("Runup for d = %5.3f" % d)


if __name__=="__main__":
    my_list = [18,36,72]
    for d in [0.061, 0.080, 0.100, 0.120, 0.140, 0.149, 0.189]:
        plot_runup(d,my_list)
        savefig('runup_d%s.png' % d)
        print "Created runup_d%s.png" % d
        
