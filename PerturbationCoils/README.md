# General Information
With the scripts in this repository one can perturbe a given set of coils and generate Poincare plots for the new perturbed coil configuration. From the Poincare plots one can estimate how severe imperfections of the coils affect the generated magnetic field.

When testing a new Design make a folder and copy Execuable.py. Within the new DesignFolder generate a "InitialConfiguration" folder and in this folder additionally a "Coils" and "Surface" folder. (e.g. Design_V1.1)

"perturbe_Coil_shape_lib.py" is the library in which all perturbation functions are stored. 
The current perturbations are: "scaling","shift", "wiggling", "current" and "rotationX/Y/Z". Additional information about the perturbations and how they are calculated can be found directly in the library file.

"Executable.py" is the file one needs to execute to generate Poincare plots for the perturbed coil configuration.

# Preperations
You need a running SimsOpt installed
Put your coil_configuration.json into InitialConfiguration/Coils
Put your Vmec_surface_input file into InitialConfiguration/Surface 
Make sure these are the only files in their respective folder!

# How to generate perturbed Poincaré plots
"Executable.py" can be executed directly from Terminal.
e.g.: python Executable.py --pType "scaling" --pSize 0.1 --plot 1
Change into "yourDesignName" directory  
execute: python Executable.py -h to get additional help

Or you can open the script in your code editor and run it from there. In this case you have to perform a few adjustments to the script. Description what to adjust is given in "Executable.py"

The generated plots are saved to a folder called "poincare" (gets generated on the fly if needed)
The chosen naming convention is "pType_pSize.png". Can be adjusted in line 123 saveFileName=...

# Help for calling Executable.py
pType must be string: "scaling", "shift", "wiggle", "current", "rotateX/Y/Z"
    -> further info in pertubate_Coil_shape_lib.py
pSize either 1 value or multiple values seperated by "spacebar": depends on pertubation mode either % randomized disturbance or flat amount.
    -> further info in pertubate_Coil_shape_lib.py
plot 1 or 0: wheter to show the disturbed coil configuration with initial surface 

In line 74 one can change the number of coils, which get perturbed. For our current design of 12 coils, where we have 3 base coils which get rotated and shifted 4 times, a maximum of 3 is possible. When setting the range to 3, then all 3 base coils get perturbed. 
Additionally one can change how the output coil is generated so that either just the base coil or all similar coils get perturbed. Therefore you need to change curve_out = CurveXYZFourier(coil_in.curve.quadpoints, order) (only basecoil) to curve_out = curve_in (all similar coils) in perturbe_Coil_shape_lib.py. This has to be done for the desired perturbation type.

# possible Errors
## in Executable.py
In line 140: The radial range in which the the fieldline tracer starts its tracing, defined by R0, depends on the size of the flux surface at hand and may need adjustment, got the current value mainly by trial and error.
In line 150: uncomment if you also want to generate VTK files
In line 116-119: one can adjust these parameters for a higher resolved plot with more flux surfaces -> can also lead to termination if chosen bad.
In the interpolation of the magnetic field starting on line 153 one also needs to adjust rrange and zrange according to the magnetic field.

# Acknowledgement
Mainly taken and adjusted from the SimsOpt example "1_Simple/tracing_fieldlines_QA.py"