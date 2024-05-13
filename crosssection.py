import numpy as np
import matplotlib.pyplot as plt


def crosssection_cPipes(
        diam_cond,
        cond_thickness,
        material,
        iso_thickness,
        casing_thickness,
        dim_pol = None,
        dim_tor = None,
        windings_pol = None,
        windings_tor = None,
        optimize_dims = True,
        draw = True,
        roughness = 0.0015
):
    """
    creates the cross section for circular tubes
    """
    diam_tot = diam_cond + 2 * iso_thickness
    if windings_pol and windings_tor and dim_pol and dim_tor:
        raise Exception("system is over defined, either give number of windings (pol, tor), or the dimensions (pol, tor)")
    if windings_pol and windings_tor:
        dim_pol = windings_pol * diam_tot
        dim_tor = windings_tor * diam_tot
    elif dim_pol or dim_tor:
        windings_pol = np.floor(dim_pol / diam_tot)
        windings_tor = np.floor(dim_tor / diam_tot)
        if optimize_dims:
            dim_pol = windings_pol * diam_tot
            dim_tor = windings_tor * diam_tot
    else:
        raise Exception("system is under defined, you need to give either windings (pol, tor) or dimensions (pol, tor)")
    diam_water = diam_cond - 2 * cond_thickness
    p_loss_pm =
    if draw:

    return dim_pol, dim_tor, windings_pol, windings_tor, p_loss_pm