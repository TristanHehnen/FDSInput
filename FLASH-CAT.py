def combustible_mass_pua(n_cables, combustible_fraction, residue_yield,
                      mass_length=1.0, tray_width=0.45):
    """
    Formula 9-2 from CHRISTIFIRE Phase 1 (NUREG/CR-7010, Vol. 1), p. 148
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
    Formula 9-1 from CHRISTIFIRE Phase 1 (NUREG/CR-7010, Vol. 1), p. 148
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