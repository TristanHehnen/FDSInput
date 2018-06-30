import numpy as np
import matplotlib.pyplot as plt


def circle_raster(r, dx, xm=0.0, ym=0.0, zm=0.0,
                  dy=None, dz=None, height=0.1):
    # (x - xm)**2 + (y + ym)**2 = r**2
    # x**2 + y**2 = r**2

    # Make the cells cubes, if nothing is defined specifically.
    if dy is None:
        dy = dx
    if dz is None:
        dz = dx

    # Calculate upper end of slices in y, depending on grid resolution.
    coord_list = []
    # Start at one half of the cell size.
    x = dx / 2
    while x <= r:
        y = np.sqrt(r**2 - (x - xm)**2) + ym
        coord_list.append([x, y])
        x += dx

    # Calculate obstruction dimensions, described by two points p1 and p2.
    # Calculate how many cells the radius spans, and separate into a tuple of
    #  integer and rest.
    r_n = (int(r // dx), r % dx)
    if r_n[1] != 0:
        dr = r_n[0] + 1
    else:
        dr = r_n[0]

    # p1x, p1y, p1z = 0.0 + xm, 0.0 + ym, 0.0 + zm
    box_coord = []

    x = dx / 2
    counter = 1
    while x <= r:
        y = np.sqrt(r ** 2 - (x - xm) ** 2) + ym

        y_n = (int(y // dy), y % dy)
        # print(y_n)
        if y_n[1] != 0:
            dy_n = y_n[0] + 1
        else:
            dy_n = y_n[0]

        p2x = dx * counter
        p1x = p2x - dx
        p2y = dy_n * dy
        p1y = -p2y
        p1z = zm
        p2z = zm + height

        new_obst = [p1x, p2x, p1y, p2y, p1z, p2z]
        box_coord.append(new_obst)
        new_obst = [-p1x, -p2x, p1y, p2y, p1z, p2z]
        box_coord.append(new_obst)

        x += dx
        counter += 1

    return coord_list, box_coord


##############

xloc, yloc = 0, 0

radius = 0.03
dh = 0.001

cl, bl = circle_raster(radius, dh, zm=-0.02, height=0.02)

print(cl)
for i in range(len(bl)):
    print(bl[i])

a = int(0.1/dh)
b = int(0.1/dh)
c = int(0.04/dh)
m = "&MESH IJK={},{},{}, XB=-0.05,0.05,-0.05,0.05,-0.01,0.03/".format(a, b, c)
print(m)
print("")


#######################
### Lower Pipe
for t in bl:
    nstr = "&OBST XB = {}, {}, {}, {}, {}, {} /".format(t[0], t[1],
                                                        t[2], t[3],
                                                        t[4], t[5])
    print(nstr)

print("")


#######################
### Upper Pipe
cl2, bl2 = circle_raster(radius, dh, zm=0.013, height=0.02)

for t in bl2:
    nstr = "&OBST XB = {}, {}, {}, {}, {}, {} /".format(t[0], t[1],
                                                        t[2], t[3],
                                                        t[4], t[5])
    print(nstr)

print("")


#######################
### Lower VENT

cl3, bl3 = circle_raster(radius, dh, zm=0.0, height=0.00)

for t in bl3:
    nstr = "&VENT XB = {}, {}, {}, {}, {}, {}" \
           ", COLOR='RASPBERRY', SURF_ID='BURNER' /".format(t[0], t[1],
                                                            t[2], t[3],
                                                            t[4], t[5])
    print(nstr)

print("")


#######################
### Upper VENT

cl4, bl4 = circle_raster(radius, dh, zm=0.013, height=0.00)

for t in bl4:
    nstr = "&VENT XB = {}, {}, {}, {}, {}, {}" \
           ", COLOR='BLUE', SURF_ID='OXIDISER' /".format(t[0], t[1],
                                                         t[2], t[3],
                                                         t[4], t[5])
    print(nstr)

print("")


# for coord in cl:
#     plt.plot(coord[0], coord[1], marker='o')
#
#
# # Check if it is a circle.
# t = np.arange(0, np.pi/2, 0.1)
# for j in t:
#     plt.plot(np.cos(j), np.sin(j), marker='.')
#
# plt.xticks(np.arange(0, 1.1, step=dh))
# plt.yticks(np.arange(0, 1.1, step=dh))
# plt.xlim(-0.05, 1.05)
# plt.ylim(-0.05, 1.05)
# plt.grid()
# plt.show()

