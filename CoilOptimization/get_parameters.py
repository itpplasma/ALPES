import os
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
import simsopt
from simsopt.field import BiotSavart, Current, coils_via_symmetries
from simsopt.geo import (
    CurveLength, CurveCurveDistance,
    MeanSquaredCurvature, LpCurveCurvature, CurveSurfaceDistance, LinkingNumber,
    SurfaceRZFourier, curves_to_vtk, create_equally_spaced_planar_curves, plot, create_equally_spaced_curves
)
from simsopt.objectives import Weight, SquaredFlux, QuadraticPenalty
from simsopt.util import in_github_actions


coils_input_path = 'Design_Example/input/serial0021326.json'
surfaces, B_axis, coils = simsopt.load(coils_input_path)

curves = [c.curve for c in coils]
s = surfaces[-1]
ncoils = 3

nphi = len(surfaces[-1].quadpoints_phi)
ntheta = len(surfaces[-1].quadpoints_theta)
print(nphi, ntheta)
print(dir(surfaces[-1]))
bs = BiotSavart(coils)
BASLINE_flux = SquaredFlux(s, bs).J()
print('initial flux:', BASLINE_flux)

# Create coils from the input curves and currents:
base_curves = [c.curve for c in coils[:ncoils]]#create_equally_spaced_curves(ncoils, s.nfp, stellsym=True, R0=R0, R1=R1, order=order)
# base_curves = curves[:ncoils]
base_currents = [c.current for c in coils[:ncoils]] #[Current(-4.87817660200371E+05), Current(-2.71334693485699E+05), Current(-3.22002680993767E+05)]
# Since the target field is zero, one possible solution is just to set all
# currents to 0. To avoid the minimizer finding that solution, we fix one
# of the currents:
base_currents[0].fix_all()

coils = coils_via_symmetries(base_curves, base_currents, s.nfp, True)
bs = BiotSavart(coils)
bs.set_points(s.gamma().reshape((-1, 3)))


# calculate the initial objective function values from BASELINE
Jf = SquaredFlux(s, bs)
Jccdist = CurveCurveDistance(base_curves, 1, num_basecurves=ncoils)
Jcsdist = CurveSurfaceDistance(base_curves, s, 1)
Jcs = [LpCurveCurvature(c, 2, 1) for c in base_curves]
Jmscs = [MeanSquaredCurvature(c) for c in base_curves]
Jls = [CurveLength(c) for c in base_curves]
linkNum = LinkingNumber(base_curves)




# Set the thresholds for the objective function based on the initial values:
LENGTH_THRESHOLD = sum([CurveLength(c.curve).J() for c in coils])/len(coils)
CC_THRESHOLD = Jccdist.shortest_distance()
CS_THRESHOLD = Jcsdist.shortest_distance()
CURVATURE_THRESHOLD = max([np.max(c.kappa()) for c in curves])
MSC_THRESHOLD = max([J.J() for J in Jmscs])


print('|----------- Parameters -----------|')
print(f' Length / Coil:\t{LENGTH_THRESHOLD:.4f}')
print(f' CC distance:\t\t{CC_THRESHOLD:.4f}')
print(f' CS distance:\t\t{CS_THRESHOLD:.4f}')
print(f' Curvature :\t{CURVATURE_THRESHOLD:.4f}')
print(f' MSC :\t\t{MSC_THRESHOLD:.4f}')
print('|----------------------------------|')



jf = Jf.J()
BdotN = np.mean(np.abs(np.sum(bs.B().reshape((nphi, ntheta, 3)) * s.unitnormal(), axis=2)))
MaxBdotN = np.max(np.abs(np.sum(bs.B().reshape((nphi, ntheta, 3)) * s.unitnormal(), axis=2)))
mean_AbsB = np.mean(bs.AbsB())
outstr = f"Jf={jf:.1e}, ⟨B·n⟩={BdotN:.1e}"
cl_string = ", ".join([f"{J.J():.1f}" for J in Jls])
kap_string = ", ".join(f"{np.max(c.kappa()):.1f}" for c in base_curves)
msc_string = ", ".join(f"{J.J():.1f}" for J in Jmscs)
outstr += f", Len=sum([{cl_string}])={sum(J.J() for J in Jls):.1f}, ϰ=[{kap_string}], ∫ϰ²/L=[{msc_string}]"
outstr += f", C-C-Sep={Jccdist.shortest_distance():.2f}, C-S-Sep={Jcsdist.shortest_distance():.2f}"
outstr += f", ⟨B·n⟩/|B|={BdotN/mean_AbsB:.1e}"
outstr += f", (Max B·n)/|B|={MaxBdotN/mean_AbsB:.1e}"
outstr += f", Link Number = {linkNum.J()}"
print(outstr)