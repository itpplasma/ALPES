#!/usr/bin/env python
r"""
This coil optimization script is similar to stage_two_optimization.py. However
in this version, the coils are constrained to be planar, by using the curve type
CurvePlanarFourier. Also the LinkingNumber objective is used to prevent coils
from becoming topologically linked with each other.

In this example we solve a FOCUS like Stage II coil optimisation problem: the
goal is to find coils that generate a specific target normal field on a given
surface.  In this particular case we consider a vacuum field, so the target is
just zero.

The objective is given by

    J = (1/2) \int |B dot n|^2 ds
        + LENGTH_WEIGHT * (sum CurveLength)
        + DISTANCE_WEIGHT * MininumDistancePenalty(DISTANCE_THRESHOLD)
        + CURVATURE_WEIGHT * CurvaturePenalty(CURVATURE_THRESHOLD)
        + MSC_WEIGHT * MeanSquaredCurvaturePenalty(MSC_THRESHOLD)
        + LinkingNumber

if any of the weights are increased, or the thresholds are tightened, the coils
are more regular and better separated, but the target normal field may not be
achieved as well. This example demonstrates the adjustment of weights and
penalties via the use of the `Weight` class.

The target equilibrium is the QA configuration of arXiv:2108.03711.
"""

import os
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
import simsopt
from simsopt.field import BiotSavart, Current, coils_via_symmetries
from simsopt.geo import (
    CurveLength, CurveCurveDistance,
    MeanSquaredCurvature, LpCurveCurvature, CurveSurfaceDistance, LinkingNumber, curves_to_vtk, plot, SurfaceRZFourier)
from simsopt.objectives import Weight, SquaredFlux, QuadraticPenalty

# Number of unique coil shapes, i.e. the number of coils per half field period:
# (Since the configuration has nfp = 2, multiply by 4 to get the total number of coils.)
ncoils = 3

# Major radius for the initial circular coils:
R0 = 0.9

# Minor radius for the initial circular coils:
R1 = 0.5

# Number of Fourier modes describing each Cartesian component of each coil:
order = 16

# Weight on the curve lengths in the objective function. We use the `Weight`
# class here to later easily adjust the scalar value and rerun the optimization
# without having to rebuild the objective.
LENGTH_WEIGHT = Weight(100)
LENGTH_THRESHOLD = 4.5 * 3

# Threshold and weight for the coil-to-coil distance penalty in the objective function:
CC_WEIGHT = 1
CC_THRESHOLD = 0.1512

# Threshold and weight for the coil-to-surface distance penalty in the objective function:
CS_WEIGHT = 1
CS_THRESHOLD = 0.1862

# Threshold and weight for the curvature penalty in the objective function:
CURVATURE_WEIGHT = 5e-6
CURVATURE_THRESHOLD = 4.7965

# Threshold and weight for the mean squared curvature penalty in the objective function:
MSC_WEIGHT = 5e-6
MSC_THRESHOLD = 5.0

# Number of iterations to perform:
MAXITER = 400

# File for the desired boundary magnetic surface:
script_dir = os.path.dirname(os.path.realpath(__file__))
coils_filename = 'Design_Example/input/serial0021326.json'
surface_filename = 'CoilOptimization/03_from_opt_coils/input.surface'

# Directory for output
OUT_DIR = os.path.join(script_dir, "output")
os.makedirs(OUT_DIR, exist_ok=True)

#######################################################
# End of input parameters.
#######################################################

# Initialize the boundary magnetic surface:
surfaces, B_axis, coils = simsopt.load(coils_filename)
s = SurfaceRZFourier.from_vmec_input(surface_filename, range="half period", nphi=32, ntheta=32)
nphi = len(s.quadpoints_phi)
ntheta = len(s.quadpoints_theta)
print(f'Number of phi points: {nphi}')
print(f'Number of theta points: {ntheta}')

# Create the initial coils:
base_curves = [c.curve for c in coils[:3]]#create_equally_spaced_curves(ncoils, s.nfp, stellsym=True, R0=R0, R1=R1, order=order)
# base_curves = curves[:ncoils]
base_currents = [c.current for c in coils[:3]] #[Current(-4.87817660200371E+05), Current(-2.71334693485699E+05), Current(-3.22002680993767E+05)]
# Since the target field is zero, one possible solution is just to set all
# currents to 0. To avoid the minimizer finding that solution, we fix one
# of the currents:
base_currents[0].fix_all()

coils = coils_via_symmetries(base_curves, base_currents, s.nfp, True)
bs = BiotSavart(coils)
bs.set_points(s.gamma().reshape((-1, 3)))


BASLINE_flux = SquaredFlux(s, bs).J()
print('initial flux:', BASLINE_flux)

# plot the initial coils
plot([s] + coils, engine="mayavi", close=True)

curves = [c.curve for c in coils]
curves_to_vtk(curves, OUT_DIR + "/curves_init")
pointData = {"B_N": np.sum(bs.B().reshape((nphi, ntheta, 3)) * s.unitnormal(), axis=2)[:, :, None]}
s.to_vtk(OUT_DIR + "/surf_init", extra_data=pointData)

# Define the individual terms objective function:
Jf = SquaredFlux(s, bs)
Jls = [CurveLength(c) for c in base_curves]
Jccdist = CurveCurveDistance(curves, CC_THRESHOLD, num_basecurves=ncoils)
Jcsdist = CurveSurfaceDistance(curves, s, CS_THRESHOLD)
Jcs = [LpCurveCurvature(c, 2, CURVATURE_THRESHOLD) for c in base_curves]
Jmscs = [MeanSquaredCurvature(c) for c in base_curves]
linkNum = LinkingNumber(curves)

# Form the total objective function. To do this, we can exploit the
# fact that Optimizable objects with J() and dJ() functions can be
# multiplied by scalars and added:

#QuadraticPenalty(sum(Jls), LENGTH_THRESHOLD) \

JF = Weight(1000) * Jf \
    + LENGTH_WEIGHT * QuadraticPenalty(sum(Jls), LENGTH_THRESHOLD) \
    + CC_WEIGHT * Jccdist \
    + CS_WEIGHT * Jcsdist \
    + CURVATURE_WEIGHT * sum(Jcs) \
    + MSC_WEIGHT * sum(QuadraticPenalty(J, MSC_THRESHOLD) for J in Jmscs) \
    + linkNum

# We don't have a general interface in SIMSOPT for optimisation problems that
# are not in least-squares form, so we write a little wrapper function that we
# pass directly to scipy.optimize.minimize


def fun(dofs):
    JF.x = dofs
    J = JF.J()
    grad = JF.dJ()
    jf = Jf.J()
    BdotN = np.mean(np.abs(np.sum(bs.B().reshape((nphi, ntheta, 3)) * s.unitnormal(), axis=2)))
    MaxBdotN = np.max(np.abs(np.sum(bs.B().reshape((nphi, ntheta, 3)) * s.unitnormal(), axis=2)))
    mean_AbsB = np.mean(bs.AbsB())
    outstr = f"J={J:.1e}, Jf={jf:.1e}, ⟨B·n⟩={BdotN:.1e}"
    cl_string = ", ".join([f"{J.J():.1f}" for J in Jls])
    kap_string = ", ".join(f"{np.max(c.kappa()):.1f}" for c in base_curves)
    msc_string = ", ".join(f"{J.J():.1f}" for J in Jmscs)
    outstr += f", Len=sum([{cl_string}])={sum(J.J() for J in Jls):.1f}, ϰ=[{kap_string}], ∫ϰ²/L=[{msc_string}]"
    outstr += f", C-C-Sep={Jccdist.shortest_distance():.2f}, C-S-Sep={Jcsdist.shortest_distance():.2f}"
    outstr += f", ║∇J║={np.linalg.norm(grad):.1e}"
    outstr += f", ⟨B·n⟩/|B|={BdotN/mean_AbsB:.1e}"
    outstr += f", (Max B·n)/|B|={MaxBdotN/mean_AbsB:.1e}"
    outstr += f", Link Number = {linkNum.J()}"
    print(outstr)
    return J, grad


print("""
################################################################################
### Perform a Taylor test ######################################################
################################################################################
""")
f = fun
dofs = JF.x
np.random.seed(1)
h = np.random.uniform(size=dofs.shape)
J0, dJ0 = f(dofs)
dJh = sum(dJ0 * h)
for eps in [1e-3, 1e-4, 1e-5, 1e-6, 1e-7]:
    J1, _ = f(dofs + eps*h)
    J2, _ = f(dofs - eps*h)
    print("err", (J1-J2)/(2*eps) - dJh)

print("""
################################################################################
### Run the optimisation #######################################################
################################################################################
""")
res = minimize(fun, dofs, jac=True, method='L-BFGS-B', options={'maxiter': MAXITER, 'maxcor': 500, 'iprint': 50}, tol=1e-15)
curves_to_vtk(curves, OUT_DIR + "/curves_opt_short")
pointData = {"B_N": np.sum(bs.B().reshape((nphi, ntheta, 3)) * s.unitnormal(), axis=2)[:, :, None]}
s.to_vtk(OUT_DIR + "/surf_opt_short", extra_data=pointData)


# We now use the result from the optimization as the initial guess for a
# subsequent optimization with reduced penalty for the coil length. This will
# result in slightly longer coils but smaller `B·n` on the surface.
steps = 3
for i in range(steps):
    dofs = res.x
    LENGTH_WEIGHT *= 0.1
    res = minimize(fun, dofs, jac=True, method='L-BFGS-B', options={'maxiter': MAXITER, 'maxcor': 500}, tol=1e-15)
    curves_to_vtk(curves, OUT_DIR + "/curves_opt_long")
    pointData = {"B_N": np.sum(bs.B().reshape((nphi, ntheta, 3)) * s.unitnormal(), axis=2)[:, :, None]}
    s.to_vtk(OUT_DIR + "/surf_opt_long", extra_data=pointData)


# Save the optimized coil shapes and currents so they can be loaded into other scripts for analysis:
bs.save(OUT_DIR + "/biot_savart_opt.json")

print('initial flux:', BASLINE_flux)
print('final flux:', SquaredFlux(s, bs).J())