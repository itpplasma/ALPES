import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from tqdm import tqdm
from scipy.interpolate import splprep, splev

def dimensions(dim_z_max=0.65, dim_plane_max=1.6):
    files = glob.glob("coil_coordinates?.txt")
    files += glob.glob("coil_coordinates??.txt")
    # (coil, :, xyz)
    coils = []
    for i in range(len(files)):
        temp = np.loadtxt("coil_coordinates{}.txt".format(i))
        coils.append(temp)
    coils = np.array(coils)
    max_z = np.max(coils[:, :, 2])
    min_z = np.min(coils[:, :, 2])
    dim_z = abs(max_z - min_z)
    factor = dim_z_max / dim_z
    coils *= factor
    radius = np.sqrt(np.sum(coils[:, :, :-1]**2, axis=2))
    dim_plane = 2 * np.max(radius)
    if dim_plane > dim_plane_max:
        factor = dim_plane_max / dim_plane
    dim_z *= factor
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
    return dim_z, dim_plane, min_dist, length

if __name__ == "__main__":
    files = glob.glob("coil_coordinates?.txt")
    files += glob.glob("coil_coordinates??.txt")
    # (coil, :, xyz)
    coils = []
    for i in range(len(files)):
        temp = np.loadtxt("coil_coordinates{}.txt".format(i))
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

    z, p, m, l = dimensions()
    print("\nThe dimension in z-direction is: {:.3f} m \nThe max dimension in the torroidal plane is: {:.3f} m\n"
          "And the min distance between coils is {:.3f} mm\n\n"
          "The lengths of the coils are (in meter):\n{}".format(z, p, m * 1e+3, l))




