import numpy as pd


#################
# FDS OBJECTS CLASS
class FDSObjects:
    def __init__(self):
        a = 'toast'

    def mesh(self):
        m2 = '&MESH IJK=90,36,38, XB=-1.0,8.0,-1.8,1.8,0.0,3.82 /'
        m3 = '&MESH IJK={},{},{}, XB={},{},{},{},{},{} /'
        m = '&MESH IJK={},{},{}, {}'.format()


#################
# FDS MESH CLASS
class FDSMesh:
    def __init__(self, loc_x=None, loc_y=None, loc_z=None,
                 len_x=None, len_y=None, len_z=None,
                 len_x1=None, len_x2=None,
                 len_y1=None, len_y2=None,
                 len_z1=None, len_z2=None,):

        self.loc_x = loc_x, self.loc_y = loc_y, self.loc_z = loc_z,
        self.len_x = len_x, self.len_y = len_y, self.len_z = len_z,
        self.len_x1 = len_x1, self.len_x2 = len_x2,
        self.len_y1 = len_y1, self.len_y2 = len_y2,
        self.len_z1 = len_z1, self.len_z2 = len_z2

    def mesh(self):
        # Initialise the location of the objects origin.
        if self.loc_x is None:
            self.loc_x = 0.0

        if self.loc_y is None:
            self.loc_y = 0.0
        if self.loc_z is None:
            self.loc_z = 0.0

        # Set default size if none is provided.
        if self.len_x is None:
            self.len_x = 1.0
        if self.len_y is None:
            self.len_y = 1.0
        if self.len_z is None:
            self.len_z = 1.0

        # Calculate objects dimensions, based on size and location.
        x1 = self.len_x1 + self.loc_x
        x2 = self.len_x2 + self.loc_x
        y1 = self.len_y1 + self.loc_y
        y2 = self.len_y2 + self.loc_y
        z1 = self.len_z1 + self.loc_z
        z2 = self.len_z2 + self.loc_z

        bx1 = BoxShape(x1, x2, y1, y2, z1, z2)
        m = '&MESH IJK={},{},{}, {}'.format(10, 10, 10, bx1)
        print(m)


#################
# FDS DOMAIN CLASS
class FDSDomain:
    def __init__(self,
                 loc_x=None, loc_y=None, loc_z=None,
                 len_x=None, len_y=None, len_z=None,
                 len_x1=None, len_x2=None,
                 len_y1=None, len_y2=None,
                 len_z1=None, len_z2=None):
        self.loc_x = loc_x, self.loc_y = loc_y, self.loc_z = loc_z,
        self.len_x = len_x, self.len_y = len_y, self.len_z = len_z,
        self.len_x1 = len_x1, self.len_x2 = len_x2,
        self.len_y1 = len_y1, self.len_y2 = len_y2,
        self.len_z1 = len_z1, self.len_z2 = len_z2,

        a = 'toast'


#################
# BOX SHAPE CLASS
class BoxShape:
    def __init__(self, box_x1=0.0, box_y1=0.0, box_z1=0.0, box_x2=1.0,
                 box_y2=1.0, box_z2=1.0):
        self.box_x1 = box_x1
        self.box_x2 = box_x2
        self.box_y1 = box_y1
        self.box_y2 = box_y2
        self.box_z1 = box_z1
        self.box_z2 = box_z2

    def get_box(self):
        box = 'XB={},{},{},{},{},{}'.format(self.box_x1, self.box_x2,
                                            self.box_y1, self.box_y2,
                                            self.box_z1, self.box_z2)
        return box


#################
# SURFACE CLASS
class Surf:
    def __init__(self, surf_id='id'):
        self.surf_id = surf_id

    def get_surf(self):
        if self.surf_id is 'id':
            surf = "SURF_ID='INERT'"
        return surf


#################
# OBSTRUCTION CLASS
class Obst:
    def __init__(self, pos_x=0.0, pos_y=0.0, pos_z=0.0,
                 len_x=1.0, len_y=1.0, len_z=1.0):

        # Starting point.
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)
        self.pos_z = float(pos_z)

        # Edge length.
        self.len_x = float(len_x)
        self.len_y = float(len_y)
        self.len_z = float(len_z)

    def get_obst(self):
        # Calculate dimensions and position of the obstruction.
        # Start.
        x1 = self.pos_x
        y1 = self.pos_y
        z1 = self.pos_z

        # End.
        x2 = self.pos_x + self.len_x
        y2 = self.pos_y + self.len_y
        z2 = self.pos_z + self.len_z

        # Create box shape of obstruction.
        bx1 = BoxShape(x1, x2,
                       y1, y2,
                       z1,  z2)

        # Attach surface to obstruction.
        sf1 = Surf()

        # Finalise obstruction for FDS input file.
        obst = "&OBST {}, {} /".format(bx1.get_box(), sf1.get_surf())

        return obst


def test_boxshape():
    bx1 = BoxShape(0.0, 0.0, 0.0, 5.0, 2.0, 3.0)
    print(bx1.get_box())


test_boxshape()


# fm = FDSMesh(1.0, 2.0, 1.0)
# print(fm.mesh())

def test_obst():
    obst1 = Obst(1, 1, 1)
    print(obst1.get_obst())

test_obst()
