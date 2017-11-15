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
# changing grid size, input should look something like:
# 15 15 1 10 10 1 15 15 1
parser.add_option('-g', '--grid', type = 'string', dest = 'grid', help = 'Input render grid.')
# number of field lines to render
parser.add_option('--lines', type = 'int', dest = 'lines', help = 'Changes the number of field lines drawn.')

(options, args) = parser.parse_args()

# set file name
name = 'pos_charge' # default
if options.file:
    name = options.file

# read in csv file where the charges should be defined
charge = []
pos = []
with open('data/' + name + '.csv') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    for row in reader:
        charge.append(float(row[0]))
        pos.append((float(row[1]), float(row[2]), float(row[3])))

# changes grid size
if options.grid:
    grid = options.grid.split()
    grid = [float(i) for i in grid]
    x_grid = np.arange(grid[0], grid[1] + grid[2], grid[2])
    y_grid = np.arange(grid[3], grid[4] + grid[5], grid[5])
    z_grid = np.arange(grid[6], grid[7] + grid[8], grid[8])
else:
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
            elec = np.sum(np.array([functions.e_calc(q, (x, y, z), p) for q, p in zip(charge, pos) if functions.e_calc(q, (x, y, z), p) is not None]), axis = 0)
            if elec is None:
                x_field_y_z.append(0)
                y_field_y_z.append(0)
                z_field_y_z.append(0)
            else:
                x_field_y_z.append(elec[0])
                y_field_y_z.append(elec[1])
                z_field_y_z.append(elec[2])
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
else:
    functions.e_vector(charge, pos, x_grid, y_grid, z_grid, x_field, y_field, z_field)
    functions.e_field(charge, pos, x_grid, y_grid, z_grid, x_field, y_field, z_field, no_lines)
