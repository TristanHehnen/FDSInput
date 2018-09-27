import numpy as np
import matplotlib.pyplot as plt


def circle_raster(r, dx, xm=0.0, ym=0.0, zm=0.0,
                  dy=None, dz=None, height=None):
    """
    Creates a rastered circle, as multiple adjacent boxes. Only half of the
    circle is created, second half is mirrored. The circle is constructed around
    the origin (0, 0, 0) and shifted to another location afterwards, if values
    for the new center (xm, ym, zm) are provided.
    Note: If only information for dx is provided, cells are assumed to
    be cubes (dx=dy=dz)!

    :param r: Circle radius
    :param dx: Edge length of cube-shaped cells.
    :param xm: X-component of circle center location.
    :param ym: Y-component of circle center location.
    :param zm: Z-component of circle center location.
    :param dy: Edge length of cube-shaped cells.
    :param dz: Edge length of cube-shaped cells.
    :param height: Thickness of the circle --> cylinder.

    :return: List of coordinates.
             List of box coordinates.
    """

    # (x - xm)**2 + (y + ym)**2 = r**2
    # x**2 + y**2 = r**2

    # Make the cells cubes, if nothing is defined specifically.
    if dy is None:
        dy = dx
    if dz is None:
        dz = dx

    # Creates a disk with a thickness of one cell size, if nothing else is
    # defined.
    if height is None:
        height = dz

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

    # Initialise coordinate list.
    box_coord = []

    # Brute force iteration over the circle, create a box for each slice with
    # a width of one cell (dx).
    x = dx / 2
    counter = 1
    while x <= r:
        # y = np.sqrt(r ** 2 - (x - xm) ** 2) + ym
        y = np.sqrt(r ** 2 - x ** 2)

        y_n = (int(y // dy), y % dy)
        # print(y_n)
        if y_n[1] != 0:
            dy_n = y_n[0] + 1
        else:
            dy_n = y_n[0]

        p2x = dx * counter + xm
        p1x = p2x - dx
        p2y = dy_n * dy + ym
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


def sphere_raster(r, dx, xm=0.0, ym=0.0, zm=0.0,
                  dy=None, dz=None):

    # Make the cells cubes, if nothing is defined specifically.
    if dy is None:
        dy = dx
    if dz is None:
        dz = dx

    # Calculate obstruction dimensions, described by two points p1 and p2.
    # Calculate how many cells the radius spans, and separate into a tuple of
    # integer and rest. Thus, the number of cells, that need to be "filled", is
    # determined. If there is a rest, the cell is filled as well --> always
    # "rounded up".
    r_n = (int(r // dx), r % dx)
    if r_n[1] != 0:
        dr = r_n[0] + 1
    else:
        dr = r_n[0]

    # Initialise coordinate list.
    box_coord = []

    # Brute force iteration over the circle, create a box for each slice with
    # a width of one cell (dx) and a height of one cell (dz).
    # x = dx / 2
    z = dz / 2


    # Iterate over the northern hemisphere, starting from the center slice,
    # to the north pole (z+). Calculate horizontal cross section ring radius
    # (rx) for each slice, in the x-y plane.
    slice_counter = 1
    while z <= r:
        # rx = np.sqrt(r ** 2 - (z - zm) ** 2) + xm
        rx = np.sqrt(r ** 2 - z ** 2)
        print(rx)

        # Create horizontal slice of the sphere, starting at the center and move
        # up, meaning in z+ direction.
        # Coordinate in z-axis of northern hemisphere are mirrored,
        # to generate whole sphere.
        x = dx / 2
        box_counter = 1
        while x <= rx:
            # y = np.sqrt(rx ** 2 - (x - xm) ** 2) + ym
            y = np.sqrt(rx ** 2 - x ** 2)

            y_n = (int(y // dy), y % dy)
            # print(y_n)
            if y_n[1] != 0:
                dy_n = y_n[0] + 1
            else:
                dy_n = y_n[0]

            # p2x = dx * box_counter + xm
            # p1x = p2x - dx + xm
            # p2y = dy_n * dy + ym
            # p1y = -p2y + ym
            # p1z = -z - dz / 2 + zm
            # p2z = z + dz / 2 + zm
            # # p1z = zm + dz * (slice_counter - 1)
            # # p2z = zm + dz * slice_counter

            p1x = xm - dx * box_counter
            p2x = xm + dx * box_counter
            p1y = ym - dy_n * dy
            p2y = ym + dy_n * dy
            p1z = zm - z - dz / 2
            p2z = zm + z + dz / 2


            new_obst = [p1x, p2x, p1y, p2y, p1z, p2z]
            box_coord.append(new_obst)
            new_obst = [-p1x, -p2x, p1y, p2y, p1z, p2z]
            box_coord.append(new_obst)

            x += dx
            box_counter += 1

        z += dz
        slice_counter += 1
        print("slice", slice_counter, z)

    return box_coord


def fds_lollipop_tree(x_loc, y_loc, z_loc, dx, h_trunk=2.0, r_leafs=3.0,
                      r_trunk=None, dy=None, dz=None):

    # Make the cells cubes, if nothing is defined specifically.
    if dy is None:
        dy = dx
    if dz is None:
        dz = dx

    # Set tree trunk radius to 5% of the leaf radius.
    if r_trunk is None:
        r_trunk = 0.05 * r_leafs

    # Set up the tree trunk.
    empty, trunk_coords = circle_raster(r_trunk, dx, x_loc, y_loc, z_loc,
                                        dy, dz, h_trunk)

    # Set up the leafs.
    leaf_height = z_loc + h_trunk + r_leafs
    leaf_coords = sphere_raster(r_leafs, dx, x_loc, y_loc, leaf_height, dy, dz)

    # #
    # tree_parts = [trunk, leafs]
    # tree = []
    # for part in tree_parts:
    #     for coord_set in part:
    #         tree.append(coord_set)

    # Create input line for the tree.
    tree = []

    # Define FDS obstruction input line.
    obst_line = "&OBST XB = {}, {}, {}, {}, {}, {}, SURF_ID='{}' /"

    # Add tree trunk.
    for coord_set in trunk_coords:
        nl = obst_line.format(coord_set[0], coord_set[1],
                              coord_set[2], coord_set[3],
                              coord_set[4], coord_set[5],
                              "BARK")
        tree.append(nl)

    # Add leafs.
    for coord_set in leaf_coords:
        nl = obst_line.format(coord_set[0], coord_set[1],
                              coord_set[2], coord_set[3],
                              coord_set[4], coord_set[5],
                              "LEAFS")
        tree.append(nl)

    return tree


def write_fds_input(file_name, box_coord):
    """

    :param file_name: Name of the text file, that shall contain the output.
    :param box_coord: List of coordinates describing the individual boxes
        (OBST).

    :return: None, writes text file to hard drive.
    """

    fds_file = open('{}.txt'.format(file_name), 'w')

    for i in box_coord:
        nl = "&OBST XB = {}, {}, {}, {}, {}, {} /".format(i[0], i[1],
                                                          i[2], i[3],
                                                          i[4], i[5])
        fds_file.write("%s\n" % nl)

    fds_file.close()
    print("* The file '{}.txt' was written.".format(file_name))


def write_fds_input2(file_name, input_lines):
    """

    :param file_name: Name of the text file, that shall contain the output.
    :param box_coord: List of coordinates describing the individual boxes
        (OBST).

    :return: None, writes text file to hard drive.
    """

    fds_file = open('{}.txt'.format(file_name), 'w')

    for line in input_lines:
        fds_file.write("%s\n" % line)

    fds_file.close()
    print("* The file '{}.txt' was written.".format(file_name))


##############

xloc, yloc = 0, 0

radius = 0.09
dh = 0.001

# cl, bl = circle_raster(radius, dh, zm=-0.02, height=0.02)
#
# print(cl)
# for i in range(len(bl)):
#     print(bl[i])
#
# a = int(0.1/dh)
# b = int(0.1/dh)
# c = int(0.04/dh)
# m = "&MESH IJK={},{},{}, XB=-0.05,0.05,-0.05,0.05,-0.01,0.03/".format(a, b, c)
# print(m)
# print("")


# #######################
# ### Sphere
# sr = 2
# dsh = 0.1
#
# sbl1 = sphere_raster(sr, dsh)
# sbl2 = sphere_raster(sr, dsh, xm=5.0, ym=0.0, zm=0.0)
# sbl3 = sphere_raster(sr, dsh, xm=0.0, ym=0.0, zm=5.0)
# sbl4 = sphere_raster(sr, dsh, xm=0.0, ym=5.0, zm=5.0)
#
#
# sbls = [sbl1, sbl2, sbl3, sbl4]
#
# sbl = []
# for i in sbls:
#     for j in i:
#         sbl.append(j)
#
#
# write_fds_input("sphere_test", sbl)
#
# for t in sbl1:
#     nstr = "&OBST XB = {}, {}, {}, {}, {}, {} /".format(t[0], t[1],
#                                                         t[2], t[3],
#                                                         t[4], t[5])
#     # print(nstr)
#
# print("")


#######################
### Tree test

dht = 0.1
tree_rad = 3.0
tree_height = 2.0

t = fds_lollipop_tree(0.0, 0.0, 1.0, dht, tree_height, tree_rad)
write_fds_input2("tree_test", t)
print("")

# t1 = fds_lollipop_tree(0.0, 0.0, 0.0, dht, tree_height, tree_rad)
# write_fds_input2("tree_test1", t1)
# print("")
#
# t2 = fds_lollipop_tree(4.0, 4.0, 1.0, dht, tree_height, tree_rad)
# write_fds_input2("tree_test2", t2)
# print("")


# ###################
# ###################
# t1 = ["line 1", "line 2", "line 3"]
#
#
# with open("writetest.txt", "w") as f:
#     for l in t1:
#         f.write("%s\n" % l)
# f.close()
#
# with open("writetest.txt", "a") as f:
#     f.write("%s\n" % "line 4")
#
# f.close()
#
# with open("writetest.txt", "a") as f:
#     f.write("%s\n" % "line 5")
# f.close()
# ###################
# ###################


# #######################
# ### Lower Pipe
# for t in bl:
#     nstr = "&OBST XB = {}, {}, {}, {}, {}, {} /".format(t[0], t[1],
#                                                         t[2], t[3],
#                                                         t[4], t[5])
#     print(nstr)
#
# print("")
#
#
# #######################
# ### Upper Pipe
# cl2, bl2 = circle_raster(radius, dh, zm=0.013, height=0.02)
#
# for t in bl2:
#     nstr = "&OBST XB = {}, {}, {}, {}, {}, {} /".format(t[0], t[1],
#                                                         t[2], t[3],
#                                                         t[4], t[5])
#     print(nstr)
#
# print("")
#
#
# #######################
# ### Lower VENT
#
# cl3, bl3 = circle_raster(radius, dh, zm=0.0, height=0.00)
#
# for t in bl3:
#     nstr = "&VENT XB = {}, {}, {}, {}, {}, {}" \
#            ", COLOR='RASPBERRY', SURF_ID='BURNER' /".format(t[0], t[1],
#                                                             t[2], t[3],
#                                                             t[4], t[5])
#     print(nstr)
#
# print("")
#
#
# #######################
# ### Upper VENT
#
# cl4, bl4 = circle_raster(radius, dh, zm=0.013, height=0.00)
#
# for t in bl4:
#     nstr = "&VENT XB = {}, {}, {}, {}, {}, {}" \
#            ", COLOR='BLUE', SURF_ID='OXIDISER' /".format(t[0], t[1],
#                                                          t[2], t[3],
#                                                          t[4], t[5])
#     print(nstr)
#
# print("")
#
#
# # for coord in cl:
# #     plt.plot(coord[0], coord[1], marker='o')
# #
# #
# # # Check if it is a circle.
# # t = np.arange(0, np.pi/2, 0.1)
# # for j in t:
# #     plt.plot(np.cos(j), np.sin(j), marker='.')
# #
# # plt.xticks(np.arange(0, 1.1, step=dh))
# # plt.yticks(np.arange(0, 1.1, step=dh))
# # plt.xlim(-0.05, 1.05)
# # plt.ylim(-0.05, 1.05)
# # plt.grid()
# # plt.show()

