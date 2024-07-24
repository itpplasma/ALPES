import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from tqdm import tqdm
from scipy.interpolate import splprep, splev

def dimensions(dim_z_max=None,
               dim_plane_max=None,
               scaling_factor=None):
    """
    :param dim_z_max: maximal length in z direction
    :param dim_plane_max: maximal length in the toroidal plane
    :param scaling_factor: scaling factor for the coil data
    :return: dim_z, dim_plane, min_dist, length, scaling_factor
    """
    if not (dim_z_max or dim_plane_max or scaling_factor):
        raise Exception("Either dim_z_max, dim_plane_max or scaling factor ha to be given!")
    files = glob.glob("coilData\coil_coordinates?.txt")
    files += glob.glob("coilData\coil_coordinates??.txt")
    # (coil, :, xyz)
    coils = []
    for i in range(len(files)):
        temp = np.loadtxt("coilData\coil_coordinates{}.txt".format(i))
        coils.append(temp)
    coils = np.array(coils)
    # Calc dim z
    max_z = np.max(coils[:, :, 2])
    min_z = np.min(coils[:, :, 2])
    dim_z = abs(max_z - min_z)
    # Calc dim plane
    radius = np.sqrt(np.sum(coils[:, :, :-1] ** 2, axis=2))
    dim_plane = 2 * np.max(radius)
    if dim_z_max:
        scaling_factor = dim_z_max / dim_z
    elif dim_plane_max:
        scaling_factor = dim_plane_max / dim_plane
    coils *= scaling_factor
    dim_z *= scaling_factor
    dim_plane *= scaling_factor
    coils_shifted = np.roll(coils, 1, axis=0)
    min_dist = 100
    for i in tqdm(range(len(coils[:, 0, 0]))):
        for k in coils[i, :, :]:
            for m in coils_shifted[i, :, :]:
                dist = np.sqrt(np.sum((k - m)**2))
                if dist < min_dist:
                    min_dist = dist
    length = np.zeros_like(coils[:, 0, 0])
    for idx, coil in enumerate(coils[:, :, :]):
        coil = np.append(coil, coil[0, :]).reshape((len(coil[:, 0]) + 1, len(coil[0, :])))
        coil_shifted = np.roll(coil, 1, axis=0)
        dist = np.sqrt(np.sum((coil - coil_shifted) ** 2, axis=1))
        length[idx] = np.sum(dist)
    return v

if __name__ == "__main__":
    files = glob.glob("coilData\coil_coordinates?.txt")
    files += glob.glob("coilData\coil_coordinates??.txt")
    # (coil, :, xyz)
    coils = []
    for i in range(len(files)):
        temp = np.loadtxt("coilData\coil_coordinates{}.txt".format(i))
        coils.append(temp)
    coils = np.array(coils)
    tck, u = splprep([coils[0, :, 0], coils[0, :, 1], coils[0, :, 2]], s=0)
    new_points = splev(u, tck)
    new_points = np.array(new_points)
    if len(new_points[0, :]) == len(coils[0, : , 0]):
        print("interpolation did nothing :(")
    else:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        # for i in coils[0, :, :]:
        #     ax.scatter(i[0], i[1], i[2], marker="o")
        for i in range(len(new_points[0, :])):
            ax.scatter(new_points[0, i], new_points[1, i], new_points[2, i], marker="o")
        plt.show()

    z, p, m, l, f = dimensions(scaling_factor=0.35)
    print("\nThe dimension in z-direction is: {:.3f} m \nThe max dimension in the torroidal plane is: {:.3f} m\n"
          "And the min distance between coils is {:.3f} mm\n"
          "The factor for the design data is: {}\n\n"
          "The lengths of the coils are (in meter):\n{}".format(z, p, m * 1e+3, f, np.round(l, 4)))




