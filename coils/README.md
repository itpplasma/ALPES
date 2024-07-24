## Read the 3D-coordinates and get the total forces on the coils
- coils_xyz - folder
- load your data into coilData (we are using a total of 12 coils with 3 circuits)
- let magnetix.py run (depending on your system, you apparently need to change 'coilData/coil_coordinates0.txt' to 'coilData\coil_coordinates0.txt')

## make some basic assumptions and get possible systems
- the system is testing for different number of coils values
- you can plug in your basic assumtions on the magnetic field, you wanna have, in `definitions.py`
- basically all you wanna do is in functions and definitions
- the calculations of all other parameters is done in functions.py in the function calculations
- the definition of the calculations is done in definitions
- the crossection of a coil is specifically defined in geometric_object.py in order to allowthe tests of different crossections. right now, we have only round though
- in order to calculate the pressure drop in the coil, the folder pressure_loss_calculator is used.
- the script crosssection.py gives you nice pictures of the crossection. the script variant.py is a dead weight on that, which cant be removed
