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
    """
    Container class for FDS objects, like obstructions, vents, devices, ...
    """

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
    """
    Container class for meshes.
    """

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
    """
    Provide the basic box shape for FDS entities.
    """

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
    """
    Container for surface information of obstructions in FDS.
    """
    def __init__(self, surf_id='id'):
        self.surf_id = surf_id

    def get_surf(self):
        if self.surf_id is 'id':
            surf = "SURF_ID='INERT'"
        else:
            surf = "SURF_ID='INERT'"
        return surf


#################
# OBSTRUCTION CLASS
class Obst:
    """
    Set size and position of an obstruction in FDS.
    """
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


#################
# SURFACE CLASS
class FDSSURF:
    surf_temp = {'init': "&SURF ID = '{}'",
                 'ext_flux': "EXTERNAL_FLUX = {}",
                 'rgb': "RGB = {}",
                 'tga_analysis': "TGA_ANALYSIS = .{}.",
                 'tga_heat_rate': "TGA_HEATING_RATE = {}",
                 'tga_fin_temp': "TGA_FINAL_TEMPERATURE = {}",
                 'backing': "BACKING = '{}'",
                 'cell_size_fac': "CELL_SIZE_FACTOR = {}",
                 'burn_away': "BURN_AWAY = .{}.",
                 'layer_div': "LAYER_DIVIDE = {}",
                 'thickness': "THICKNESS({}) = {}",
                 'matl_id': "MATL_ID({}) = {}",
                 'matl_mass_frac': "MATL_MASS_FRACTION({}) = {}", }

    def __init__(self, init, ext_flux=None, rgb=None,
                 tga_analysis=None, tga_heat_rate=None,
                 tga_fin_temp=None, backing=None,
                 cell_size_fac=None, burn_away=None,
                 layer_div=None, thickness=None, matl_id=None,
                 matl_mass_frac=None, ):

        self.init = init
        self.ext_flux = ext_flux
        self.rgb = rgb
        self.tga_analysis = tga_analysis
        self.tga_heat_rate = tga_heat_rate
        self.tga_fin_temp = tga_fin_temp
        self.backing = backing
        self.cell_size_fac = cell_size_fac
        self.burn_away = burn_away
        self.layer_div = layer_div
        self.thickness = thickness
        self.matl_id = matl_id
        self.matl_mass_frac = matl_mass_frac

        self.param_base = [['init', self.init],
                           ['ext_flux', self.ext_flux],
                           ['rgb', self.rgb],
                           ['tga_analysis', self.tga_analysis],
                           ['tga_heat_rate', self.tga_heat_rate],
                           ['tga_fin_temp', self.tga_fin_temp],
                           ['backing', self.backing],
                           ['cell_size_fac', self.cell_size_fac],
                           ['burn_away', self.burn_away],
                           ['layer_div', self.layer_div]]  # ,
        # ['thickness', self.thickness],
        # ['matl_id', self.matl_id],
        # ['matl_mass_frac', self.matl_mass_frac],]

        self.param_base_dict = {'init': self.init,
                                'ext_flux': self.ext_flux,
                                'rgb': self.rgb,
                                'tga_analysis': self.tga_analysis,
                                'tga_heat_rate': self.tga_heat_rate,
                                'tga_fin_temp': self.tga_fin_temp,
                                'backing': self.backing,
                                'cell_size_fac': self.cell_size_fac,
                                'burn_away': self.burn_away,
                                'layer_div': self.layer_div}  # ,
        # 'thickness': self.thickness,
        # 'matl_id': self.matl_id,
        # 'matl_mass_frac': self.matl_mass_frac,}

        self.materials = []

        # Attempt to handle cases with only one material.
        self.matl_param_base = [['thickness', self.thickness],
                                ['matl_id', self.matl_id],
                                ['matl_mass_frac', self.matl_mass_frac]]

        for i in self.matl_param_base:
            if i[1] is not None:
                self.add_material(self.thickness,
                                  self.matl_id,
                                  self.matl_mass_frac)
                break

    def add_material(self,
                     thickness=None,
                     matl_id=None,
                     matl_mass_frac=None):

        self.thickness = thickness
        self.matl_id = matl_id
        self.matl_mass_frac = matl_mass_frac

        new_matl = {'thickness': self.thickness,
                    'matl_id': self.matl_id,
                    'matl_mass_frac': self.matl_mass_frac}

        self.materials.append(new_matl)

    def compile_surf(self, show=False):
        surf_lines = []
        num_matl = len(self.materials)
        print(self.materials)
        matl_count = 1

        for component in self.param_base[:]:
            idfr = '{}'.format(component[0])

            if self.param_base_dict[idfr] is not None:
                comp = self.surf_temp[idfr]
                if component[0] is not 'init':
                    comp = '      ' + comp

                new_c = comp.format(self.param_base_dict[idfr])
                # print(new_c)
                surf_lines.append(new_c + ',')

        thick_comp = "{}, "
        id_list = []
        mass_frac_list = []
        comp_id_temp = '{},{}:{}'
        matl_comp_count = 1
        thicknesses = ''

        # Add different materials.
        for matl_dict in self.materials:
            print('len matl_dict', len(self.materials))

            # Check if material(s) are provided, by using the existance
            # of thickness as an indicator.
            idfr = 'thickness'
            if matl_dict[idfr] is not None:
                matl_ids = len(matl_dict['matl_id'])

                # Determine the amount of materials and collect their
                # thicknesses in a single string.
                thick_num = '1:{}'.format(len(self.materials))
                thicknesses += thick_comp.format(matl_dict[idfr])

                # Collect the different material ids
                # for a material components.
                idfr = 'matl_id'
                comp_id = comp_id_temp.format(matl_comp_count,
                                              '1', matl_ids)
                ml = ''
                for md in matl_dict[idfr]:
                    ml += "'{}', ".format(md)
                ml = ml[:-2]
                new_c = "      " + self.surf_temp[idfr].format(comp_id,
                                                               ml)
                id_list.append(new_c)

                # Collect the different mass fractions
                # for the material components.
                idfr = 'matl_mass_frac'
                comp_id = comp_id_temp.format(matl_comp_count,
                                              '1', matl_ids)
                mf = ''
                for md in matl_dict[idfr]:
                    mf += "'{}', ".format(md)
                mf = mf[:-2]
                new_c = "      " + self.surf_temp[idfr].format(comp_id,
                                                               mf)
                mass_frac_list.append(new_c)

                matl_comp_count += 1

        # Create the thickness input line.
        new_thick = "      " + self.surf_temp['thickness'].format(thick_num,
                                                                  thicknesses[
                                                                  :-1])
        surf_lines.append(new_thick)

        # Append the various material id lines.
        for m_id in id_list:
            surf_lines.append(m_id + ',')

        # Append the various material mass fraction lines.
        for m_fr in mass_frac_list:
            surf_lines.append(m_fr + ',')

        # Remove the last comma.
        surf_lines[-1] = surf_lines[-1][:-1] + ' /\n'

        # Print results to the screen, if desired.
        if show is True:
            for line in surf_lines:
                print(line)

        return surf_lines


#################
# MATERIAL CLASS
class FDSMATL:
    matl_temp = {'init': "&MATL ID = '{}'",
                 'density': "DENSITY = {}",
                 'emissivity': "EMISSIVITY = {}",
                 'conductivity': "CONDUCTIVITY = {}",
                 'specific_heat': "SPECIFIC_HEAT = {}",
                 'n_reactions': "N_REACTIONS = {}",
                 'a': "A({}) = {}",
                 'e': "E({}) = {}",
                 'n_s': "N_S({}) = {}",
                 'nu_matl': "NU_MATL({}) = {}",
                 'matl_id': "MATL_ID({}) = '{}'",
                 'nu_spec': "NU_SPEC({}) = {}",
                 'spec_id': "SPEC_ID({}) = '{}'",
                 'heat_of_comb': "HEAT_OF_COMBUSTION({}) = {}",
                 'heat_of_reac': "HEAT_OF_REACTION({}) = {}"}

    def __init__(self, init, density=None, emissivity=None,
                 conductivity=None, specific_heat=None,
                 a=None, e=None, n_s=None, nu_matl=None,
                 matl_id=None, nu_spec=None, spec_id=None,
                 heat_of_comb=None, heat_of_reac=None):

        self.init = init
        self.density = density
        self.emissivity = emissivity
        self.conductivity = conductivity
        self.specific_heat = specific_heat
        self.n_reactions = None
        self.a = a
        self.e = e
        self.n_s = n_s
        self.nu_matl = nu_matl
        self.matl_id = matl_id
        self.nu_spec = nu_spec
        self.spec_id = spec_id
        self.heat_of_comb = heat_of_comb
        self.heat_of_reac = heat_of_reac

        self.param_base = [['init', self.init],
                           ['emissivity', self.emissivity],
                           ['density', self.density],
                           ['conductivity', self.conductivity],
                           ['specific_heat', self.specific_heat]]  # ,
        # ['heat_of_comb', self.heat_of_comb],
        # ['heat_of_reac', self.heat_of_reac]]

        self.param_base_dict = {'init': self.init,
                                'emissivity': self.emissivity,
                                'density': self.density,
                                'conductivity': self.conductivity,
                                'specific_heat': self.specific_heat}  # ,
        # 'heat_of_comb': self.heat_of_comb,
        # 'heat_of_reac': self.heat_of_reac}

        self.reactions = []

        # Attempt to handle cases with only one reaction.
        self.reac_param_base2 = [['a', self.a],
                                 ['e', self.e],
                                 ['n_s', self.n_s],
                                 ['nu_matl', self.nu_matl],
                                 ['matl_id', self.matl_id],
                                 ['nu_spec', self.nu_spec],
                                 ['spec_id', self.spec_id],
                                 ['heat_of_comb', self.heat_of_comb],
                                 ['heat_of_reac', self.heat_of_reac]]
        self.reac_param_base = [self.a, self.e, self.n_s,
                                self.nu_matl, self.matl_id, self.nu_spec,
                                self.spec_id, self.heat_of_comb,
                                self.heat_of_reac]
        for i in self.reac_param_base:
            if i is not None:
                self.add_reaction(self.a, self.e, self.n_s,
                                  self.nu_matl, self.matl_id, self.nu_spec,
                                  self.spec_id, self.heat_of_comb,
                                  self.heat_of_reac)
                break

    def add_reaction(self, a=None, e=None, n_s=None,
                     nu_matl=None, matl_id=None, nu_spec=None,
                     spec_id=None, heat_of_comb=None,
                     heat_of_reac=None):

        self.a = a
        self.e = e
        self.n_s = n_s
        self.nu_matl = nu_matl
        self.matl_id = matl_id
        self.nu_spec = nu_spec
        self.spec_id = spec_id
        self.heat_of_comb = heat_of_comb
        self.heat_of_reac = heat_of_reac

        new_reac = {'a': self.a,
                    'e': self.e,
                    'n_s': self.n_s,
                    'nu_matl': self.nu_matl,
                    'matl_id': self.matl_id,
                    'nu_spec': self.nu_spec,
                    'spec_id': self.spec_id,
                    'heat_of_comb': self.heat_of_comb,
                    'heat_of_reac': self.heat_of_reac}

        self.reactions.append(new_reac)

    def compile_matl(self, show=False):
        matl_lines = []
        num_reac = len(self.reactions)
        reac_count = 1

        for component in self.param_base[:]:
            idfr = '{}'.format(component[0])

            if self.param_base_dict[idfr] is not None:
                comp = self.matl_temp[idfr]
                if component[0] is not 'init':
                    comp = '      ' + comp

                new_c = comp.format(self.param_base_dict[idfr])
                # print(new_c)
                matl_lines.append(new_c + ',')

        if num_reac is not 0:
            # print('no reac')
            new_c = "      " + self.matl_temp['n_reactions'].format(num_reac)
            matl_lines.append(new_c + ',')

        for reac_dict in self.reactions:

            for reac_para in self.reac_param_base2:
                idfr = '{}'.format(reac_para[0])

                if reac_dict[idfr] is not None:
                    new_c = "      " + self.matl_temp[idfr].format(reac_count,
                                                                   reac_dict[
                                                                       idfr])
                    matl_lines.append(new_c + ',')
            reac_count += 1

        # #         for component in self.param_base[-2:]:
        # #             idfr = '{}'.format(component[0])

        #             if self.param_base_dict[idfr] is not None:
        #                 comp = self.matl_temp[idfr]
        #                 if component[0] is not 'init':
        #                     comp = '      ' + comp

        #                 new_c = comp.format(reac_count,
        #                                     self.param_base_dict[idfr])
        #                 #print(new_c)
        #                 matl_lines.append(new_c + ',')

        #         new_c = "      " + self.matl_temp['n_reactions'].format(num_reac)
        #         matl_lines.append(new_c + ',')

        matl_lines[-1] = matl_lines[-1][:-1] + ' /\n'

        if show is True:
            for line in matl_lines:
                print(line)

        return matl_lines

    #     def compile_matl(self, show=False):
    #         matl_lines = []

    #         for component in self.mp:
    #             idfr = '{}'.format(component)

    #             if self.mp[idfr] is not None:
    #                 comp = self.matl_temp[idfr]
    #                 if component is not 'init':
    #                     comp = '      ' + comp

    #                 new_c = comp.format(self.mp[idfr])+','
    #                 #print(new_c)
    #                 matl_lines.append(new_c)

    #         matl_lines[-1] = matl_lines[-1][:-1] + ' /'

    #         if show is True:
    #             for line in matl_lines:
    #                 print(line)

    #         return matl_lines

    def show_reactions(self):

        string_temp = "  {}: {}\n"
        reac_out = '\n' \
                   '* Reactions overview:\n' \
                   '  Total: {} reaction(s)\n'.format(len(self.reactions))

        for i in range(len(self.reactions)):
            reac_out += '\n' \
                        '* Reaction: {}\n' \
                        '  Parameter: value\n' \
                        '------------------\n'.format(i + 1)

            for j in self.reactions[i]:
                reac_out += string_temp.format(j, self.reactions[i][
                    '{}'.format(j)])

        reac_out += '------------------\n\n'
        print(reac_out)

    def __str__(self):
        """
        Provide complete overview over the parameters and
        values stored within this objects instance.
        """

        string_temp = "  {}: {}\n"
        output = '* Parameter: value\n' \
                 '------------------\n'
        for i in self.param_base_dict:
            output += string_temp.format(i,
                                         self.param_base_dict['{}'.format(i)])

        output += '------------------\n\n'
        return output


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
