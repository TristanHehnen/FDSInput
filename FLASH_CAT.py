import numpy as np


def combustible_mass_pua(n_cables, combustible_fraction, residue_yield,
                         mass_length=1.0, tray_width=0.45):
    """
    Formula 9-3 from CHRISTIFIRE Phase 1 (NUREG/CR-7010, Vol. 1), p. 148
    Calculates the combustible mass per unit area of a cable tray.

    :param n_cables: Number of cables per tray, dimensionless.
    :param combustible_fraction: Fraction of combustible (non-metallic)
        material per cable, dimensionless.
    :param residue_yield: Amount of residue left, dimensionless.
    :param mass_length: Mass per length of cable, in g/m.
    :param tray_width: Width of the tray, in m.

    :return: Combustible mass per unit area per tray, in g/m^2.
    """

    m_comb = 1 - residue_yield
    m_l = (n_cables * combustible_fraction * m_comb * mass_length)
    m_c_pua = m_l / tray_width

    return m_c_pua


def fire_duration(comb_mass_pua, hoc, hrrpua_avg):
    """
    Formula 9-2 from CHRISTIFIRE Phase 1 (NUREG/CR-7010, Vol. 1), p. 148
    Calculates the fire duration of a given location.

    Note that the fraction 5/6 is a result of the fact that the average heat
    release rate per unit area is based on 80 % of the total energy release.

    :param comb_mass_pua: combustible mass per unit area.
    :param hoc: heat of combustion.
    :param hrrpua_avg: average heat release rate per unit area.

    :return: fire duration.
    """

    duration = (comb_mass_pua * hoc) / ((5 * hrrpua_avg) / 6)

    return duration


def horizontal_burning_area(vertical_distance, burning_length,
                            spread_angle=35):
    """
    Formula 9-1 from CHRISTIFIRE Phase 1 (NUREG/CR-7010, Vol. 1), p. 147
    Calculates the burning rate by the burning surface area.

    The fire is assumed to be distributed uniformly over the tray width and
    spreads only along the tray, away from the fire seat. Due to preheating
    of the upper trays, the burning area forms a V-shape of propagating flame
    and extinction fronts. Affected surface depends on the vertical distance
    between trays.

    :param vertical_distance: Vertical separation between the trays.
    :param burning_length: Length of the tray that is already burning,
        assuming uniform behaviour over the tray width.
    :param spread_angle: Spread angle of how the flame fronts propagate down
        the tray. The angle of 35° is based on observations of experiments
        documented in NUREG/CR-6850.

    :return:
    """

    new_length = burning_length + 2 * vertical_distance * np.tan(spread_angle)
    return new_length


def tray_igniton_time(distance):
    pass


def total_err(time):
    pass


def average_hrrpua(tp_fraction, tp_hrrpua=250, ts_hrrpua=150):
    """
    This calculates the average heat release rates per unit area for cable
    trays with mixed cables. Cables are assumed to be split between
    "thermoset" and "thermoplastic" cables with hrrpua values of 250 kW/m2
    and 150 kW/m2 respectively. Values are suggested by NUREG/CR-6850.

    :param tp_fraction: Fraction of thermoplastic cables, e.g. 0.3.
    :param tp_hrrpua: Heat release rate per unit area from NUREG/CR-6850 for
        thermoplastic cables: 250 kW/m2
    :param ts_hrrpua: Heat release rate per unit area from NUREG/CR-6850 for
        thermoset cables: 150 kW/m2

    :return: Averaged heat release rate per unit area.
    """

    ts_fraction = 1 - tp_fraction
    avg_hrrpua = (ts_fraction * ts_hrrpua) + (tp_fraction * tp_hrrpua)
    return avg_hrrpua


def average_cable_mass(plastic_fraction, linear_cable_mass):
    """
    Calculates the averaged cable mass per unit length.

    :param plastic_fraction: Fraction of plastic material per unit length of
        the cable.
    :param linear_cable_mass: Mass of the whole cable per unit length, in kg/m.

    :return: Average value of cable mass, in kg/m.
    """
    
    intermediate = np.sum(plastic_fraction * linear_cable_mass)
    avg_mass = intermediate/np.sum(linear_cable_mass)
    return avg_mass
