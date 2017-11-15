import numpy as np
import mayavi.mlab as mplt

def Notice():
    fig = mplt.figure()
    X,Y,Z = np.mgrid[-10:10:100j, -10:10:100j, -10:10:100j]
    thing = mplt.flow(X,Y,Z,X,Y,Z)
    phi, theta = np.mgrid[0:np.pi:11j, 0:2*np.pi:11j]
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    mplt.mesh(x+6, y, z, color=(1, 0, 0))
    mplt.axes()
    fig.scene.x_plus_view()
    mplt.show()

def Me():
    X,Y,Z = np.mgrid[-10:10:100j, -10:10:100j, -10:10:100j]
    # Let's also make the ball invisible and the lines green
    mplt.flow(X,Y,Z,2*X,Y,Z,seed_visible=False)
    mplt.show()

def Ella():
    X,Y,Z = np.mgrid[-10:10:10j, -10:10:10j, -10:10:10j]
    # Time for a quiver plot
    mplt.quiver3d(X,Y,Z,-X,-Y,np.abs(Z))
    mplt.show()

def Senpai():
    alpha = 1.0
    beta = 1.0
    epsilon = 1.0
    X,Y,Z = np.mgrid[-10:10:100j, -10:10:100j, -10:10:100j]
    # Are these meant to be the same?
    U = -(1.0/(4*epsilon)) * (alpha+beta) * (alpha / (Z**2 * (alpha**2 + Z**2)**0.5))
    V = -(1.0/(4*epsilon)) * (alpha+beta) * (alpha / (Z**2 * (alpha**2 + Z**2)**0.5))
    W = np.zeros_like(Z)
    mplt.flow(X,Y,Z,U,V,W,color=(0,1,1))
    mplt.show()

for f in [Notice,Me,Ella,Senpai]: f()
