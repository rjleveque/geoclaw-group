
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



def x_dz(xi,eta,x_0):
    """
    Convert xi,eta into x and dz when mass is centered at x_0.
    """

    xi_0 = x_0 / cos(theta)            # convert x_0 into distance along slope
    xi_j = xi
    zeta_j = zeta(xi_j - xi_0, eta)
    x_j =  cos(theta)*xi_j + sin(theta)*zeta_j
    z_j = -sin(theta)*xi_j + cos(theta)*zeta_j
    dz_j = z_j - (-tan(theta)*x_j)
    #import pdb; pdb.set_trace()
    return x_j,dz_j

def plot_slope(eta, x_0):

    xi = linspace(0., 3., 1001)
    if type(eta) != list:
        eta = [eta]

    figure(2)
    clf()
    for eta_k in eta:
        x,dz = x_dz(xi, eta_k, x_0)

        z0 = -tan(theta)*x 

        plot(x, z0, 'k')
        plot(x, z0 + dz, 'b')
        title("eta = %s, x_0 = %s" % (eta_k,x_0))

    if 0:
        x2 = cos(theta)*x - sin(theta)*(z0+dz)
        z2 = sin(theta)*x + cos(theta)*(z0+dz)
        plot(x2, 0*x2, 'g')
        plot(x2, z2, 'r')
    #import pdb; pdb.set_trace()
    axis('scaled')


def interp_dz(xi, eta, x_0, x):
    from scipy import interpolate
    x_j,dz_j = x_dz(xi, eta, x_0)
    dz = interpolate.interp1d(x_j, dz_j, bounds_error=False, fill_value=0.)
    return dz(x)



def interp_dz_2d(x,y,x_0):
    X,Y = meshgrid(x,y)
    dz = zeros(X.shape)
    xi = x*cos(theta)
    for j,eta in enumerate(y):
        dz[j,:] = interp_dz(xi, eta, x_0, x)
    return X,Y,dz

def make_s(t):
    from scipy import interpolate
    kdata = loadtxt("kinematics.txt",skiprows=1)
    t_j = kdata[:,0]
    sdata = zeros((len(t),7))
    for k in range(1,8):
        s_j = kdata[:,k]
        sfunc = interpolate.interp1d(t,s_j)
        sdata[:,k] = sfunc(t_j)
    return sdata


def make_dtopo(x,y,x_i,t,sdata):
    for k in range(7):
        s = sdata[:,k]
        dtopo = open("dtopo%s.tt1" % k,"w")
        for t_k,s_k in zip(t,s):
            x_0 = x_i + s_k
            X,Y,dz = interp_dz_2d(x,y,x_0)
            for j in range(len(y)-1, -1, -1):
                for i in range(len(x)):
                    dtopo.write("%20.12e  %20.12e  %20.12e  %20.12e\n" \
                           % (t_k,x[i],y[j],dz[j,i]))
        dtopo.close()

