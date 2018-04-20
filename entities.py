import data_structures as ds
import matplotlib.pyplot as plt
import numpy as np

def circle(diameter, thickness, cell_x, cell_y=None, cell_z=None):

    # Check if cell sizes are provided for y and z. Otherwise set to length
    # in x, assuming cubes.
    if cell_y is None:
        cell_y = cell_x
    if cell_z is None:
        cell_z = cell_x

xval = []
yval=[]
n=30
for i in range(n):
    phi = (1/n*i)
    # 1 = x2 + y2 -> y = sqrt(1-x2)
    x = np.sqrt(1-phi**2)
    xval.append(x)
    yval.append(phi)

plt.figure(figsize=[5, 5])
plt.plot(xval, yval)

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()


