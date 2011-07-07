from numpy import * 
from pylab import *

E = loadtxt('file2.txt',skiprows=1)


t = linspace(-10,60,400)
for k in linspace(1,4,4):
    D = loadtxt("./canonical-beach-lab-3/_output/fort.q000%i" % k, skiprows =9)
    h = D[0:400,3]
    
    kodd=2*k-1
    keven=2*(k-1)
    Q = [0,15,20,25,30]    
    tlab = E[:,keven]
    hlab = E[:,kodd]

    def plot_xt(h,t,hlab,tlab,k):
        figure(k)
        clf()

        Q1 = Q[int(k)]
        title('Comparrison of Analytical and Theoretical Results for time %i'%Q1,fontsize=15)
        ylabel('$\eta/d$',fontsize=15)
        xlabel('x/d',fontsize=15)
        xlim(-7,16)

        beachx =linspace(-7,1,10)
        beachy = -beachx/19.85
        plot(beachx,beachy,'k', linewidth=5, label='beach')
        

        plot(t,h, label='Clawpack Result')
        plot(tlab, hlab, 'r',label='Laboratory Result')
        legend(('Beach','Clawpack Result','Laboratory Result'))
        # save figure as png file with unique name:
        savefig('plot3_%i.png' % k)


    if __name__=="__main__":
        plot_xt(h,t,hlab,tlab,k)
        

