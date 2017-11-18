from __future__ import division
import numpy as np
import mayavi.mlab as mplt

ep_0 = 8.854*10**-12 # vaccumn permissitivity
cons = 1/(4*np.pi*ep_0) # Coloumb's constant (k)
mu_0 = 4 * np.pi * 10**(-7) # permeability of free space

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
        E_x = cons * q * x_dist / d_sq
        E_y = cons * q * y_dist / d_sq
        E_z = cons * q * z_dist / d_sq
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
    mplt.quiver3d(X, Y, Z, x_field, y_field, z_field)
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
        ball = mplt.flow(X,Y,Z,x_field, y_field, z_field, figure=fig, seedtype='sphere', integration_direction='both')
        ball.seed.widget.center = location
        # number of field lines to integrate over
        ball.seed.widget.theta_resolution = no_lines
        ball.seed.widget.phi_resolution = no_lines
        # number of integration steps
        ball.stream_tracer.maximum_propagation = 200
        ball.seed.widget.radius = 1
        # dodgy hax... TL;DR widgets are dumb
        ball.seed.widget.enabled = False
        ball.seed.widget.enabled = True
    mplt.axes()
    # set view to x-axis coming out of screen
    fig.scene.x_plus_view()
    mplt.draw(figure=fig)
    mplt.show()

def torus(R):

    ''' draw torus for magnetic field of coil'''

    # thickness of the torus
    thickness = 1
    # polar coordinates for torus
    u = np.linspace(0,2*np.pi,100)
    v = np.linspace(0,2*np.pi,100)
    u,v = np.meshgrid(u,v)
    # convert to cartesian coordinates
    x = (R + thickness * np.cos(v)) * np.cos(u)
    y = (R + thickness * np.cos(v)) * np.sin(u)
    z = thickness * np.sin(v)
    mplt.mesh(x, y, z, color = (0.3, 0.3, 0.3))

def wire(ori, loc, grid):
    s = 0.5
    phi = np.linspace(0, 2*np.pi, 100)
    phi, _ = np.meshgrid(phi, phi)
    grid = grid.split()
    grid = [int(i) for i in grid]
    if ori == 'x':
        x, _ = np.mgrid[grid[0]:grid[1]:100j, grid[0]:grid[1]:100j]
        y = s*np.cos(phi) + loc[1]
        z = s*np.sin(phi) + loc[2]
    elif ori == 'y':
        x = s*np.cos(phi) + loc[0]
        y, _ = np.mgrid[grid[3]:grid[4]:100j, grid[6]:grid[7]:100j]
        z = s*np.sin(phi) + loc[2]
    elif ori == 'z':
        x = s*np.cos(phi) + loc[0]
        y = s*np.sin(phi) + loc[1]
        z, _ = np.mgrid[grid[6]:grid[7]:100j, grid[6]:grid[7]:100j]
    else:
        raise ValueError('not an allowed orientation')
    mplt.mesh(x, y, z, color = (1, 0, 0))

def m_calc_wire(I, ori, loc, r):

    '''calculate magnetic field of an infinite wire'''

    x = r[0]
    y = r[1]
    z = r[2]
    if ori == 'x':
        num = (y-loc[1])**2 + (z-loc[2])**2
        if num == 0.0:
            return (0., 0., 0.)
        cons = mu_0 * I / (2 * np.pi * num)
        B_x = 0.0
        B_y = cons * -(z - loc[2])
        B_z = cons * (y - loc[1])
    elif ori == 'y':
        num = (x-loc[0])**2 + (z-loc[2])**2
        if num == 0.0:
            return (0., 0., 0.)
        cons = mu_0 * I / (2 * np.pi * num)
        B_x = cons * (z - loc[2])
        B_y = 0.0
        B_z = cons * -(x - loc[0])
    elif ori == 'z':
        num = (x-loc[0])**2 + (y-loc[1])**2
        if num == 0.0:
            return (0., 0., 0.)
        cons = mu_0 * I / (2 * np.pi * num)
        B_x = cons * -(y - loc[1])
        B_y = cons * (x - loc[0])
        B_z = 0.0
    else:
        raise ValueError('not an allowed orientation')
    return (B_x, B_y, B_z)

def m_vector_wire(ori, loc, grid, x_grid, y_grid, z_grid, x_field, y_field, z_field):
    fig = mplt.figure()
    # draw sphere for point charge
    for orientation, location in zip(ori, loc):
        wire(orientation, location, grid)
    # draw vector field
    X,Y,Z = np.meshgrid(x_grid, y_grid, z_grid, indexing = 'ij')
    mplt.quiver3d(X, Y, Z, x_field, y_field, z_field)
    # set view to x-axis coming out of screen
    fig.scene.x_plus_view()
    mplt.show()

''' this doesn't work
def m_field_wire(q, pos, x_grid, y_grid, z_grid, x_field, y_field, z_field, no_lines):
    fig = mplt.figure()
    X,Y,Z = np.meshgrid(x_grid, y_grid, z_grid, indexing = 'ij')
    for charge, location in zip(q, pos):
        # draw sphere for point charge
        sphere(charge, location)
        # draw electric field lines
        ball = mplt.flow(X,Y,Z,x_field, y_field, z_field, figure=fig, seedtype='sphere', integration_direction='both')
        ball.seed.widget.center = location
        # number of field lines to integrate over
        ball.seed.widget.theta_resolution = no_lines
        ball.seed.widget.phi_resolution = no_lines
        # number of integration steps
        ball.stream_tracer.maximum_propagation = 200
        ball.seed.widget.radius = 1
        # dodgy hax... TL;DR widgets are dumb
        ball.seed.widget.enabled = False
        ball.seed.widget.enabled = True
    mplt.axes()
    # set view to x-axis coming out of screen
    fig.scene.x_plus_view()
    mplt.draw(figure=fig)
    mplt.show()
    '''
