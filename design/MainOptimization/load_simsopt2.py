# %%
from simsopt._core import load
import os
import numpy as np
from simsopt.mhd import Vmec, QuasisymmetryRatioResidual
from simsopt.objectives import LeastSquaresProblem
from simsopt.solve import least_squares_mpi_solve
from simsopt.util import MpiPartition, proc0_print
import matplotlib.pyplot as plt
# replace "NAME_OF_FILE_YOU_DOWNLOADED" with the name you gave the file
mpi = MpiPartition(4)
#coils = load(f'serial0021326.json')
#print(os.getcwd())
#print(os.chdir('/Users/nicole/Desktop/Fusion_reactor_design_2/code'))
#print(os.getcwd())
equil = Vmec('input.0021326', mpi=mpi)

surf = equil.boundary

# %%
# You can choose which parameters are optimized by setting their 'fixed' attributes.
surf.fix_all()

#for i in ['rc(1,1)', 'zs(1,1)']:
#    surf.unfix(i)
surf.unfix('rc(1,1)')
surf.unfix('zs(1,1)')

desired_iota_axis = 0.314
iota_weight = 1
term1 = (equil.iota_axis, desired_iota_axis, iota_weight)

desired_iota_edge = 0.281
term2 = (equil.iota_edge, desired_iota_edge, iota_weight)
prob = LeastSquaresProblem.from_tuples([term1, term2])

# Solve the minimization problem:
least_squares_mpi_solve(prob, mpi, grad=True)

# %%
'''
%matplotlib widget
equil_old = Vmec('input.0021326_profile_1a', mpi=mpi)
surf_old = equil_old.boundary
equil_new = Vmec('input.0021326_profile_1a_000_000507', mpi=mpi)
surf_new = equil_new.boundary
ax1 = surf_new.plot(close=True, show=True)
surf_old.plot(ax=ax1, close=True, alpha=1.)
'''
# %%
#equil_new = Vmec('input.0021326_profile_1a_000_000507', mpi=mpi)

#vmec.run()

#print(equil_new.iota_axis())
#print(equil_new.iota_edge())
#print(equil_new.iota_profile)

#vmec.run()

#from simsopt.mhd.vmec_diagnostics import vmec_fieldlines
#theta = np.linspace(-np.pi, np.pi, 50)
#fl = vmec_fieldlines(vmec, 0.5, 0, theta1d=theta)
#print(fl.B_cross_grad_B_dot_grad_alpha)

"""
from simsopt.mhd.vmec_diagnostics import vmec_compute_geometry, vmec_fieldlines
from simsopt.field.tracing import plot_poincare_data

s = np.linspace(0.001, 1, 99)
theta = np.linspace(0, 2 * np.pi, 50)
phi = np.linspace(0, 2 * np.pi / 3, 60)
data = vmec_compute_geometry(vmec, s, theta, phi)
print(dir(data))

edge_tor_flux = data.edge_toroidal_flux_over_2pi
print(edge_tor_flux)
iota_profile = data.iota
plt.plot(iota_profile)
plt.title('Profile 1')
plt.xlabel('samples')
plt.ylabel('iota')
plt.show()
"""

#fieldlines = vmec_fieldlines(vmec, s, 1, theta)

#def dump(obj):
#  for attr in dir(obj):
#    print("obj.%s = %r" % (attr, getattr(obj, attr)))

#dump(fieldlines)

#print(fieldlines)
#print(dir(fieldlines))

#print(len(fieldlines.bmag))
#print(len(fieldlines.bmag[0]))
#print(len(fieldlines.bmag[0,0]))


#plot_poincare_data(fieldlines.bmag, phi, 'poincare_data.png')
# %%