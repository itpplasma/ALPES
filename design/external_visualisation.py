# General modules
import SBGeom
import numpy as np
import meshio

# Coil modules
from simsopt._core import load
import h5py

# Magnetic field modules
import jax
import jax.numpy as jnp

#----------------------------------------------------------------------------------------------------------------------
#                                                    Coils
#----------------------------------------------------------------------------------------------------------------------
# Converting the json file to h5 file
'''
The converted h5 file can be used to visualise a coil set in the SBGeom module. This module is an external program
that is yet to be released. For further information, please contact the authors.

It is important that the data is named 'Dataset1' in the h5 file, otherwise SBGeom will not be able to read the data.
'''
data = load(f'serial0021326.json')      # SIMSOPT-data from QUASR (https://quasr.flatironinstitute.org/model/0021326)
coils = data[2]                         # Coils are stored in the third index of the data
xyz = []
for coil in coils:
    xyz.append(coil.curve.gamma())
xyz = np.array(xyz)

# Create a new h5 file with a new entry Dataset1 that should contain the data xyz
with h5py.File('coils.h5', 'w') as f:
    f.create_dataset('Dataset1', data=xyz)

#------------------------------------------------
# Getting the coil data from the h5 file
cs = SBGeom.Discrete_Coil_Set_From_HDF5("coils.h5")

# Creating the vtk file for the coil set
'''
cs.Mesh_Triangles(width_phi, width_R, number_of_vertices, 'type').write('RMFd.vtk')
    Inputs:
        width_phi = coil_width / R_0        with R_0 = 1.0 m
        width_R   = thickness of the coil
        type      = type of coil (string)
'''
# Example for QUASR coils:
cs.Mesh_Triangles(0.1/5,0.1/5,300, "RMF").write('RMFd.vtk')


#----------------------------------------------------------------------------------------------------------------------
#                                                   Magnetic Field
#----------------------------------------------------------------------------------------------------------------------
# Converting input file to vmec file
'''
To visualise the magnetic field, SBGeom needs a vmec file. The vmec file can be created by following these steps:

1. Download the .input file from the QUASR website (https://quasr.flatironinstitute.org/model/0021326)

2. Copy these extra lines to the beginning of the .input file:
    LFREEB = F
    MGRID_FILE = "none"
    DELT = 0.9
    NCURR = 0
    MPOL = 9
    NTOR = 6
    LASYM = .FALSE.
    NFP = 2
    NZETA = 18
    NSTEP = 200
    NVACSKIP = 6
    GAMMA = 0.000000E+00

    NS_ARRAY = 99
    FTOL_ARRAY = 2.e-10
    NITER = 30000

In the Terminal:
    1. write: "xvmec input.---"                             # with --- being the name of the .input file
    2. write: "nccopy -k 4 wout_---.nc vmec_file.nc4"

NB: You will be getting a few other files, but we only need the wout_---.nc file for the nc4 file.
'''

#------------------------------------------------
# Simple Flux Surface Meshing
vmec_file = "vmec_file.nc4"
s1 = SBGeom.Flux_Surfaces(vmec_file)

'''
s1.Mesh_Surface(num_surface, zeta_1, num_radial, num_poloidal, zeta_2, radius).write("surface.vtk")
    Inputs:
        num_surface  = radius of the flux surface (between [0,1])
        zeta_1       = zeta of the flux surface (keep at 0.0)
        num_radial   = number of vertices in the radial direction
        num_poloidal = number of vertices in the poloidal direction
        zeta_2       = zeta of the flux surface (keep at 0.0)
        radius       = arc length of the flux surface (between [0,2*pi])
'''
# Example for QUASR flux surfaces:
s1.Mesh_Surface(0.5,0.0,300,500,0.0,2*np.pi).write("surface.vtk")
