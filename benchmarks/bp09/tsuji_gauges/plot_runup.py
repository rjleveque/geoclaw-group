
from numpy import nan,array,sin,cos,arctan,linspace,pi,where
from matplotlib.pyplot import \
     plot,xticks,clf,figure,xlim,ylim,axis,xlabel,ylabel,text,title
lines = open('../AllTeamObs.txt','r').readlines()

gauges = []
for line in lines:
    if 'Tsuji' in line:
        tokens = line.split()
        gaugeno = int(tokens[0])
        x = float(tokens[1])
        y = float(tokens[2])
        obs = float(tokens[5])
        try:
            geoclaw = float(tokens[6])
        except:
            geoclaw = nan
        gauges.append([gaugeno,x,y,obs,geoclaw])

gauges = array(gauges)

figure(200)
clf()

plot(gauges[:,0],gauges[:,3],'ko-')
plot(gauges[:,0],gauges[:,4],'b^-')
labels = [int(i) for i in range(1,27)]
xticks(range(1,27), labels)

xlim((0,27))

#----------------------------
# Scatter plot:
#----------------------------
figure(201)
clf()

plot(gauges[:,4],gauges[:,3],'bo')
plot([0,35],[0,35],'k-')
axis('scaled')
xlim(0,35)
ylim(0,35)
xlabel("GeoClaw runup (m)",fontsize=15)
ylabel("Observed runup (m)",fontsize=15)
title('Scatter plot of observed vs. computed')

#----------------------------
# Run-up plot:
#----------------------------
figure(202)
clf()

x0 = 139.46
#y0 = 42.12
y0 = 42.14
x = gauges[:,1]
y = gauges[:,2]
obs = gauges[:,3]
geo = gauges[:,4]
xg = (x - x0)
yg = (y - y0)
theta = arctan(yg/xg)
theta = where((xg>0)&(yg<0), theta+2*pi, theta)
theta = where(xg<0, theta+pi, theta)
print theta
s = 1./35.
cost = cos(theta)
sint = sin(theta)
xz = cost
yz = sint
xobs = xz + s*obs*cost
yobs = yz + s*obs*sint
xgeo = xz + s*geo*cost
ygeo = yz + s*geo*sint

# plot circles
xc = cos(linspace(0,2*pi,500))
yc = sin(linspace(0,2*pi,500))
#for r in range(0,36,5):
for r in range(0,36,10):
    plot((1+s*r)*xc,(1+s*r)*yc,'k')
    text(-0.2,1+s*(r+1),'%s meters' % r)

plot(xgeo,ygeo,'g^',markersize=10)
plot(xobs,yobs,'ro')
xg = 6.*(x - x0)
yg = 6.*(y - y0)
plot(xg,yg,'ko')
for i in range(len(x)):
    plot([xg[i],xobs[i]],[yg[i],yobs[i]],'k-')
    plot([xg[i],xgeo[i]],[yg[i],ygeo[i]],'g-')

axis('scaled')
title('Run-up (red circles = observations)')
axis('off')
