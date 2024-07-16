import simsopt
from simsopt.field import BiotSavart
from simsopt.geo import plot, SurfaceScaled, CurveLength
from simsopt.field import Current
from simsopt.util.permanent_magnet_helper_functions import calculate_on_axis_B
import numpy as np
import matplotlib.pyplot as plt
import os
import numpy as np
import lib.runPoincare as rp


#### Input ####
DESIGN_DIRECTORY = 'Design_Example'
OUTPUT_DIRECTORY = os.path.join(DESIGN_DIRECTORY, 'SCALED')

geo_scale = 0.33
B_wanted = 0.087  # T


input_file_path = rp.verifyInputDirectory(DESIGN_DIRECTORY)
# ceate output directory
if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

#---------------------------------#
# load the file acording to your input file. Outcommand the one you are not using

# load the input file option 1
surfaces, B_axis, coils = simsopt.load(input_file_path)
bs = BiotSavart(coils)


#---------------------------------#

B_not_scaled = calculate_on_axis_B(bs, surfaces[0].to_RZFourier())
print(f'B on axis (not scaled):{B_not_scaled:.4f} T')

# scale the coils
for coil in coils:
    coil.curve.set_dofs(coil.curve.get_dofs() * geo_scale)

# scale the surfaces
for s in surfaces:
    s.set_dofs(SurfaceScaled(s, 3).x)

# scale the B_axis
B_axis.set_dofs(B_axis.get_dofs() * geo_scale)

# calculate the B field on axis
B_geo_scaled = calculate_on_axis_B(bs, surfaces[0].to_RZFourier())
print(f'B on axis (geometrical scaled):{B_geo_scaled:.4f} T')
current_scale = B_wanted / B_geo_scaled
print('current scale:', current_scale)

# scale the currents
for coil in coils[:3]:
    coil.current.scale *= current_scale
    # print('scale:', coil.current.scale)
for coil in coils:
    print('current:', coil.current.get_value())

B_scaled = calculate_on_axis_B(bs, surfaces[0].to_RZFourier())
print('B (full scaled):', B_scaled)

# save the scaled coils
bs.save(os.path.join(OUTPUT_DIRECTORY, 'scaledBiotSavart.json'))
# save the scaled surfaces
surfaces[-1].to_RZFourier().write_nml((os.path.join(OUTPUT_DIRECTORY, 'input.scaledSurface')))


# plot the firts three coils in seperate subplots and the surrent as anotation
fig, axs = plt.subplots(1, 3, figsize=(12, 8), subplot_kw={'projection': '3d'})
for i, coil in enumerate(coils[:3]):
    coil.plot(ax=axs[i], engine="matplotlib", close=True, show=False)   
    axs[i].set_title(f'Current: {coil.current.get_value(): .4f} A-turn \n Length: {CurveLength(coil.curve).J(): .4f} m', fontsize=12)

plt.show()
