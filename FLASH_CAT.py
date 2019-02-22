import numpy as np


def combustible_mass_pua(n_cables, combustible_fraction, residue_yield,
                         mass_length=0.18056, tray_width=0.45):
    """
    Formula 9-3 from CHRISTIFIRE Phase 1 (NUREG/CR-7010, Vol. 1), p. 148
    Calculates the combustible mass per unit area of a cable tray.

    :param n_cables: Number of cables per tray, dimensionless.
    :param combustible_fraction: Fraction of combustible (non-metallic)
        material per cable, dimensionless.
    :param residue_yield: Amount of residue left, dimensionless.
    :param mass_length: Mass per length of cable, in kg/m. Default is cable 219.
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

    :return: New length of burning surface.
    """

    new_length = burning_length + 2 * vertical_distance * np.tan(spread_angle)
    return new_length


def igniton_time(location, burning_length, spread_rate, tray_ignition):
    """
    Calculates the ignition time of a given location of the tray. The
    `tray_ignition` is the time when the tray ignites first.

    :param location: A given location of the tray.
    :param burning_length: Length of the already burning part of the tray.
    :param spread_rate: Rate at which the fire propagates along the tray.
    :param tray_ignition: Time at which the tray ignites.

    :return: Time at which a given part of the tray ignites.
    """

    ignition_time = tray_ignition + ((location - burning_length/2)/spread_rate)
    return ignition_time


def total_err(time):
    return


def average_hrrpua(tp_fraction, tp_hrrpua=250, ts_hrrpua=150):
    """
    This calculates the average heat release rates per unit area for cable
    trays with mixed cables. Cables are assumed to be split between
    "thermoset" (ts) and "thermoplastic" (tp) cables with hrrpua values of
    250 kW/m2 and 150 kW/m2 respectively. Values are suggested by NUREG/CR-6850.

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
        the cable. Expected to be an numpy array.
    :param linear_cable_mass: Mass of the whole cable per unit length,
        in kg/m. Expected to be an numpy array.

    :return: Average value of cable mass, in kg/m.
    """

    intermediate = np.sum(plastic_fraction * linear_cable_mass)
    avg_mass = intermediate/np.sum(linear_cable_mass)
    return avg_mass


def idealised_hrrpua(peak_hrr, duration):
    """
    Creates a simple hrrpua profile as a trapezoid, consisting of four data
    points.

    :param peak_hrr: Heat release rate value of the input data which is used
        as a constant value.
    :param duration: Duration of the test or time series.

    :return: List of lists, containing four data points forming a trapezoid
        as a heat release ramp.
    """

    ramp = duration/6
    time = [0, ramp, duration - ramp, duration]
    hrr = [0, peak_hrr, peak_hrr, 0]
    data_series = [time, hrr]
    return data_series


def delta_t(cell_size, spread_rate=3.2, hours=True):
    """
    Calculates the time the fire spreads along a linear fuel bed,
    like cables, in which it would traverse a cell width of the fluid cells.
    This is used to determine when the VENT in the adjacent cells is to be
    activated, due to fire spread.

    :param spread_rate: Time in which the fire propagates linearly over a
        unit length, in m/h. Default is 3.2 m/h for thermoplastic cable from
        findings of NUREG/CR-6850.
    :param cell_size: Cell size, or edge length, of cube-shaped CFD cells,
        e.g. for FDS, in millimeter.
    :param hours: Flag if the spread rate is provided per hour, else seconds
        are assumed.

    :return: Time needed to traverse a distance of one cell size,
    in seconds.
    """

    if hours is True:
        factor = 3600
    else:
        factor = 1

    delta = cell_size / spread_rate * factor

    return delta
