import numpy as pd


#################
# FDS DOMAIN CLASS
class FDSDomain:
    """
    Container class for meshes.
    """

    def __init__(self):
        a = 'toast'


#################
# FDS MESH CLASS
class FDSMesh:
    """
    Container class for FDS objects, like obstructions, vents, devices, ...
    """
    def __init__(self):
        a = 'obst'

    def mesh(self):
        m2 = '&MESH IJK=90,36,38, XB=-1.0,8.0,-1.8,1.8,0.0,3.82 /'
        m = '&MESH IJK={},{},{}, XB={},{},{},{},{},{} /'


#################
# FDS OBJECTS CLASS
class FDSObjects:
    def __init__(self, xb, surf='INERT', surf_ids=None):
        self.xb = xb
        self.surf = surf
        self.surf_ids = surf_ids
        a = 'toast'

    def get_obstruction(self):
        obst_surf_id2 = "&OBST XB=2.3,4.5,1.3,4.8,0.0,9.2, SURF_ID='FIRE' /"
        obst_surf_ids2 = "&OBST XB=2.3,4.5,1.3,4.8,0.0,9.2, SURF_IDS='FIRE','INERT','INERT' /"
        obst = '&OBST IJK={},{},{}, XB={},{},{},{},{},{} /'


#################
# BOX SHAPE CLASS
class BoxShape:
    def __init__(self, box_x1=0.0, box_y1=1.0, box_z1=0.0, box_x2=1.0,
                 box_y2=0.0, box_z2=1.0):
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


bx1 = BoxShape(0.0, 2.0, 0.0, 5.0, 0.0, 3.0)
print(bx1.get_box())
