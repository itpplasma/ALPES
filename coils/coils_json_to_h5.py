#%%
from simsopt._core import load
import numpy as np
data = load(f'serial0021326.json')
four1 = data[0]
four2 = data[1]
coils = data[2]
xyz = []
for coil in coils:
    xyz.append(coil.curve.gamma())
xyz = np.array(xyz)

# %%
import h5py

# Create a new hdf 5 file with a new entry Dataset1 that should contain the data xyz
with h5py.File('coils.h5', 'w') as f:
    f.create_dataset('Dataset1', data=xyz)


# # %% Coil Path
# template = h5py.File('test.h5', 'r')
# template['Dataset1']

# # %% Coil Path
# template = h5py.File('/workspaces/code/external/SBGeom-main/example_data/HELIAS5_coils_all_corr.h5', 'r')
# template['Dataset1']

# # %% Coil Fourier
# template_four = h5py.File('/workspaces/code/external/SBGeom-main/example_data/HELIAS5_coils_fourier.h5', 'r')
# print(template_four.keys())
# print(template_four['Coil_0'].keys())

# # %%

# %%
