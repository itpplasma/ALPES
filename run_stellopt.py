import simsopt.field
import lib.runPoincare as rp
import lib.pertubateCoils as pc
import numpy as np
import simsopt
import os
import json

####### DESIGN INPUTS ######
DESIGN_DIRECTORY = 'Scaled_Design'

NFP = 1
STELLSYM = False
LOG_FIELDLINES = True       # If True, print the output of xfiledlines to the console

input_file_path = rp.verifyInputDirectory(DESIGN_DIRECTORY)

output_dir = os.path.join(DESIGN_DIRECTORY, 'STELLOPT')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
####### FIELDLINE PARAMETERS ######

nLines = 20                 # Number of field lines to trace
nPoints = 500              # 

# Define the fieldline parameters
define_new_parameters = True
if define_new_parameters:
    PHI_END = np.ceil(nPoints * 2 * np.pi * 10)/10
    RSTART = (np.linspace(1.095, 1.25, nLines) * 0.33).tolist()
    ZSTART = np.zeros(nLines).tolist()
    PHISTART = np.zeros(nLines).tolist()
    PHIEND = (np.ones(nLines) * PHI_END).tolist()
    PHIPLANES = [0, np.pi/4,  np.pi/2] 

    FILEDLINE_PARAMS = {
        "LASYM": "F",
        "NFP": NFP,
        "MPOL": 10,
        "NTOR": 10,
        "NZETA": 40 * 4,
        "EXTCUR": [],

        "NR": 201,
        "NPHI": 40 * 4,
        "NZ": 201,
        "RMIN": 0.25 * 0.33,
        "RMAX": 1.55 * 0.33,
        "ZMIN": -0.65 * 0.33,
        "ZMAX": 0.65 * 0.33,
        "MU": 0.0,
        "NPOINC": 32,
        "R_START": RSTART,
        "Z_START": ZSTART,
        "PHI_START": PHISTART,
        "PHI_END": PHIEND,
        "INT_TYPE": "LSODE",
        "FOLLOW_TOL": 1e-12,
        "VC_ADAPT_TOL": 1e-7,

        "KEEP_INDATA": False,
        "LOG_FIELDLINES": LOG_FIELDLINES,
    }

    ####### PLOT PARAMETERS ######

    PLOT_PARAMS = {
        "NPOINC": 32,
        "PHIPLANES": PHIPLANES,
        "SAVE": True,
        "SHOW": False,
        "KEEP_RESULT_DATA": False,
        "RLIM": [0.5 * 0.33, 1.4 * 0.33],
        "ZLIM": [-0.42 * 0.33, 0.42 * 0.33]
    }

    # save the fieldline parameters to json file
    with open(os.path.join(output_dir, 'fieldline_params.json'), 'w') as f:
        json.dump((FILEDLINE_PARAMS, PLOT_PARAMS), f)

# load the fieldline parameters
with open(os.path.join(output_dir, 'fieldline_params.json'), 'r') as f:
    FILEDLINE_PARAMS, PLOT_PARAMS = json.load(f)


####### BASELINE ######
# Set to True to run without perturbations
RUN_BASELINE = True

####### PERTURBATIONS ######
# Set to True to save BioSavar opject of perturbaated coils
SAVE_PERTURBATIONS = True

# Set to True to run with shifted coils
RUN_SHIFTED_COILS = True
# Set array of coils to shift
SHIFTED_COILS = [0]
# Set the shifts to apply
SHIFTS = np.arange(0.03, 0.051, 0.01)#np.linspace(0.0001, 0.01, 10)

# Set to True to run with perturbated current
RUN_PERTURBATED_CURRENT = False
# Set array of coils to perturbate
PERTURBATED_COILS = [0,3,6,9]
# Set the perturbation amplitude in percentage (0.1 = 10%)
PERTURBATION_AMPLITUDE = np.linspace(0.006, 0.01, 5)




#---------------------------------#
# load the file acording to your input file. Outcommand the one you are not using

# load the input file option 1
# surfaces, B_axis, coils_in = simsopt.load(input_file_path)
# n_basecoils = len(coils_in) #//(NFP * (1 + int(STELLSYM)))
# coils = coils_in[:n_basecoils]
# bs = simsopt.field.BiotSavart(coils)
# print(f'Number of coils: {len(coils)}')

# load the input file option 2
bs = simsopt.load(input_file_path)
coils = bs.coils
for i, c in enumerate(coils):
    print(f'Coil {i} Current: {c.current.get_value()}')

FILEDLINE_PARAMS["EXTCUR"] = [c.current.get_value() for c in coils]

#---------------------------------#
if RUN_BASELINE:
    print("Running baseline...")
    # Check if the directory exists and create it if it doesn't
    output_dir = os.path.join(DESIGN_DIRECTORY, 'STELLOPT', 'BASELINE')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    variant = 'BASELINE'
    rp.run_poincare_xfieldlines(coils, variant, output_dir, NFP, FILEDLINE_PARAMS, PLOT_PARAMS, SAVE_PERTURBATIONS)

if RUN_SHIFTED_COILS:
    print("Running shifted coils...")
    # Check if the directory exists and create it if it doesn't
    output_dir = os.path.join(DESIGN_DIRECTORY, 'STELLOPT', 'SHIFTS')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for shift in SHIFTS:
        variant = f'{shift:.4f}_Shift'
        shifted_coils = coils.copy()
        for i in SHIFTED_COILS:
            trans_vec = np.array([shift, 0, 0])
            shifted_coil = pc.translate_coil(coils[i], trans_vec)
            shifted_coils[i] = shifted_coil

        rp.run_poincare_xfieldlines(shifted_coils, variant, output_dir, NFP, FILEDLINE_PARAMS, PLOT_PARAMS, SAVE_PERTURBATIONS)

if RUN_PERTURBATED_CURRENT:
    print("Running perturbated current...")
    # Check if the directory exists and create it if it doesn't
    output_dir = os.path.join(DESIGN_DIRECTORY, 'STELLOPT', 'CURRENT_PERTURBATION')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for p in PERTURBATION_AMPLITUDE:
        variant = f'{p:.3f}_Current_Perturbation'
        pertupated_coils = coils.copy()   
        for i in PERTURBATED_COILS:
            current = coils[i].current
            print(f'unpertubated current: {current.get_value()}')
            p_current  = current * (1+p)
            pertupated_coils[i] = simsopt.field.Coil(coils[i].curve, p_current)
            print(f'pertubated current: {pertupated_coils[i].current.get_value()}')
        
        FILEDLINE_PARAMS["EXTCUR"] = [c.current.get_value() for c in pertupated_coils]
        rp.run_poincare_xfieldlines(pertupated_coils, variant, output_dir, NFP, FILEDLINE_PARAMS, PLOT_PARAMS, SAVE_PERTURBATIONS)

