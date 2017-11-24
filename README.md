# Visualisation Code
Written in Python 2 using the Mayavi library (Mayavi is not well supported in Python 3 yet). Although this code is not specific to Python 2, so it should be easily generalisable to Python 3.

Everything is in SI units

# User Input
## Argument flags
### --file
Change input file. By default, this is a positive charge located at the origin. All files should be saved in the data folder. All files should be of type csv with the first row being front matter (the first row is ignored in the code). The input for the file argument should just be the name, no extension (csv) required.

### --e_vector/e_field/m_vector/m_field
Determine which graph is drawn (vector field or field lines; electric or magnetic)

### --grid
Change grid size and distance between points within grid. By default, the grid is from -10 to 10 on all 3 axis with 1 m between each point.

### --lines
Change the number of field lines rendered for field line plot. By default this is 5, increasing the number means more lines are drawn, decreasing means less.
