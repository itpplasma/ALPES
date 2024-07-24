from simsopt.geo import SurfaceRZFourier, create_equally_spaced_curves, CurveLength, plot, curves_to_vtk
from simsopt.field import Current, coils_via_symmetries, BiotSavart
import simsopt
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(script_dir, 'output')



# import optimized coils
bs_output_file = 'biot_savart_opt.json'
bs_output_file_path = os.path.join(output_dir, bs_output_file)


bs = BiotSavart.from_file(bs_output_file_path)
# print(dir(bs))
coils = bs.coils

# print(len(coils[0].curve.x))

# import target surface
nphi = 32
ntheta = 32
filename = os.path.join(script_dir, 'input.surface')
s = SurfaceRZFourier.from_vmec_input(filename, range="half period", nphi=nphi, ntheta=ntheta)

# plot the optimized coils
plot([s] + coils , engine="mayavi", close=True)