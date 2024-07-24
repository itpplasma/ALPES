# %%
from simsopt.util import MpiPartition
from simsopt.mhd import Vmec
from simsopt.objectives import LeastSquaresProblem
from simsopt.solve import least_squares_mpi_solve, least_squares_serial_solve

# In the next line, we can adjust how many groups the pool of MPI
# processes is split into.
mpi = MpiPartition(ngroups=3)

# Initialize VMEC from an input file:
equil = Vmec('input.0021326_1', mpi)
surf = equil.boundary
# %%
# You can choose which parameters are optimized by setting their 'fixed' attributes.
surf.fix_all()
surf.unfix('rc(1,1)')
surf.unfix('zs(1,1)')

# Each Target is then equipped with a shift and weight, to become a
# term in a least-squares objective function.  A list of terms are
# combined to form a nonlinear-least-squares problem.
#desired_volume = 1.2337
#volume_weight = 1
#term1 = (equil.volume, desired_volume, volume_weight)

desired_iota_axis = -0.8
iota_weight = 1
term1 = (equil.iota_axis, desired_iota_axis, iota_weight)

desired_iota_edge = -0.05
term2 = (equil.iota_edge, desired_iota_edge, iota_weight)

desired_volume = 1.0
term3 = (equil.volume, desired_volume, iota_weight)

prob = LeastSquaresProblem.from_tuples([term1, term2, term3])

# Solve the minimization problem:
#least_squares_mpi_solve(prob, mpi, grad=True)
least_squares_serial_solve(prob)
# %%
%matplotlib widget
equil_old = Vmec('input.0021326_1', mpi=mpi)
surf_old = equil_old.boundary
equil_new = Vmec('input.0021326_1_000_000043', mpi=mpi)
surf_new = equil_new.boundary
ax1 = surf_new.plot(close=True, show=True)
surf_old.plot(ax=ax1, close=True, alpha=1.)
# %%


