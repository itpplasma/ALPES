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
    shape = np.shape(xyzCoord)
    wires = np.zeros((shape[0] + 1, shape[1]))
    wires[:-1, :] = xyzCoord
    wires[-1, :] = xyzCoord[0, :]
    wireVectors = np.diff(wires, axis=0)
    return wireVectors


def wire_mid_points(xyzCoord):
    midpoints = xyzCoord + wire_vectors(xyzCoord) * 0.5
    return midpoints

def get_field(point, xyzCoord, I):
    """
    point: point in which the B field is calculated
    xyzCoord: coordinates of the coil
    I: current of the coil
    """
    B = np.zeros(3)
    rest_mp = wire_mid_points(xyzCoord)
    rest_vectors = wire_vectors(xyzCoord)
    dist = point - rest_mp
    dist_scalar = np.linalg.norm(dist, axis=1)
    B += mu_0 / (4 * np.pi) * np.sum(I * np.cross(rest_vectors, dist) / dist_scalar[:, np.newaxis] ** 3, axis=0)
    return B

def get_force(coil_nr, coilCoordlist, I_list):
    cut = coilCoordlist[coil_nr]  #cut = coil under test
    cut_mp = wire_mid_points(cut)
    cut_vectors = wire_vectors(cut)
    force_cut = np.zeros_like(cut_mp)
    for idx_cut, point in enumerate(cut_mp):
        B = np.zeros((1, 3))
        for idx_rest, xyzCoord in enumerate(coilCoordlist):
            if idx_rest != coil_nr:
                rest_mp = wire_mid_points(xyzCoord)
                rest_vectors = wire_vectors(xyzCoord)
                dist = point - rest_mp
                dist_scalar = np.linalg.norm(dist, axis=1)
                B += mu_0/(4 * np.pi) * np.sum(I_list[idx_rest] * np.cross(rest_vectors, dist) / dist_scalar[:, np.newaxis]**3, axis=0)
        force_cut[idx_cut, :] = I_list[coil_nr] * np.cross(cut_vectors[idx_cut], B)
    return force_cut


if __name__ == "__main__":
    print('hi, how are you dooin?')
    coil_nr = int(input("from which coil do you want to know the force?"))
    coilCoordlist = loadAndScale('coilData\coil_coordinates0.txt', 12, 0.33/100) # [12, 160, 3] = [coils, points, xyz]
    I1 = 14.7e+3
    I2 = 8.17e+3
    I3 = 9.7e+3
    I_list = np.array([I1, I2, I3, -I3, -I2, -I1, I1, I2, I3, -I3, -I2, -I1])
    force = get_force(coil_nr, coilCoordlist, I_list)
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
            print('Bfield in CG', str(i), ' ', np.linalg.norm(vec))
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
        print("total force = {}".format(force_tot))
        print("total force magnitude = {}".format(np.linalg.norm(force_tot)))
        ax.plot([CGlist[coil_nr][0], CGlist[coil_nr][0]+plot_force_tot[0]], [CGlist[coil_nr][1], CGlist[coil_nr][1]+plot_force_tot[1]], [CGlist[coil_nr][2], CGlist[coil_nr][2]+plot_force_tot[2]], color="black")
        for idx, point in enumerate(mp):
            ax.plot([point[0], point[0] + plot_force[idx, 0]], [point[1], point[1] + plot_force[idx, 1]], [point[2], point[2] + plot_force[idx, 2]])
        ax.legend()
        plt.show()


