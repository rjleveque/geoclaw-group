from pylab import *

figure(350)
clf()
# Plot Runup
t,x1,x2 = loadtxt('_output/fort.runup',unpack=True)

plot(t,x1,'b')
d = loadtxt('Delta_0100_RunupGage_2.txt')
plot(d[:,0],-d[:,1],'k')
legend(('GeoClaw', 'Lab Data'), loc='upper right')

figure(360)
clf()
plot(t,x2,'g')
d = loadtxt('Delta_0100_RunupGage_3.txt')
plot(d[:,0],-d[:,1],'r')
legend(('GeoClaw', 'Lab Data'), loc='upper right')

show()

