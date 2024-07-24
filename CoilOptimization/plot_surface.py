from simsopt.geo import SurfaceRZFourier, create_equally_spaced_curves, CurveLength, plot, curves_to_vtk, RotatedCurve
from simsopt.field import Current, coils_via_symmetries, BiotSavart
import simsopt
import os
import numpy as np


surfaces, B_axis, coils = simsopt.load('Design_Example/input/serial0021326.json')

surface_new = SurfaceRZFourier.from_wout('CoilOptimization/wout_0021326_1_000_000043.nc', range="half period", nphi=32, ntheta=32)




surface_new.write_nml('CoilOptimization/input.surface')

plot([surfaces[-1], surface_new], engine="matplotlib", close=True, show=True)

