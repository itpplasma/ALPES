from py_spec import *
from py_spec.output import SPECout
from py_spec.input import SPECNamelist
import matplotlib.pyplot as plt
from simsopt.mhd import Spec
import simsopt
import os
import lib.runPoincare as rp


#### Input ####
DESIGN_DIRECTORY = 'Design_Example'
OUTPUT_DIRECTORY = os.path.join(DESIGN_DIRECTORY, 'SPEC')

input_file_path = rp.verifyInputDirectory(DESIGN_DIRECTORY, extension='.sp')
# ceate output directory
if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

# initialize SPEC
equil = Spec(input_file_path)

# change boundary
# sur = surfaces[-1]
# sur = sur.to_RZFourier()
# sur.change_resolution(9,6)
# equil.boundary = sur

# plot([equil.boundary], engine="matplotlib", close=True, show=True)
#plot([equil.boundary, surfaces[0]], engine="matplotlib", close=True, show=True)

equil.run()

# out = SPECout('test/test_bs/test_bs_2DOF_targetIotaAndVolume.sp.h5')
out = SPECout(input_file_path + '.h5')

def plot_poincare_grid(step=1, stop=24):
    # Calculate the number of plots needed
    num_plots = (stop + step - 1) // step  # Ceiling division to include the last index if needed
    
    # Determine grid size
    ncols = 3  # Number of columns
    nrows = (num_plots + ncols - 1) // ncols  # Ceiling division to determine rows
    
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, nrows * 2.5))
    axes = axes.flatten()  # Flatten the axes array for easy indexing
    
    for idx, ax in enumerate(axes):
        toroidal_idx = idx * step
        if toroidal_idx < stop:
            ax.grid()
            out.plot_poincare(toroidalIdx=toroidal_idx, ax=ax, marker='o')
            ax.set_title(f'Toroidal Index {toroidal_idx}')
            
        else:
            fig.delaxes(ax)  # Remove unused subplots
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()

# Example usage: Plot every 2nd element
plot_poincare_grid(step=10, stop=21)

