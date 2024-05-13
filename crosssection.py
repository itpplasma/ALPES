import numpy as np
import matplotlib.pyplot as plt
#import pressure_loss_calculator.PressureLossMod as pl

def crosssection_cPipes(
        diam_cond,
        cond_thickness,
        material,
        iso_thickness,
        casing_thickness,
        mass_flow,
        dim_pol = None,
        dim_tor = None,
        windings_pol = None,
        windings_tor = None,
        optimize_dims = True,
        draw = True,
        temperature = 90,
        roughness = 0.0015
):
    """
    creates the cross section for circular tubes
    """
    walls = 2 * casing_thickness
    diam_tot = diam_cond + (2 * iso_thickness)
    if windings_pol and windings_tor and dim_pol and dim_tor:
        raise Exception("system is over defined, either give number of windings (pol, tor), or the dimensions (pol, tor)")
    if windings_pol and windings_tor:
        dim_pol = (windings_pol * diam_tot) + walls
        dim_tor = (windings_tor * diam_tot) + walls
    elif dim_pol or dim_tor:
        windings_pol = np.floor((dim_pol - walls) / diam_tot)
        windings_tor = np.floor((dim_tor - walls) / diam_tot)
        if optimize_dims:
            dim_pol = windings_pol * diam_tot + walls
            dim_tor = windings_tor * diam_tot + walls
    else:
        raise Exception("system is under defined, you need to give either windings (pol, tor) or dimensions (pol, tor)")
    diam_water = diam_cond - 2 * cond_thickness
    #p_loss_pm = pl.PressureLoss_DW(1, diam_water, mass_flow, temperature, roughness)
    if draw:
        fig, ax = plt.subplots()
        fig.set_size_inches(dim_pol, dim_tor)
        ax.patch.set_edgecolor('black')
        ax.patch.set_linewidth(casing_thickness)
        for i in range(windings_tor):
            for k in range(windings_pol):
                x = i * diam_tot
                y = k * diam_tot
                iso = plt.Circle((x + diam_tot, y + diam_cond + diam_tot), (diam_cond / 2) + iso_thickness, color='g')
                cond = plt.Circle((x + diam_tot, y + diam_cond + diam_tot), diam_cond / 2, color='r')
                water = plt.Circle((x + diam_tot, y + diam_cond + diam_tot), diam_water / 2, color='b')
                ax.add_patch(iso)
                ax.add_patch(cond)
                ax.add_patch(water)
        ax.set_xlim(0, dim_pol)
        ax.set_ylim(0, dim_tor)
        plt.tight_layout()
        plt.grid()
        plt.axis('equal')
        plt.show()
    return dim_pol, dim_tor, windings_pol, windings_tor#, p_loss_pm

dim_pol, dim_tor, windings_pol, windings_tor = crosssection_cPipes(4, 1, "copper", 0.5, 1, 10,
                                                                              windings_pol=5, windings_tor=5)


