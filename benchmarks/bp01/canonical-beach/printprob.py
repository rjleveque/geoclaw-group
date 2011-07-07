from numpy import * 
from pylab import *

E = loadtxt("canonical_profiles.txt",skiprows=5)
ttheo = E[:,0]
t = linspace(-3,18,120)

I = [0,35,40,45,50,55,60,65,70]
#added the zero in the beginning as a padding cell


G = loadtxt('./_output/fort.gauge')
D = loadtxt('canonical_ts1.txt',skiprows=5)
D2 = loadtxt('canonical_ts2.txt',skiprows=5)
t25 = hstack((D[:,0],D2[:,0]))
h25 = hstack((D[:,1],D2[:,1]))
t995 = D[:,2]
h995 = D[:,3]


hc25 = G[0:-1:2,6]
hc995 = G[1:-1:2,6]
tc25 = G[0:-1:2,2]
tc995 = G[1:-1:2,2]


beachx =linspace(-4,1,10)
beachy = -beachx/19.85

for k in linspace(1,8,8):

    D = loadtxt("./_output/fort.q000%i" % k, skiprows =9)
    h = D[40:160,3]

    htheo = E[:,k]

    
    def plot_comp(h,t,htheo,ttheo,k):
        figure(k)
        clf()
        ylabel('$\eta/d$',fontsize=15)
        xlabel('x/d',fontsize=15)
        plot(t,h, label='Clawpack Result')
        plot(beachx,beachy,'k', linewidth=5, label='beach')
        plot(ttheo, htheo, label='Analytical Result')
        legend(('Clawpack Result','Beach','Analytical Result'))
        title('Clawpack and Analytical Results at time t = %i'  %I[int(k)])
        # save figure as png file with unique name:
        time = 30+5*k
        savefig('bp1compt%i.png' % time)


    def plot_gauge1(hc25,tc25,h25,t25):
        figure(1)
        clf()
        ylabel('$\eta/d$',fontsize=15)
        xlabel('t(g/d)',fontsize=15)

        plot(tc25,hc25, label='Clawpack Result')
        plot(t25,h25,'r', label='Analytical Result')
        legend(('Clawpack Result','Analytical Result'))
        title('Gauge Comparison at X = 0.25(h/d)', fontsize=15)
        # save figure as png file with unique name:
        savefig('plotgauge1.png')


    def plot_gauge2(hc995,tc995,h995,t995):
        figure(1)
        clf()
        ylabel('$\eta/d$',fontsize=15)
        xlabel('t(g/d)',fontsize=15)

        plot(tc995,hc995, label='Clawpack Result')
        plot(t995,h995,'r', label='Analytical Result')
        legend(('Clawpack Result','Analytical Result'))
        title('Gauge Comparison at X = 9.95(h/d)', fontsize=15)
        # save figure as png file with unique name:
        savefig('plotgauge2.png')

    if __name__=="__main__":
        plot_comp(h,t,htheo,ttheo,k)
        plot_gauge1(hc25,tc25,h25,t25)
        plot_gauge2(hc995,tc995,h995,t995)
        

