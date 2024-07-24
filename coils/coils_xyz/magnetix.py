"""
This is the story of Magnetix. The roman empire streches across the european continent. All of Gaul is under roman controll.
 All of Gaul??? No! A small village has kept the romans out, thanks to Magnetix and his magix repelling force, that repells
 both romans and coils.
 Magnetix has one weakpoint however, his enemies must never find out. He can only cast his spells with all coils being in
 the corrext order. Sometimes he forgets and has to recharge his powers with Danix. Only Danix knows how to correct the
 currents in the coils, so that Megnetix' powers can thrive.
"""
from windingCoordinateGenerator import *

mu_0 = 1.25663706127e-6


def wire_vectors(xyzCoord):
    """
    :param xyzCoord: coordinates of the coil
    :return: the vectors between each two consecutive points xyzCoords including last to first, shape like input
    """
    shape = np.shape(xyzCoord)
    wires = np.zeros((shape[0] + 1, shape[1]))
    wires[:-1, :] = xyzCoord
    wires[-1, :] = xyzCoord[0, :]
    wireVectors = np.diff(wires, axis=0)
    return wireVectors


def wire_mid_points(xyzCoord):
    """
    :param xyzCoord: coordinates of the coil
    :return: points in between the original xyzCoords, shape like input
    """
    midpoints = xyzCoord + wire_vectors(xyzCoord) * 0.5
    return midpoints


def get_field(point, xyzCoord, I):
    """
    :param point: point in which the B field is calculated
    :param xyzCoord: coordinates of the coil
    :param I: current of the coil
    :return: B field at point, created by given coil (xyzCoord) with current (I), shape: [xyz] numpy array
    """
    B = np.zeros(3)
    rest_mp = wire_mid_points(xyzCoord)
    rest_vectors = wire_vectors(xyzCoord)
    dist = point - rest_mp
    dist_scalar = np.linalg.norm(dist, axis=1)
    dist_scalar[np.argwhere(dist_scalar == 0)] = 1 # Avoid division by 0! Magnetix is happy :))
    # This works since np.cross gives zero for dist = 0!
    B += mu_0 / (4 * np.pi) * np.sum(I * np.cross(rest_vectors, dist) / dist_scalar[:, np.newaxis] ** 3, axis=0) #Biot-Savart
    return B


def get_force(coil_nr, coilCoordlist, I_list, include_self=True):
    """
    :param coil_nr: The index of the coil, where the forces are calculated
    :param coilCoordlist: list of numpy arrays containing xyz coil coordinates
    :param I_list: list of currents through each coil, !signs must be right!
    :param include_self: boolean, if True points on the coil under test are also considered.
    :return: return force vectors for every point of the coil in a numpy [n, 3] array
    """
    cut = coilCoordlist[coil_nr]  #cut = coil under test
    cut_mp = wire_mid_points(cut)
    cut_vectors = wire_vectors(cut)
    force_cut = np.zeros_like(cut_mp)
    for idx_cut, point in enumerate(cut_mp):
        B = np.zeros((1, 3))
        for idx_rest, xyzCoord in enumerate(coilCoordlist):
            if include_self:
                B += get_field(point, xyzCoord, I_list[idx_rest])
            else:
                if coil_nr != idx_rest:
                    B += get_field(point, xyzCoord, I_list[idx_rest])
        force_cut[idx_cut, :] = I_list[coil_nr] * np.cross(cut_vectors[idx_cut], B)
    return force_cut


def get_moments(coil_nr, coilCoordlist, I_list):
    """
    :param coil_nr: The index of the coil, where the forces are calculated
    :param coilCoordlist: list of numpy arrays containing xyz coil coordinates
    :param I_list: list of currents through each coil, !signs must be right!
    :return: return moment vector for the center of gravity as numpy [3] array
    """
    CG = np.mean(coilCoordlist[coil_nr], axis=0)
    force = get_force(coil_nr, coilCoordlist, I_list, include_self=False)
    mp = wire_mid_points(coilCoordlist[coil_nr])
    dist = mp - CG
    moment = np.sum(np.cross(dist, force), axis=0)
    return moment


if __name__ == "__main__":
    print('hi, how are you dooin?')
    coil_nr = int(input("from which coil do you want to know the force?"))
    coilCoordlist = loadAndScale('coilData\coil_coordinates0.txt', 12, 0.33/100) # [12, 160, 3] = [coils, points, xyz] !!!/100 bc: convert from fusion (cm) units!!!
    I1 = 14.7e+3 #A
    I2 = 8.17e+3 #A
    I3 = 9.7e+3 #A
    I_list = np.array([I1, I2, I3, -I3, -I2, -I1, I1, I2, I3, -I3, -I2, -I1])
    force = get_force(coil_nr, coilCoordlist, I_list)
    moment = get_moments(coil_nr, coilCoordlist, I_list)
    total_moment = np.sqrt(np.sum(moment**2))
    print("The total moment for coil {} is {:.3f} Nm\nThe components are: \n{} Nm\n".format(coil_nr, total_moment, np.round(moment, 3)))
    if True: #3D Plot
        ax = plt.figure().add_subplot(projection='3d')
        CGlist = coilCG(coilCoordlist)
        for i in range(len(coilCoordlist)):
            #panCk = pancakeCoordList[i]
            cl = coilCoordlist[i]
            #ax.plot(panCk[:,0], panCk[:,1], panCk[:,2], label='pancake')
            ax.plot(cl[:, 0], cl[:, 1], cl[:, 2], label='coil_{}'.format(i))
            CG = CGlist[i]
            vec = get_field(CG, cl, I_list[i])
            #print('Bfield in CG', str(i), ' ', np.linalg.norm(vec))
            # vecList = CGvectors(CGlist)
            # vec = vecList[i] * 20
            vec *= 1e+0
            #print("len:", np.linalg.norm(vec))
            ax.plot([CG[0], CG[0]+vec[0]], [CG[1], CG[1]+vec[1]], [CG[2], CG[2]+vec[2]])
            ax.plot(CG[0], CG[1], CG[2],'.')
        mp = wire_mid_points(coilCoordlist[coil_nr])
        plot_force = 1e-2*force
        force_tot = np.sum(force, axis=0)
        plot_force_tot = force_tot * 1e-3
        print("total force = {} N".format(np.round(force_tot, 3)))
        print("total force magnitude = {:.3f} N".format(np.linalg.norm(force_tot)))
        ax.plot([CGlist[coil_nr][0], CGlist[coil_nr][0]+plot_force_tot[0]],
                [CGlist[coil_nr][1], CGlist[coil_nr][1]+plot_force_tot[1]],
                [CGlist[coil_nr][2], CGlist[coil_nr][2]+plot_force_tot[2]], color="black", label="total force")
        plot_moment = moment * 1e-2
        ax.plot([CGlist[coil_nr][0], CGlist[coil_nr][0] + plot_moment[0]],
                [CGlist[coil_nr][1], CGlist[coil_nr][1] + plot_moment[1]],
                [CGlist[coil_nr][2], CGlist[coil_nr][2] + plot_moment[2]], color="blue", label="total moment")
        for idx, point in enumerate(mp):
            ax.plot([point[0], point[0] + plot_force[idx, 0]], [point[1], point[1] + plot_force[idx, 1]], [point[2], point[2] + plot_force[idx, 2]])
        ax.legend()
        plt.show()