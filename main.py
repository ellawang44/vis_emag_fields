from __future__ import division
import csv
import numpy as np
from optparse import OptionParser
import functions

# adds option flags for maximum customisability
parser = OptionParser()

# change files
parser.add_option('-f', '--file', type = 'string', dest = 'file', help = 'Reads in the given file.')
# draw different graphs
parser.add_option('--e_vector', action = 'store_true', dest = 'e_vector', help = 'Draw electric vector field.')
parser.add_option('--e_field', action = 'store_true', dest = 'e_field', help = 'Draw electric field.')
parser.add_option('--m_vector', action = 'store_true', dest = 'm_vector', help = 'Draw magnetic vector field.')
parser.add_option('--m_field', action = 'store_true', dest = 'm_field', help = 'Draw magnetic field.')
# changing grid size, input should look something like:
# 15 15 1 10 10 1 15 15 1
parser.add_option('-g', '--grid', type = 'string', dest = 'grid', help = 'Input render grid.')
# number of field lines to render
parser.add_option('--lines', type = 'int', dest = 'lines', help = 'Changes the number of field lines drawn.')

(options, args) = parser.parse_args()

# set file name
if options.e_vector or options.e_field:
    name = 'pos_charge' # default
elif options.m_vector or options.m_field:
    name = 'inf_wire' # default
if options.file:
    name = options.file

# read in csv file where the charges should be defined
if options.e_vector or options.e_field:
    charge = []
    pos = []
    with open('data/' + name + '.csv') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            charge.append(float(row[0]))
            pos.append((float(row[1]), float(row[2]), float(row[3])))
elif options.m_vector or options.m_field:
    currents = []
    orientations = []
    pos= []
    with open('data/' + name + '.csv') as f:
        reader = csv.reader(f, delimiter = ',')
        next(reader)
        for row in reader:
            currents.append(float(row[0]))
            orientations.append(row[1])
            pos.append((float(row[2]), float(row[3]), float(row[4])))

# changes grid size
if options.grid:
    grid = options.grid.split()
    grid = [float(i) for i in grid]
    x_grid = np.arange(grid[0], grid[1] + grid[2], grid[2])
    y_grid = np.arange(grid[3], grid[4] + grid[5], grid[5])
    z_grid = np.arange(grid[6], grid[7] + grid[8], grid[8])
else:
    grid = '-10 10 1 -10 10 1 -10 10 1'
    x_grid = np.arange(-10, 11, 1)
    y_grid = np.arange(-10, 11, 1)
    z_grid = np.arange(-10, 11, 1)

# create 3D array that stores the field
x_field = []
y_field = []
z_field = []
for x in x_grid:
    x_field_y = []
    y_field_y = []
    z_field_y = []
    for y in y_grid:
        x_field_y_z = []
        y_field_y_z = []
        z_field_y_z = []
        for z in z_grid:
            # calculate electric field
            if options.e_vector or options.e_field:
                val = np.sum(np.array([functions.e_calc(q, (x, y, z), p) for q, p in zip(charge, pos)]), axis = 0)
            # calculate magnetic field
            elif options.m_vector or options.m_field:
                val = np.sum(np.array([functions.m_calc_wire(i, o, l, (x, y, z)) for i, o, l in zip(currents, orientations, pos)]), axis = 0)
            # append values
            x_field_y_z.append(val[0])
            y_field_y_z.append(val[1])
            z_field_y_z.append(val[2])
        x_field_y.append(x_field_y_z)
        y_field_y.append(y_field_y_z)
        z_field_y.append(z_field_y_z)
    x_field.append(x_field_y)
    y_field.append(y_field_y)
    z_field.append(z_field_y)
x_field = np.array(x_field)
y_field = np.array(y_field)
z_field = np.array(z_field)

# set number of field lines drawn
no_lines = 5 # default
if options.lines:
    no_lines = options.lines

# draws the electric field
if options.e_vector:
    functions.e_vector(charge, pos, x_grid, y_grid, z_grid, x_field, y_field, z_field)
elif options.e_field:
    functions.e_field(charge, pos, x_grid, y_grid, z_grid, x_field, y_field, z_field, no_lines)
elif options.m_vector:
    functions.m_vector_wire(orientations, pos, grid, x_grid, y_grid, z_grid, x_field, y_field, z_field)
elif options.m_field:
    functions.m_field_wire(orientations, pos, grid, x_grid, y_grid, z_grid, x_field, y_field, z_field, no_lines)
