from __future__ import division
import numpy as np
import mayavi.mlab as mplt

ep_0 = 8.854*10**-12 # vaccumn permissitivity
cons = 1/(4*np.pi*ep_0) # Coloumb's constant (k)

def e_calc(q, r, r_prime):

    ''' Calculates the electric field '''

    x, y, z = r
    x_prime, y_prime, z_prime = r_prime
    x_dist = x - x_prime
    y_dist = y - y_prime
    z_dist = z - z_prime
    d_sq = x_dist**2 + y_dist**2 + z_dist**2
    if d_sq == 0.0:
        return (0.,0.,0.)
    else:
        E_x = cons*q*x_dist/d_sq
        E_y = cons*q*y_dist/d_sq
        E_z = cons*q*z_dist/d_sq
        return (E_x, E_y, E_z)

def sphere(q, pos):

    '''draw sphere for point charge'''

    phi, theta = np.mgrid[0:np.pi:11j, 0:2*np.pi:11j]
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    x_loc, y_loc, z_loc = pos
    # determine colour of sphere based on charge
    if q == 0:
        raise ValueError('Charge can not be 0')
    elif q > 0:
        c = (1, 0, 0)
    else:
        c = (0, 0, 1)
    mplt.mesh(x + x_loc, y + y_loc, z + z_loc, color=c)

def e_vector(q, pos, x_grid, y_grid, z_grid, x_field, y_field, z_field):
    fig = mplt.figure()
    # draw sphere for point charge
    for charge, location in zip(q, pos):
        sphere(charge, location)
    # draw vector field
    X,Y,Z = np.meshgrid(x_grid, y_grid, z_grid, indexing = 'ij')
    mplt.quiver3d(X,Y,Z, x_field, y_field, z_field)
    # set view to x-axis coming out of screen
    fig.scene.x_plus_view()
    mplt.show()

def e_field(q, pos, x_grid, y_grid, z_grid, x_field, y_field, z_field, no_lines):
    fig = mplt.figure()
    X,Y,Z = np.meshgrid(x_grid, y_grid, z_grid, indexing = 'ij')
    for charge, location in zip(q, pos):
        # draw sphere for point charge
        sphere(charge, location)
        # draw electric field lines
        thing = mplt.flow(X,Y,Z,x_field, y_field, z_field, figure=fig, seedtype='sphere', integration_direction='both')
        thing.seed.widget.center = location
        # number of field lines to integrate over
        thing.seed.widget.theta_resolution = no_lines
        thing.seed.widget.phi_resolution = no_lines
        # number of integration steps
        thing.stream_tracer.maximum_propagation = 200
        thing.seed.widget.radius = 1
        # dodgy hax...
        thing.seed.widget.enabled = False
        thing.seed.widget.enabled = True
    mplt.axes()
    # set view to x-axis coming out of screen
    fig.scene.x_plus_view()
    mplt.draw(figure=fig)
    mplt.show()
