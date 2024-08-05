# Power balance simulations

This is the simulation code for the power balance.

Please check first the files simulation_0d.py and simulation_1d_studies.py. These run functions and algorithms from the other files to implement a 0D and 1D simulation, respectively.

Note that the 0D simulation can be done quasi instantaneously.

The 1D simulation first has to run for a while (around 30 minutes for all cases, depending on your processor). Also note that it requires up to around 20GB of memory (RAM). This could be easily reduced to a fraction by not storing every step in memory in the fully_explicit function in simulation_1d.py but I had no time for this optimization.