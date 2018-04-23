import data_structures as ds
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def circle(radius, thickness, cell_x, cell_y=None, cell_z=None,
           pos_x=0, pos_y=0, poly=48):

    # Check if cell sizes are provided for y and z. Otherwise set to length
    # in x, assuming cubes.
    if cell_y is None:
        cell_y = cell_x
    if cell_z is None:
        cell_z = cell_x

    xval = []
    yval = []
    # n = 48
    #
    #
    # xm = 1
    # ym = 2
    # r = 1

    for i in range(poly + 1):
        # Increments of angle phi.
        phi = (2 * np.pi) * (1 / poly) * i

        # Parametric circle.
        x = pos_x + radius * np.cos(phi)
        y = pos_y + radius * np.sin(phi)

        # Check
        radius = x ** 2 + y ** 2

        #     print(x, y, radius)
        xval.append(x)
        yval.append(y)

    return xval, yval


xvalues, yvalues = circle(1,1,0)


# Create figure and axes
fig, ax = plt.subplots(1)

# plt.figure(figsize=[8, 8])
ax.plot(xvalues, yvalues)

# plt.xlim(-1.2, 1.2)
# plt.ylim(-1.2, 1.2)
ax.grid()

# plt.show()


# Detect if points are in cells of a given raster.

# Describe the raster (cell size)
raster_x = 0.1
raster_y = 0.1

# cell position
rectx = 0.5
recty = 0.5

print(xvalues[0])
print(yvalues[0])

# Create a Rectangle patch
rect = patches.Rectangle((rectx, recty),
                         0.1, 0.1, linewidth=1,
                         edgecolor='r',
                         facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect)

plt.show()
