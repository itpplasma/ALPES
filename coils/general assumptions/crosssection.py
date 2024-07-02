import numpy as np
import matplotlib.pyplot as plt
from variant import *


def crosssection_cPipes(
        diam_cond,
        cond_thickness,
        iso_thickness,
        casing_thickness,
        dim_pol=None,
        dim_tor=None,
        windings_pol=None,
        windings_tor=None,
        optimize_dims=True,
        draw=True,
):
    """
    calculates conductor and water area for circular pipes, given either a dimension or number of windings.
    Also plots the cross sections.
    :param diam_cond: diameter of conductor
    :param cond_thickness: thickness of conductor
    :param iso_thickness: thickness of insulator
    :param casing_thickness: thickness of casing, surrounding winding pack
    :param dim_pol: total dimension of coil in poloidal direction
    :param dim_tor: total dimension of coil in toroidal direction
    :param windings_pol: number of windings in poloidal direction
    :param windings_tor: number of windings in toroidal direction
    :param optimize_dims: If True, dimensions of coil are optimized to exactly fit the windings
    :param draw: If True, plots are created and saved
    :return: dim_pol, dim_tor, windings_pol, windings_tor, area_cond, area_water
    """
    walls = 2 * casing_thickness
    diam_tot = diam_cond + (2 * iso_thickness)
    if windings_pol and windings_tor and dim_pol and dim_tor:
        raise Exception("system is over defined, either give number of windings (pol, tor), or the dimensions (pol, tor)")
    if windings_pol and windings_tor:
        dim_pol = (windings_pol * diam_tot) + walls
        dim_tor = (windings_tor * diam_tot) + walls
    elif dim_pol or dim_tor:
        windings_pol = int(np.floor((dim_pol - walls) / diam_tot))
        windings_tor = int(np.floor((dim_tor - walls) / diam_tot))
        if optimize_dims:
            dim_pol = windings_pol * diam_tot + walls
            dim_tor = windings_tor * diam_tot + walls
    else:
        raise Exception("system is under defined, you need to give either windings (pol, tor) or dimensions (pol, tor)")
    diam_water = diam_cond - 2 * cond_thickness
    area_water = (diam_water/2)**2 * np.pi
    area_cond = (diam_cond/2)**2 * np.pi - area_water
    if draw:
        offset = diam_tot
        fig, ax = plt.subplots()
        wall_bottom = plt.Rectangle((0, 0), dim_tor, casing_thickness, linewidth=0, edgecolor='0', facecolor='0')
        wall_top = plt.Rectangle((0, dim_pol - casing_thickness), dim_tor, casing_thickness, linewidth=0, edgecolor='0', facecolor='0')
        wall_left = plt.Rectangle((0, 0), casing_thickness, dim_pol, linewidth=0, edgecolor='0', facecolor='0')
        wall_right = plt.Rectangle((dim_tor - casing_thickness, 0), casing_thickness, dim_pol, linewidth=0, edgecolor='0', facecolor='0')
        ax.add_patch(wall_bottom)
        ax.add_patch(wall_top)
        ax.add_patch(wall_left)
        ax.add_patch(wall_right)
        x = 0
        y = 0
        for i in range(windings_tor):
            for k in range(windings_pol):
                x = i * offset - diam_tot / 2 + casing_thickness
                y = k * offset - diam_tot / 2 + casing_thickness
                iso = plt.Circle((x + offset, y + offset), (diam_cond / 2) + iso_thickness, color='g')
                cond = plt.Circle((x + offset, y + offset), diam_cond / 2, color='r')
                water = plt.Circle((x + offset, y + offset), diam_water / 2, color='b')
                ax.add_patch(iso)
                ax.add_patch(cond)
                ax.add_patch(water)
        ax.set(xlim=(0, dim_tor), ylim=(0, dim_pol))
        # ax.set_xticks(np.linspace(0, dim_tor, 10))
        locs, labels = plt.xticks()
        labels = [float(item) / mm for item in locs]
        ax.set_xticks(locs, labels)
        ax.set_xlabel("tor / mm")
        # ax.set_yticks(np.linspace(0, dim_pol, 10))
        locs, labels = plt.yticks()
        labels = [float(item) / mm for item in locs]
        ax.set_yticks(locs, labels)
        ax.set_ylabel("pol / mm")
        plt.tight_layout()
        plt.grid()
        plt.axis('equal')
        plt.savefig(f"{diam_cond/mm}x{cond_thickness/mm}_copperpipe_{windings_pol}x{windings_tor}.png")
    return dim_pol, dim_tor, windings_pol, windings_tor, area_cond, area_water


def crosssection_rPipes(
        diam_cond_pol,
        diam_cond_tor,
        cond_thickness_pol,
        cond_thickness_tor,
        iso_thickness,
        casing_thickness,
        dim_pol=None,
        dim_tor=None,
        windings_pol=None,
        windings_tor=None,
        optimize_dims=True,
        draw=True,
):
    """
    calculates conductor and water area for rectangular pipes, given either a dimension or number of windings.
    Also plots the cross sections.
    :param diam_cond_pol: diameter of conductor in poloidal direction
    :param diam_cond_tor: diameter of conductor in toroidal direction
    :param cond_thickness_pol: conductor thickness in poloidal direction
    :param cond_thickness_tor: conductor thickness in toroidal direction
    :param iso_thickness: insulator thickness
    :param casing_thickness: thickness of casing, surrounding winding pack
    :param dim_pol: total dimension of coil in poloidal direction
    :param dim_tor: total dimension of coil in poloidal direction
    :param windings_pol: windings in poloidal direction
    :param windings_tor: windings in toroidal direction
    :param optimize_dims: If True, dimensions of coil are optimized to exactly fit the windings
    :param draw: If True, plots are created and saved
    :return: dim_pol, dim_tor, windings_pol, windings_tor, area_water, area_cond
    """
    walls = 2 * casing_thickness
    diam_tot_pol = diam_cond_pol + (2 * iso_thickness)
    diam_tot_tor = diam_cond_tor + (2 * iso_thickness)
    if windings_pol and windings_tor and dim_pol and dim_tor:
        raise Exception("system is over defined, either give number of windings (pol, tor), or the dimensions (pol, tor)")
    if windings_pol and windings_tor:
        dim_pol = (windings_pol * diam_tot_pol) + walls
        dim_tor = (windings_tor * diam_tot_tor) + walls
    elif dim_pol or dim_tor:
        windings_pol = int(np.floor((dim_pol - walls) / diam_tot_pol))
        windings_tor = int(np.floor((dim_tor - walls) / diam_tot_tor))
        if optimize_dims:
            dim_pol = windings_pol * diam_tot_pol + walls
            dim_tor = windings_tor * diam_tot_tor + walls
    else:
        raise Exception("system is under defined, you need to give either windings (pol, tor) or dimensions (pol, tor)")
    diam_water_pol = diam_cond_pol - 2 * cond_thickness_pol
    diam_water_tor = diam_cond_tor - 2 * cond_thickness_tor
    area_water = diam_water_tor * diam_water_pol
    area_cond = diam_cond_tor * diam_cond_pol - area_water
    if draw:
        offset_pol = diam_tot_pol
        offset_tor = diam_tot_tor
        fig, ax = plt.subplots()
        wall_bottom = plt.Rectangle((0, 0), dim_tor, casing_thickness, linewidth=0, edgecolor='0', facecolor='0')
        wall_top = plt.Rectangle((0, dim_pol - casing_thickness), dim_tor, casing_thickness, linewidth=0, edgecolor='0', facecolor='0')
        wall_left = plt.Rectangle((0, 0), casing_thickness, dim_pol, linewidth=0, edgecolor='0', facecolor='0')
        wall_right = plt.Rectangle((dim_tor - casing_thickness, 0), casing_thickness, dim_pol, linewidth=0, edgecolor='0', facecolor='0')
        ax.add_patch(wall_bottom)
        ax.add_patch(wall_top)
        ax.add_patch(wall_left)
        ax.add_patch(wall_right)
        x = 0
        y = 0
        for i in range(windings_tor):
            for k in range(windings_pol):
                x = i * offset_tor + casing_thickness
                y = k * offset_pol + casing_thickness
                iso = plt.Rectangle((x, y), diam_cond_tor + 2 * iso_thickness, diam_cond_pol + 2 * iso_thickness, color='g')
                cond = plt.Rectangle((x + iso_thickness, y + iso_thickness), diam_cond_tor, diam_cond_pol, color='r')
                water = plt.Rectangle((x + cond_thickness_tor + iso_thickness, y + cond_thickness_tor + iso_thickness),
                                      diam_water_tor, diam_water_pol, color='b')
                ax.add_patch(iso)
                ax.add_patch(cond)
                ax.add_patch(water)
        ax.set(xlim=(0, dim_tor), ylim=(0, dim_pol))
        ax.set_yticks(np.linspace(0, dim_pol, 10))
        locs, labels = plt.xticks()
        labels = [float(item) / mm for item in locs]
        ax.set_xticks(locs, labels)
        plt.tight_layout()
        plt.grid()
        plt.axis('equal')
        plt.show()
    return dim_pol, dim_tor, windings_pol, windings_tor, area_water, area_cond

def crosssection_umspuelt(
        diam_cond,
        cond_thickness,
        iso_thickness,
        casing_thickness,
        dim_pol=None,
        dim_tor=None,
        windings_pol=None,
        windings_tor=None,
        optimize_dims=True,
        draw=True,
):
    """
    calculates conductor and water area for circular conductors in water, given either a dimension or
    number of windings. Also plots the cross sections.
    :param diam_cond: diameter of conductor
    :param cond_thickness: thickness of conductor
    :param iso_thickness: thickness of insulator
    :param casing_thickness: thickness of casing, surrounding winding pack
    :param dim_pol: total dimension of coil in poloidal direction
    :param dim_tor: total dimension of coil in toroidal direction
    :param windings_pol: number of windings in poloidal direction
    :param windings_tor: number of windings in toroidal direction
    :param optimize_dims: If True, dimensions of coil are optimized to exactly fit the windings
    :param draw: If True, plots are created and saved
    :return: dim_pol, dim_tor, windings_pol, windings_tor, area_cond, area_water
    """
    walls = 2 * casing_thickness
    diam_tot = diam_cond + (2 * iso_thickness)
    if windings_pol and windings_tor and dim_pol and dim_tor:
        raise Exception("system is over defined, either give number of windings (pol, tor), or the dimensions (pol, tor)")
    if windings_pol and windings_tor:
        dim_pol = (windings_pol * diam_tot) + walls
        dim_tor = (windings_tor * diam_tot) + walls
    elif dim_pol or dim_tor:
        windings_pol = int(np.floor((dim_pol - walls) / diam_tot))
        windings_tor = int(np.floor((dim_tor - walls) / diam_tot))
        if optimize_dims:
            dim_pol = windings_pol * diam_tot + walls
            dim_tor = windings_tor * diam_tot + walls
    else:
        raise Exception("system is under defined, you need to give either windings (pol, tor) or dimensions (pol, tor)")
    diam_water = diam_cond - 2 * cond_thickness
    area_water = (diam_water/2)**2 * np.pi
    area_cond = (diam_cond/2)**2 * np.pi - area_water
    if draw:
        print("dim_pol = {}\ndim_tor = {}".format(dim_pol, dim_tor))
        print("diam_cond = {}, cond_thickness = {}, iso_thickness = {}\ndiam_tot = {}".format(diam_cond, cond_thickness,
                                                                                              iso_thickness, diam_tot))
        offset = diam_tot
        fig, ax = plt.subplots()
        #fig.set_size_inches(dim_pol, dim_tor)
        water = plt.Rectangle((0, 0), dim_tor, dim_pol, linewidth=1, facecolor="b", edgecolor="b")
        wall_bottom = plt.Rectangle((0, 0), dim_tor, casing_thickness, linewidth=0, edgecolor='0', facecolor='0')
        wall_top = plt.Rectangle((0, dim_pol - casing_thickness), dim_tor, casing_thickness, linewidth=0, edgecolor='0', facecolor='0')
        wall_left = plt.Rectangle((0, 0), casing_thickness, dim_pol, linewidth=0, edgecolor='0', facecolor='0')
        wall_right = plt.Rectangle((dim_tor - casing_thickness, 0), casing_thickness, dim_pol, linewidth=0, edgecolor='0', facecolor='0')
        ax.add_patch(water)
        ax.add_patch(wall_bottom)
        ax.add_patch(wall_top)
        ax.add_patch(wall_left)
        ax.add_patch(wall_right)
        x = 0
        y = 0
        for i in range(windings_tor):
            for k in range(windings_pol):
                x = i * offset - diam_tot / 2 + casing_thickness
                y = k * offset - diam_tot / 2 + casing_thickness
                iso = plt.Circle((x + offset, y + offset), (diam_cond / 2) + iso_thickness, color='g')
                cond = plt.Circle((x + offset, y + offset), diam_cond / 2, color='r')
                # water = plt.Circle((x + offset, y + offset), diam_water / 2, color='b')
                ax.add_patch(iso)
                ax.add_patch(cond)
        ax.set(xlim=(0, dim_tor), ylim=(0, dim_pol))
        # ax.set_xticks(np.linspace(0, dim_tor, 10))
        locs, labels = plt.xticks()
        labels = [float(item) / mm for item in locs]
        ax.set_xticks(locs, labels)
        ax.set_xlabel("tor / mm")
        # ax.set_yticks(np.linspace(0, dim_pol, 10))
        locs, labels = plt.yticks()
        labels = [float(item) / mm for item in locs]
        ax.set_yticks(locs, labels)
        ax.set_ylabel("pol / mm")
        plt.tight_layout()
        plt.grid()
        plt.axis('equal')
        plt.show()
        plt.savefig("{}x{}_umspült.png".format(diam_cond/mm, cond_thickness/mm))
    return dim_pol, dim_tor, windings_pol, windings_tor, area_cond, area_water


# dim_pol, dim_tor, windings_pol, windings_tor, area_water, area_cond = crosssection_rPipes(8 * mm, 8 * mm,
#             2 * mm, 2 * mm, iso_thickness=0.25 * mm, casing_thickness=2 * mm,
#             dim_pol=50 * mm, dim_tor=50 * mm)

if 1:
    dim_pol, dim_tor, windings_pol, windings_tor, area_cond, area_water = crosssection_cPipes(diam_cond=6*mm,
                cond_thickness=1*mm, iso_thickness=0.5 * mm, casing_thickness=2 * mm,
                windings_tor=6, windings_pol=8, draw=True)  # windings_pol=6, windings_tor=6)
    print("dimension = {:.2f} mm pol, {:.2f} mm tor".format(dim_pol/mm, dim_tor/mm))
    p_drop_per_coil, p_drop_per_dPancake, power_coil, I_winding = calcEverything(radius_major=0.5, radius_minor=28 * cm, number_coils=12,
                           conductor_crosssection=area_cond, number_windings=windings_pol * windings_tor, material="copper",
                           I_linking=176*kA, deltaT=25, pipeInnerDiam=2 * np.sqrt(area_water / np.pi), dPancake_factor=windings_tor/2)


cond_list = np.array([4.75, 6, 6.35, 6.35, 8, 8, 8, 10]) * mm
thick_list = np.array([0.75, 1, 0.79, 1, 1, 1.5, 2, 2]) * mm
output = ""

if 0:
    for idx, cond in enumerate(cond_list):
        dim_pol, dim_tor, windings_pol, windings_tor, area_cond, area_water = crosssection_cPipes(diam_cond=cond,
            cond_thickness=thick_list[idx], material="copper", iso_thickness=0.25 * mm, casing_thickness=2 * mm,
            dim_pol=50 * mm, dim_tor=50 * mm)  # windings_pol=6, windings_tor=6)

        p_drop_per_coil, p_drop_per_dPancake, power_coil, I_winding = calcEverything(radius_major=0.4, radius_minor=32 * cm, number_coils=12,
                       conductor_crosssection=area_cond, number_windings=windings_pol * windings_tor, material='copper',
                       frequency_rotation=2.45 * GHz, deltaT=25, pipeInnerDiam=2 * np.sqrt(area_water / np.pi), dPancake_factor=windings_tor/2)
        output += "conductor diameter = {} mm, conductor thickness = {} mm:\np_drop_per_coil = {} bar, p_drop_per_dPancake = {} bar, power_coil = {} kW, " \
                  "I_winding = {} A\n\n".format(cond/mm, thick_list[idx]/mm, p_drop_per_coil, p_drop_per_dPancake, power_coil/kW, I_winding)


    with open("pipe_test/copperpipe.txt", "w") as file:
        file.write(output)

# dim_pol, dim_tor, windings_pol, windings_tor, area_cond, area_water = crosssection_umspuelt(diam_cond=4*mm,
#             cond_thickness=1*mm, material="copper", iso_thickness=0.25 * mm, casing_thickness=2 * mm,
#             dim_pol=50 * mm, dim_tor=50 * mm)
