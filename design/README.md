## Baseline Configuration

The baseline configuration has been provided and re-used from the QUASR database under the MIT License.

Giuliani, A. (2024). QUASR: the QUAsisymmetric Stellarator Repository [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10944430

https://quasr.flatironinstitute.org/model/0021326


## Poincare Plot and Coil Scaling Scripts Documentation

This documentation covers three scripts used for generating Poincare plots and scaling coil designs. These scripts utilize the `simsopt` and `stellopt` libraries to process coil designs, create Poincare plots, and scale designs to desired field strengths and sizes.

### Dependencies
- `simsopt`
- `numpy`
- `os`
- `json`
- `matplotlib`
- Custom libraries:
  - `lib.runPoincare`
  - `lib.pertubateCoils`

### Common Configuration
All scripts require a design folder where they take the input files. Ensure the design folder is correctly set and contains the necessary input files.

---

## `run_simsopt.py`

### Overview
This script creates Poincare plots using `simsopt`. It can also perturb coils and generate Poincare plots from the perturbed coils.

### Design Inputs
- `DESIGN_DIRECTORY`: Directory containing the coil design files.
- `NFP`: Number of field periods. Note: When perturbing a single coil, set to 1.
- `STELLSYM`: Boolean flag for stellarator symmetry.
- `LOG_FIELDLINES`: Boolean flag to log the output of field lines.

### Fieldline Parameters
- `nLines`: Number of field lines to trace.
- `RSTART`: List of R start values for fieldlines
- `ZSTART`: List of Z start values for fieldlines



### Usage
```bash
python run_simsopt.py
```

---

## `run_stellopt.py`

### Overview
This script creates Poincare plots using `stellopt` and also requires `simsopt` for coil perturbation.

### Design Inputs
- `DESIGN_DIRECTORY`: Directory containing the coil design files.
- `NFP`: Number of field periods.
- `STELLSYM`: Boolean flag for stellarator symmetry.
- `LOG_FIELDLINES`: Boolean flag to log the output of field lines.

### Fieldline Parameters
- `nLines`: Number of field lines to trace.
- `nPoints`: Number of points on one phi plane (e.g., number of circles the field line makes).
- `RSTART`: List of R start values for fieldlines
- `ZSTART`: List of Z start values for fieldlines


### Usage
```bash
python run_stellopt.py
```

---

## `scale_coils.py`

### Overview
This script scales the design to the desired field strength and size.

### Design Inputs
- `DESIGN_DIRECTORY`: Directory containing the coil design files.
- `OUTPUT_DIRECTORY`: Directory where the scaled design will be saved.
- `geo_scale`: Geometric scale factor.
- `B_wanted`: Desired magnetic field strength (in Tesla).


### Usage
```bash
python scale_coils.py
```

---
## Additional Components

### Example Input Design Directory
The repository includes an example input design directory that contains necessary files for testing and running the provided scripts. This directory should be used to understand the structure and required contents for running the scripts effectively.

**Note:** The example design is taken from the [QUASR Database](https://quasr.flatironinstitute.org/model/0021326).

### Coil Optimization Code
The repository also contains a script for optimizing coils. This script is built upon a `simsopt` code example and provides functionality for refining coil designs to meet specific criteria or improve performance. Ensure you have the optimization-specific requirements installed and configured.

### SPEC (Stellarator Equilibrium Code) Integration
A simple script is included to run SPEC on the provided design. This script demonstrates how to use SPEC for calculating poincare plots based on the plasma surface. Ensure SPEC is correctly installed and configured on your system to use this script.

---

### Notes
- Modify the design inputs and fieldline parameters as needed to suit specific requirements.
- Ensure that the custom libraries (`lib.runPoincare` and `lib.pertubateCoils`) are available in the script's directory or the Python path.
- Each script requires appropriate setup of the design directory containing necessary input files.

### Contact
For further assistance refer to the `simsopt` and `stellopt` documentation.
