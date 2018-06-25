import numpy as np


def calc_mesh_geo(array, cell_x, cell_y=None, cell_z=None, origin=None):
    """
    Calculates the geometrical mesh dimensions based on cell amount and cell
    size.

    :param array: A Numpy array that contains geometrical information on the
        mesh.
    :param cell_x: Edge length of the cell in x-direction.
    :param cell_y: Edge length of the cell in y-direction.
    :param cell_z: Edge length of the cell in z-direction.
    :param origin: Origin point of the mesh as a list: [x, y, z].

    :return:
    """

    # Set mesh origin.
    if origin is None:
        origin = [0, 0, 0]

    # Set cell sizes per axis, if no values are provided all defaults to the
    # cell size in x-direction.
    if cell_y is None:
        cell_y = cell_x
    if cell_z is None:
        cell_z = cell_x

    # Determine the overall mesh size from the np.array shape.
    # Initialise cell numbers for each direction in the mesh. Thus, minimum
    # cell number for each direction is 1.
    mesh_cells = [1, 1, 1]

    # Adjust cell amount depending on the array size.
    for idx, val in enumerate(array.shape):
        mesh_cells[idx] = val

    # Calculate start (1) and end (2) point of the mesh
    mesh_x1 = float(origin[0])
    mesh_x2 = float(origin[0]) + cell_x * mesh_cells[0]

    mesh_y1 = float(origin[1])
    mesh_y2 = float(origin[1]) + cell_y * mesh_cells[1]

    mesh_z1 = float(origin[2])
    mesh_z2 = float(origin[2]) + cell_z * mesh_cells[2]

    # Collect all geometry information of the mesh
    mesh_info = [mesh_cells, mesh_x1, mesh_x2, mesh_y1, mesh_y2, mesh_z1,
                 mesh_z2]

    return mesh_info


def create_mesh(mesh_info, digits=2, mesh_id="'Mesh_01'",
                mpi_proc=None, threads=None):
    """
    This function creates the input line for FDS, which describes how a mesh
    is to be set up. The result will be a string.

    :param mesh_info: Geometrical information of the mesh, cells and physical
        dimension.
    :param digits: Number of decimal places to be written.
    :param mesh_id: Human-readable mesh ID for referencing.
    :param mpi_proc: Allows to control which MPI process this mesh should be
        assigned to, see FDS User Guide.
    :param threads: Sets number of threads this mesh gets, see FDS User Guide.

    :return: Line for FDS input file, as string.
    """

    # Set number of decimal places.
    prec = "%.{}f".format(digits)

    # Set mesh id.
    m_id = "ID = {}".format(mesh_id)

    # Set number of cells for each direction (mesh resolution).
    ijk = 'IJK = {}, {}, {}'.format(mesh_info[0][0], mesh_info[0][1],
                                    mesh_info[0][2])

    # Set mesh coordinates.
    xb = 'XB = {}, {}, {}, {}, {}, {}' \
         ''.format(prec % mesh_info[1], prec % mesh_info[2],
                   prec % mesh_info[3], prec % mesh_info[4],
                   prec % mesh_info[5], prec % mesh_info[6])

    # Which MPI process this mesh is assigned to.
    if mpi_proc is not None:
        m_p = ", MPI_PROCESS={}".format(mpi_proc)
    else:
        m_p = ""

    # Number of threads, to be used by FDS when calculating this mesh.
    if threads is not None:
        n_t = ", N_THREADS={}".format(threads)
    else:
        n_t = ""

    # Collect information and create FDS input line.
    m = '&MESH {}, {}, {}{}{} /'.format(m_id, ijk, xb, m_p, n_t)

    return m


def calc_obst_geo(mesh_info):
    """
    Takes values other than 0 and calculates the geometry of the obstructions.

    :param mesh_info:
    :return:
    """

    print("\nObstructions"
          "\n---------")
    for row in mesh_info[:4]:
        print("Row content:\n", row)

        for element in row:
            if element == 1:
                print(element)

    pass


###################
#
delta_x = 0.1

a = np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 0, 1, 0],
              [0, 0, 0, 0, 0, 1, 0],
              [0, 0, 1, 1, 0, 1, 0]])

print(a.shape)

mesh_geo = calc_mesh_geo(a, delta_x)

print(create_mesh(mesh_geo))

calc_obst_geo(a)
