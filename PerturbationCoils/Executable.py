import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import argparse
import numpy as np
from simsopt.geo import SurfaceRZFourier, plot
from simsopt.field import BiotSavart
from perturbe_Coil_shape_lib import *
import time
import logging
from pathlib import Path
import simsopt
from simsopt.field import (BiotSavart, InterpolatedField, SurfaceClassifier, particles_to_vtk,
                           compute_fieldlines, LevelsetStoppingCriterion, plot_poincare_data)
from simsopt.geo import SurfaceRZFourier
from simsopt.util import proc0_print, comm_world


def main():
    ###---------- Comment this block if you don't want to call it from Terminal
    parser = argparse.ArgumentParser()
    
    # Add arguments with default values
    parser.add_argument('--pType', '--pt', type=str, default="scaling", choices=['scaling', 'shift', 'wiggling', 'current', 'rotateX', 'rotateY', 'rotateZ'], help='What kind of pertubation should be performed. 7 possibilities')
    parser.add_argument('--pSize', '--ps', type=float, nargs='*', default=np.linspace(-0.01,0.01,20), help='What is the size of the pertubation. Accepts multiple inputs simulataneously seperated by "spacebar".')
    parser.add_argument('--plot', '--p', type=int, choices=[0, 1], default=0, help='1:Plot perturbed coil arrangement with initial magnetic field')
    parser.add_argument('--axis', '--a', type=float, )

    # Parse the arguments
    args = parser.parse_args()
    if args.pType == 'shift' and args.axis is None:
        parser.error("--axis is required when --pType is 'shift'")

    pertubationType = args.pType
    pertubationFactors = args.pSize
    plotCoil = args.plot
    ax = args.axis

    ### Instead write desired pertubationType and Size directly into the variables
    '''
    pertubationType = "scaling"
    pertubationFactors = [1.00001]
    plotCoil = False
    '''

    ### -------- End of Initialization


    coilsFolder = "./InitialConfiguration/Coils/"
    surfaceFolder = "./InitialConfiguration/Surface/"
    
    opt_coils_filename = os.path.join(coilsFolder, os.listdir(coilsFolder)[0])
    target_surface_filename = os.path.join(surfaceFolder, os.listdir(surfaceFolder)[0])

    nphi = 200
    ntheta = 30

    # Random but periodic pertubation of coils 
    for pertubationfactor in pertubationFactors:
        
        proc0_print("Pertubate Coil")
        proc0_print("=========================================")
        # reads the simsopt input file: [0]...surfaceXYZ, [1]...magnetic axis, [2]...coils
        bs = BiotSavart.from_file(opt_coils_filename)
        bs = BiotSavart(bs[2])
        # reads vmec surface input file: surfaceRZ
        surface = SurfaceRZFourier.from_vmec_input(target_surface_filename, range="full torus", nphi=nphi, ntheta=ntheta)
        nfp = 1  # number of field periods, when perturbing you cant use any symmetry anymore

        # pertupate coils N1
        coils = bs.coils

        # assumes 3 coils per half period
        for coil_n in range(0, 1):
            
            coil_p1 = coils[coil_n]

            if pertubationType == 'scaling':
                coil_p1 =  scale_coil(coil_p1, scalefactor=pertubationfactor)
            elif pertubationType == 'shift':
                coil_p1 = shift_coil(coil_p1,axis=ax,amount=pertubationfactor)
            elif pertubationType == 'wiggling':
                coil_p1 = wiggle_coil(coil_p1,disturbance_mode=pertubationfactor)
            elif pertubationType == 'current':
                coil_p1 = scale_current(coil_p1, scalefactor=pertubationfactor)
            elif pertubationType == 'rotateX':
                coil_p1 = rotate_coil_x(coil_p1, angle=pertubationfactor)
            elif pertubationType == 'rotateY':
                coil_p1 = rotate_coil_y(coil_p1, angle=pertubationfactor)
            elif pertubationType == 'rotateZ':
                coil_p1 = rotate_coil_z(coil_p1, angle=pertubationfactor)
            else:
                errMsg = "Unknown pertubation Mode: got " + pertubationType +" but expected, scaling/wiggling/current"
                raise ValueError(errMsg)
            
            #replace the initial coil with the perturbed coil
            coils[coil_n] = coil_p1
        
        #calculate BiotSavart for perturbed coils
        bs_p1 = BiotSavart(coils)

        proc0_print("Done perturbating coils")
        proc0_print("========================================")

        #plot perturbed coils with initial surface
        if plotCoil:
            plot(coils + [surface], engine="plotly", close=True)

        proc0_print("Calculate Poincaré Plot")
        proc0_print("=========================================")

        logging.basicConfig()
        logger = logging.getLogger('simsopt.field.tracing')
        logger.setLevel(1)

        degree = 4          #for interpolation
        nfieldlines = 20    #how many fieldlines one wants to trace
        tmax_fl = 50000      #duration of simulation, the longer the more intersections with poincare plot
        tol = 1e-12        #accuracy of ODE solution when tracing field lines


        # Directory for output
        saveFileName = pertubationType + "_" + str(pertubationfactor)
        OUT_DIR = "./poincare/" 
        os.makedirs(OUT_DIR, exist_ok=True)

    
        sc_fieldline = SurfaceClassifier(surface, h=0.03, p=2)
        #sc_fieldline.to_vtk(OUT_DIR + 'levelset', h=0.02)

        stopping_crit = [LevelsetStoppingCriterion(sc_fieldline.dist)]


        def trace_fieldlines(bfield, label):
            t1 = time.time()
            # Set initial grid of points for field line tracing, going from
            # the magnetic axis to the surface. 
            # The Values of R0 were a bit trial and error and may need adjustment
            # for different configurations
            R0 = np.linspace(1.094, 0.975, nfieldlines)
            Z0 = np.zeros(nfieldlines)
            phis = [(i/4)*(2*np.pi/nfp) for i in range(4)] #4 cuts
        
            fieldlines_tys, fieldlines_phi_hits = compute_fieldlines(
                bfield, R0, Z0, tmax=tmax_fl, tol=tol, comm=comm_world,
                phis=phis, stopping_criteria=stopping_crit)
            t2 = time.time()
            proc0_print(f"Time for fieldline tracing={t2-t1:.3f}s. Num steps={sum([len(l) for l in fieldlines_tys])//nfieldlines}", flush=True)
            if comm_world is None or comm_world.rank == 0:
                #particles_to_vtk(fieldlines_tys, OUT_DIR + f'fieldlines_{label}')
                plot_poincare_data(fieldlines_phi_hits, phis, OUT_DIR + f'{label}.png', dpi=150)

        #interpolation of magnetic field for faster calculation
        n = nfieldlines
        rs = np.linalg.norm(surface.gamma()[:, :, 0:2], axis=2)
        zs = surface.gamma()[:, :, 2]

        print(f'number of field periods: {nfp}')

        rrange = (0.4, 1.5, n)
        print(f'r min: {rrange[0]}, r max: {rrange[1]}')

        phirange = (0, 2*np.pi/nfp, n*2)
        print(f'phi min: {phirange[0]}, phi max: {phirange[1]}')

        zrange = (-0.4, 0.4, n)
        print(f'z min: {zrange[0]}, z max: {zrange[1]}')
        
        proc0_print('Initializing InterpolatedField')
        bsh = InterpolatedField(
            bs_p1, degree, rrange, phirange, zrange, extrapolate=True, nfp=nfp, stellsym=False, skip=None
            )

        proc0_print('Done initializing InterpolatedField.')

        bsh.set_points(surface.gamma().reshape((-1, 3)))
        bs_p1.set_points(surface.gamma().reshape((-1, 3)))
        Bh = bsh.B()
        B = bs_p1.B()
        proc0_print("Mean(|B|) on plasma surface =", np.mean(bs_p1.AbsB()))

        proc0_print("|B-Bh| on surface:", np.sort(np.abs(B-Bh).flatten()))

        proc0_print('Beginning field line tracing')
        trace_fieldlines(bsh, saveFileName )

        proc0_print("Done calculating Poincare plot")
        proc0_print("========================================")


# Execute Script
if __name__ == "__main__":
    main()
