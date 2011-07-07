
from pylab import *
from scipy import sinh,cosh,tanh,arccosh

# Problem parameters:

theta = 15. * pi / 180.
#theta = 70. * pi / 180.
epsilon = 0.717
C = arccosh(1. / epsilon)
b = 0.395
w = 0.680
T = 0.082
kb = 2*C / b
kw = 2*C / w

x_0 = [0.551, 0.617, 0.696, 0.763, 0.846, 0.877, 1.017]


def zeta(xi,eta):
    zeta1 = (T/(1.-epsilon)) * (1./(cosh(kb*xi)*cosh(kw*eta)) - epsilon)
    return maximum(zeta1, 0.)

    
def plot_cross_sec():
    """
    Plot vertical cross sections, compare to Figure 3.
    """
    xi = linspace(-0.5, 0.5, 101)
    eta = linspace(-0.7,0.7, 141)

    figure(1)
    clf()

    zeta_xi0 = zeta(0., eta)
    plot(eta, zeta_xi0, 'b')
    
    zeta_eta0 = zeta(xi, 0.)
    plot(xi, zeta_eta0, 'b')
    
    axis([-0.4, 0.4, 0, 0.15])



def x_dz(xi,eta,x_c):
    """
    Convert xi,eta into x and dz when mass is centered at x_c.
    """

    xi_c = x_c / cos(theta)            # convert x_c into distance along slope
    xi_j = xi
    zeta_j = zeta(xi_j - xi_c, eta)
    x_j =  cos(theta)*xi_j + sin(theta)*zeta_j
    z_j = -sin(theta)*xi_j + cos(theta)*zeta_j
    dz_j = z_j - (-tan(theta)*x_j)
    #import pdb; pdb.set_trace()
    return x_j,dz_j

def plot_slope(eta, x_c):

    xi = linspace(0., 3., 1001)
    if type(eta) != list:
        eta = [eta]

    figure(2)
    clf()
    for eta_k in eta:
        x,dz = x_dz(xi, eta_k, x_c)

        z0 = -tan(theta)*x 

        plot(x, z0, 'k')
        plot(x, z0 + dz, 'b')
        title("eta = %s, x_c = %s" % (eta_k,x_c))

    if 0:
        x2 = cos(theta)*x - sin(theta)*(z0+dz)
        z2 = sin(theta)*x + cos(theta)*(z0+dz)
        plot(x2, 0*x2, 'g')
        plot(x2, z2, 'r')
    #import pdb; pdb.set_trace()
    axis('scaled')


def interp_dz(xi, eta, x_c, x):
    from scipy import interpolate
    x_j,dz_j = x_dz(xi, eta, x_c)
    dz = interpolate.interp1d(x_j, dz_j, bounds_error=False, fill_value=0.)
    return dz(x)



def interp_dz_2d(x,y,x_c):
    X,Y = meshgrid(x,y)
    dz = zeros(X.shape)
    xi = x*cos(theta)
    for j,eta in enumerate(y):
        dz[j,:] = interp_dz(xi, eta, x_c, x)
    return X,Y,dz

def make_s(t):
    from scipy import interpolate
    kdata = loadtxt("kinematics-new.txt",skiprows=1)
    t_j = kdata[:,0]
    sdata = zeros((len(t),7))
    for k in range(7):
        s_j = kdata[:,k+1]
        sfunc = interpolate.interp1d(t_j,s_j)
        sdata[:,k] = sfunc(t)
    return sdata


def make_dtopo(x,y,x_0,t,sdata):
    for k in range(2):
        s = sdata[:,k]
        fname  = "dtopo%s.tt1" % (k+1)
        dtopo = open(fname,"w")
        for t_k,s_k in zip(t,s):
            x_c = x_0[k] + s_k
            X,Y,dz = interp_dz_2d(x,y,x_c)
            figure(3)
            clf()
            contour(X,Y,dz,linspace(0.01,0.1,10))
            title('x0 = %s, time = %s' % (x_0[k],t_k))
            draw()
            for j in range(len(y)-1, -1, -1):
                for i in range(len(x)):
                    dtopo.write("%20.12e  %20.12e  %20.12e  %20.12e\n" \
                           % (t_k,x[i],y[j],dz[j,i]))
        dtopo.close()
        print "Created ",fname

def make_all_dtopo():
    t = linspace(0,5,11)
    sdata = make_s(t)
    x = linspace(0,5,101)
    y = linspace(0,1,21)
    make_dtopo(x,y,x_0,t,sdata)
    


