from fractions import Fraction
import os
import subprocess
import sys
import numpy as np
from simsopt.field import coils_to_makegrid
import h5py
import matplotlib.pyplot as plt
from simsopt.field import (BiotSavart, InterpolatedField, SurfaceClassifier, particles_to_vtk,
                           compute_fieldlines, LevelsetStoppingCriterion, plot_poincare_data)
import time

def verifyInputDirectory(DESIGN_DIRECTORY, extension = '.json'):
    # Test if the DESIGN_DIRECTORY exists
    if not os.path.exists(DESIGN_DIRECTORY):
        print(f"Error: {DESIGN_DIRECTORY} does not exist.")
        sys.exit(1)

    # Test if the input directory exists within DESIGN_DIRECTORY
    input_directory = os.path.join(DESIGN_DIRECTORY, 'input')
    if not os.path.exists(input_directory):
        print(f"Error: {DESIGN_DIRECTORY} exists but no input directory: '{input_directory}' exists.")
        sys.exit(1)

    # Test if one and only one JSON input file exists
    input_files = [f for f in os.listdir(input_directory) if f.endswith(extension) and os.path.isfile(os.path.join(input_directory, f))]

    if len(input_files) != 1:
        print(f"Error: {len(input_files)} {extension} input files found in '{input_directory}'. Exactly one is required.")
        sys.exit(1)
    
    # Return the path to the JSON input file if exactly one is found
    input_file_path = os.path.join(input_directory, input_files[0])
    print("Using input file:", input_file_path)
    return input_file_path

def create_coils_file(nfp, coils_output_file_path, bs):
    # Create the coils input file for makegrid
    print("Creating coils input file...")
    coils = bs.coils
    curves = [coil.curve for coil in coils]
    currents = [coil.current for coil in coils]

    # As we export all coils we have to set nfp=1 and stellsym=False
    coils_to_makegrid(coils_output_file_path, curves, currents, nfp=1, stellsym=False)

    # Change first line of coils file to the correct nfp
    with open(coils_output_file_path, 'r') as f:
        lines = f.readlines()
        lines[0] = f"periods   {nfp}\n"

        with open(coils_output_file_path, 'w') as f:
            f.writelines(lines)

def create_fieldlines_file(file_path, params, variant):
    # Convert list of EXTCUR values to formatted strings
    extcur_lines = "\n".join([f"EXTCUR({i+1})  =  {value:.17E}" for i, value in enumerate(params['EXTCUR'])])

    # Convert R_START, Z_START, PHI_START, PHI_END lists to space-separated strings
    r_start = "  ".join(map(str, params['R_START']))
    z_start = "  ".join(map(str, params['Z_START']))
    phi_start = "  ".join(map(str, params['PHI_START']))
    phi_end = "  ".join(map(str, params['PHI_END']))

    content = f"""&INDATA
  LASYM = {str(params["LASYM"]).upper()}
  NFP  =  {params["NFP"]}
  {extcur_lines}
  MPOL =  {params["MPOL"]}
  NTOR =  {params["NTOR"]}
  NZETA = {params["NZETA"]}
/
\\
&FIELDLINES_INPUT
  NR = {params["NR"]}
  NPHI = {params["NPHI"]}
  NZ = {params["NZ"]}
  RMIN = {params["RMIN"]}
  RMAX = {params["RMAX"]}
  ZMIN = {params["ZMIN"]}
  ZMAX = {params["ZMAX"]}
  MU = {params["MU"]}
  R_START = {r_start}
  Z_START = {z_start}
  PHI_START = {phi_start}
  PHI_END = {phi_end}
  NPOINC = {params["NPOINC"]}
  INT_TYPE = '{params["INT_TYPE"]}'
  FOLLOW_TOL = {params["FOLLOW_TOL"]:.1E}
  VC_ADAPT_TOL = {params["VC_ADAPT_TOL"]:.1E}
/
\\
&END
\\
"""
    file_path = os.path.join(file_path, 'input.fieldlines_' + variant)
    with open(file_path, 'w') as file:
        file.write(content)

def run_fieldlines(variant, output_dir, XGRID_PARAMS):
    LOG_FIELDLINES = True
    working_dir = os.getcwd()
    print("Creating fieldlines input file...")
    create_fieldlines_file(output_dir, XGRID_PARAMS, variant)

    # Execute xfiledlines from stellopt for the vacuum fieldlines
    xfiledlines_cmd = os.path.expanduser('~/bin/xfieldlines')

    print("Execute xfiledlines...")
    cmd = xfiledlines_cmd + ' -vmec fieldlines_' + variant + ' -coil coils.' + variant + ' -vac'
    print(cmd)

    try:
        # change to the directory where the vmec input file is located and execute vmec
        os.chdir(os.path.join(output_dir))
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Open the log file for writing
        log_file_path = 'xfiledlines' + variant + '.log'
        log_file = open(log_file_path, 'w')

        # Print the output if LOG_VMEC is True and write to log file
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                log_file.write(output)
                if LOG_FIELDLINES:
                    print(output.strip())

        # Get the stderr output of the process and write to log file
        stderr_output = process.stderr.read()
        if stderr_output:
            print("Error:", stderr_output.strip())
            log_file.write("Error: " + stderr_output)

        # Get the return code of the process
        return_code = process.poll()
        if return_code != 0:
            print(f"Command '{cmd}' failed with return code {return_code}")
            log_file.write(f"Command '{cmd}' failed with return code {return_code}")

        # Close the log file
        log_file.close()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # change back to the working directory
        os.chdir(working_dir)

def plot_poincare(file_path, PLOT_PARAMS, nfp, variant, save=None):

    NPOINC = PLOT_PARAMS["NPOINC"]
    phi_planes = PLOT_PARAMS["PHIPLANES"]
    show = PLOT_PARAMS["SHOW"]

    def rad_to_fraction_of_pi(angle_rad):
        frac = Fraction(angle_rad / np.pi).limit_denominator()
        if frac.denominator == 1:
            return r"$\pi$"
        elif frac.numerator == 1:
            return r"$\frac{{\pi}}{{{}}}$".format(frac.denominator)
        elif frac.denominator == 1:
            return r"${}\pi$".format(frac.numerator)
        else:
            return r"$\frac{{{}\pi}}{{{}}}$".format(frac.numerator, frac.denominator)

    PHI_values = phi_planes  # List of phi values to plot
    PHI_indices = [int(nfp * phi / (2 * np.pi) * NPOINC) for phi in PHI_values]  # Corresponding indices

    with h5py.File(file_path, 'r') as hdf:
        L_lines = hdf['L_lines'][:]
        R_lines = hdf['R_lines'][:]
        Z_lines = hdf['Z_lines'][:]

# Number of field lines
    num_lines = L_lines.shape[0]

# Create a single plot with multiple subplots for each phi value
    fig, axs = plt.subplots(1, len(PHI_values), figsize=(6 * len(PHI_values), 6))
    # add figure title
    # all_r = np.concatenate([R_lines[phi_idx::NPOINC, :] for phi_idx in PHI_indices])
    # all_z = np.concatenate([Z_lines[phi_idx::NPOINC, :] for phi_idx in PHI_indices])
    # rmin, rmax = np.percentile(all_r.flatten(), [10, 90])
    # zmin, zmax = np.percentile(all_z.flatten(), [10, 90])
    
    # print('zmin', zmin)
    # print('zmax', zmax)
    # print('rmin', rmin)
    # print('rmax', rmax)
    # axmax = max(rmax, zmax)
    # axmin = min(rmin, zmin)
    fig.suptitle('Poincaré Plot ' + variant.replace('_', ' ') , fontsize=16)

    for idx, (phi_idx, phi) in enumerate(zip(PHI_indices, PHI_values)):
        ax = axs[idx]
        for i in range(num_lines):    
            ax.scatter(R_lines[phi_idx::NPOINC, i], Z_lines[phi_idx::NPOINC, i], s=1, label=f'Line {i+1}')

        
        
        ax.set_xlabel('R')
        ax.set_ylabel('Z')
        ax.axis('equal')
        ax.set_xlim(PLOT_PARAMS["RLIM"])
        ax.set_ylim(PLOT_PARAMS["ZLIM"])
        print('xlim', ax.get_xlim())
        print('ylim', ax.get_ylim())

        phi_label = rad_to_fraction_of_pi(phi)
        ax.set_title(f'Poincaré Plot at $\phi$ = {phi_label}')
        #ax.axis('equal', adjustable = 'box')
        print('xlim axis', ax.get_xlim())
        print('ylim axis', ax.get_ylim())
        if idx == 0:
            ax.legend()
            print('xlim legend', ax.get_xlim())
            print('ylim legend', ax.get_ylim())
        ax.grid(True)
        print('xlim grid', ax.get_xlim())
        print('ylim grid', ax.get_ylim())
        # plt.gca().set_aspect('equal', adjustable = 'box')

    plt.tight_layout()
    print('xlim layout', ax.get_xlim())
    print('ylim layout', ax.get_ylim())
    

    if save is not None:
        print('xlim layout', ax.get_xlim())
        print('ylim layout', ax.get_ylim())
        plt.savefig(save)

    if show:
        plt.show()

def run_poincare_xfieldlines(coils, variant, output_dir, nfp, FILEDLINE_PARAMS, PLOT_PARAMS, SAVE_PERTURBATIONS):
    print(f'|------- Running {variant} -------|')

    # create BiotSavart object
    bs = BiotSavart(coils)

    # save BiotSavart object to json
    if SAVE_PERTURBATIONS:
        bs_output_file = 'biot_savart_' + variant + '.json'
        bs_output_file_path = os.path.join(output_dir,'Coils', bs_output_file)
        #create the directory if it does not exist
        if not os.path.exists(os.path.join(output_dir,'Coils')):
            os.makedirs(os.path.join(output_dir,'Coils'))
        bs.save(bs_output_file_path)

    # create coils file
    coils_output_file = 'coils.' + variant
    coils_output_file_path = os.path.join(output_dir, coils_output_file)
    create_coils_file(nfp, coils_output_file_path, bs)

    # run fieldlines
    run_fieldlines(variant, output_dir, FILEDLINE_PARAMS)

    # plot Poincaré plot
    input_file_path = os.path.join(output_dir, 'fieldlines_fieldlines_' + variant + '.h5')
    if PLOT_PARAMS["SAVE"]:
        save_path = os.path.join(output_dir, 'poincare_plot_' + variant + '.png')

    plot_poincare(input_file_path, PLOT_PARAMS, nfp, variant, save=save_path)

    if not PLOT_PARAMS["KEEP_RESULT_DATA"]:
        os.remove(os.path.join(output_dir, 'fieldlines_fieldlines_' + variant + '.h5'))

    if not FILEDLINE_PARAMS["KEEP_INDATA"]:
        os.remove(os.path.join(output_dir, 'input.fieldlines_' + variant))

    # remove the coils file
    os.remove(coils_output_file_path)

def run_poincare_simsopt(coils, variant, output_dir, surface ,SAVE_PERTURBATIONS, FILEDLINE_PARAMS):

    
    print("Calculate Poincaré Plot")

    bs = BiotSavart(coils)
    nfp = FILEDLINE_PARAMS['NFP']

    if SAVE_PERTURBATIONS:
        bs_output_file = 'biot_savart_' + variant + '.json'
        bs_output_file_path = os.path.join(output_dir,'Coils', bs_output_file)
        #create the directory if it does not exist
        if not os.path.exists(os.path.join(output_dir,'Coils')):
            os.makedirs(os.path.join(output_dir,'Coils'))
        bs.save(bs_output_file_path)


    degree = FILEDLINE_PARAMS['DEGREE']         #for interpolation
    nfieldlines = len(FILEDLINE_PARAMS['R_START'])   #how many fieldlines one wants to trace
    tmax_fl = FILEDLINE_PARAMS['TMAX']      #duration of simulation, the longer the more intersections with poincare plot
    tol = FILEDLINE_PARAMS['FOLLOW_TOL']       #accuracy of ODE solution when tracing field lines


    sc_fieldline = SurfaceClassifier(surface, h=0.03, p=2)
    #sc_fieldline.to_vtk(OUT_DIR + 'levelset', h=0.02)

    stopping_crit = [LevelsetStoppingCriterion(sc_fieldline.dist)]


    def trace_fieldlines(bfield, label):
        t1 = time.time()
        # Set initial grid of points for field line tracing, going from
        # the magnetic axis to the surface. 
        # The Values of R0 were a bit trial and error and may need adjustment
        # for different configurations
        R0 = FILEDLINE_PARAMS['R_START']
        Z0 = FILEDLINE_PARAMS['Z_START']
        phis = [(i/4)*(2*np.pi/nfp) for i in range(FILEDLINE_PARAMS['NPLANES'])] #4 cuts

        fieldlines_tys, fieldlines_phi_hits = compute_fieldlines(
            bfield, R0, Z0, tmax=tmax_fl, tol=tol,
            phis=phis, stopping_criteria=stopping_crit)
        t2 = time.time()
        print(f"Time for fieldline tracing={t2-t1:.3f}s. Num steps={sum([len(l) for l in fieldlines_tys])//nfieldlines}", flush=True)
        plot_poincare_data(fieldlines_phi_hits, phis, os.path.join(output_dir, f'{label}.png'), dpi=150)


    #interpolation of magnetic field for faster calculation
    n = nfieldlines
    rs = np.linalg.norm(surface.gamma()[:, :, 0:2], axis=2)
    zs = surface.gamma()[:, :, 2]

    print(f'number of field periods: {nfp}')

    rrange = (np.min(rs), np.max(rs), n)
    print(f'r min: {rrange[0]}, r max: {rrange[1]}')

    phirange = (0, 2*np.pi/nfp, n*2)
    print(f'phi min: {phirange[0]}, phi max: {phirange[1]}')

    nz = n
    if FILEDLINE_PARAMS['STELL_SYM']:
        nz = n//2
    zrange = (np.min(zs), np.max(zs), nz)
    print(f'z min: {zrange[0]}, z max: {zrange[1]}')

    print('Initializing InterpolatedField')
    bsh = InterpolatedField(
        bs, degree, rrange, phirange, zrange, extrapolate=True, nfp=nfp, stellsym=FILEDLINE_PARAMS['STELL_SYM'], skip=None
        )

    print('Done initializing InterpolatedField.')

    bsh.set_points(surface.gamma().reshape((-1, 3)))
    bs.set_points(surface.gamma().reshape((-1, 3)))
    Bh = bsh.B()
    B = bs.B()
    print("Mean(|B|) on plasma surface =", np.mean(bs.AbsB()))

    print("|B-Bh| on surface:", np.sort(np.abs(B-Bh).flatten()))

    print('Beginning field line tracing')
    trace_fieldlines(bsh, 'filedlines_' + variant) 

    print("Done calculating Poincare plot")
    print("========================================")

    
    
