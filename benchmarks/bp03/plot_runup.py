from pylab import *

figure(350)
clf()
# Plot Runup
t,x1,x2 = loadtxt('_output/fort.runup',unpack=True)
plot(t,x1,'b')
#plot(t,x2,'g')

#t,x1,x2 = loadtxt('_output_fine/fort.runup',unpack=True)
#plot(t,x1,'r')
#plot(t,x2,'g')

#legend(('GeoClaw coarse', 'GeoClaw fine'), loc='upper left')


