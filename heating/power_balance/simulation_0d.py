
import numpy as np
import matplotlib.pyplot as plt
import utils
import simulation_common

ion_masses_kg = {"hydrogen": 1 * simulation_common.proton_mass_kg, "helium": 4 * simulation_common.proton_mass_kg, "argon": 40 * simulation_common.proton_mass_kg}

def coulomb_logarithm(electron_density_Dcm3, ion_density_Dcm3, ion_charge_number, ion_mass_kg, ion_temperature_eV, electron_temperature_eV):
    """Calculates the coulomb logarithm ln Λ for electron-ion collisions, assuming maxwellian distribution.
    source: https://farside.ph.utexas.edu/teaching/plasma/Plasma/node39.html

    Parameters:
      ion_charge_number: this is not necessarily the same as the nuclear charge number (e.g. in case the plasma is not fully ionized)
    """
    result = np.empty_like(electron_temperature_eV, dtype=np.float64)
    formula1_condition = electron_temperature_eV < ion_temperature_eV * simulation_common.electron_mass_kg / ion_mass_kg
    formula2_condition = np.logical_and(np.logical_not(formula1_condition), electron_temperature_eV < 10 * ion_charge_number**2)
    formula3_condition = np.logical_and(np.logical_not(formula1_condition), np.logical_not(formula2_condition))

    formula1 = (30 - np.log(electron_density_Dcm3**0.5 * ion_temperature_eV**(-1.5) * ion_charge_number**1.5 * (ion_mass_kg / simulation_common.proton_mass_kg))) * np.ones_like(electron_temperature_eV)
    formula2 = 23 - np.log(electron_density_Dcm3**0.5 * ion_charge_number * electron_temperature_eV**(-1.5))
    formula3 = 24 - np.log(electron_density_Dcm3**0.5 * electron_temperature_eV**(-1))

    result[formula1_condition] = formula1[formula1_condition]
    result[formula2_condition] = formula2[formula2_condition]
    result[formula3_condition] = formula3[formula3_condition]
    return result

def coulomb_logarithm_test():
    # to compare with Stroth PDF p. 280, which lists coulomb logarithm = 17 for T = 100, 1000 and 10000 eV
    print(coulomb_logarithm(2e12, 2e12, 1, simulation_common.proton_mass_kg, 1000, 1000))  # 16.75 -> quite good

    t = np.linspace(3, 40)
    plt.plot(t, coulomb_logarithm(2e11, 2e11, 1, simulation_common.proton_mass_kg, 300 * simulation_common.boltzmann_constant_JDK / simulation_common.electron_charge_C, t), label='electron & ion density = 2e11 / cm³')
    plt.plot(t, coulomb_logarithm(2e12, 2e12, 1, simulation_common.proton_mass_kg, 300 * simulation_common.boltzmann_constant_JDK / simulation_common.electron_charge_C, t), label='electron & ion density = 2e12 / cm³')
    plt.plot(t, coulomb_logarithm(2e13, 2e13, 1, simulation_common.proton_mass_kg, 300 * simulation_common.boltzmann_constant_JDK / simulation_common.electron_charge_C, t), label='electron & ion density = 2e13 / cm³')
    plt.xlabel('electron & ion temperature [eV]')
    plt.ylabel('coulomb logarithm')
    utils.make_clickable_legend('lower right')

def calc_ion_density_simplified_Dm3(heating_power_rf_W, neutral_density_Dm3, volume_m3, gamma, alpha, electron_temperature_eV, ionization_energy_eV, ionization_rate_coefficient_m3Ds, radiation_neutral_energy_rate_coefficient_eVm3Ds):
    """ implements equation 12 from the Lechte paper
    (the ion density is taken to be equal to the electron density)
    This equation neglects recombination and elastic (coulomb) losses, as well as losses through excitation of ions (latter one only relevant for nuclear charge Z > 1)
    Note: At the low neutral densities, radiation losses are mainly due to ion excitation, which means that Eq. 12 may not be used

    alpha: fraction of the bulk plasma temperature that determines the temperature at the plasma border T_e_border = α * T_e
    gamma: ratio between heat diffusivity and particle diffusivity, ɣ = χ / D
    """
    return (heating_power_rf_W / (neutral_density_Dm3 * volume_m3)) / (((gamma + 3/2 * alpha) * electron_temperature_eV + ionization_energy_eV) * ionization_rate_coefficient_m3Ds(electron_temperature_eV) + radiation_neutral_energy_rate_coefficient_eVm3Ds(electron_temperature_eV)) / simulation_common.electron_charge_C

def calc_ion_density_Dm3(heating_power_rf_W, neutral_density_Dm3, volume_m3, gamma, alpha, electron_temperature_eV, ionization_energy_eV, ionization_rate_coefficient_m3Ds, radiation_neutral_energy_rate_coefficient_eVm3Ds, ion_mass_kg, coulomb_logarithm, ion_temperature_eV, radiation_ion_energy_rate_coefficient_eVm3Ds):
    """ calculates the density using equations 8, 9 and 11 from the Lechte paper
    (the ion density is taken to be equal to the electron density)

    alpha: fraction of the bulk plasma temperature that determines the temperature at the plasma border T_e_border = α * T_e
    gamma: ratio between heat diffusivity and particle diffusivity, ɣ = χ / D
    """
    # we are measuring energies in eV here -> the only thing to adjust is the heating power to be eV/s instead of W/s

    # # this system would correspond to the simplified equation which is already given in the paper
    # a = 0
    # b = -volume_m3 * (ionization_energy_eV * ionization_rate_coefficient_m3Ds(electron_temperature_eV) * neutral_density_Dm3
    #    + radiation_neutral_energy_rate_coefficient_eVm3Ds(electron_temperature_eV) * neutral_density_Dm3) - (gamma + 3/2 * alpha) * electron_temperature_eV * volume_m3 * (ionization_rate_coefficient_m3Ds(electron_temperature_eV) * neutral_density_Dm3)
    # c = heating_power_rf_W / electron_charge_C

    # system without simplifications
    # Note: recombination practially does not change anything
    recombination_energy_eV = ionization_energy_eV
    electron_ion_relaxation_time_without_density_sDm3 = (4 * np.pi * simulation_common.dielectricity_constant_C2DNm2 / simulation_common.electron_charge_C**2)**2 * 3 * ion_mass_kg * (electron_temperature_eV * simulation_common.electron_charge_C)**1.5 / (8 * np.sqrt(2 * np.pi * simulation_common.electron_mass_kg) * coulomb_logarithm)
    Q_eVm3Ds = 3/2 * (electron_temperature_eV - ion_temperature_eV) / electron_ion_relaxation_time_without_density_sDm3
    a = -volume_m3 * (recombination_energy_eV * simulation_common.calc_recominbation_rate_coefficient_m3Ds(electron_temperature_eV)
         + radiation_ion_energy_rate_coefficient_eVm3Ds(electron_temperature_eV)
         + Q_eVm3Ds) - (gamma + 3/2 * alpha) * (-simulation_common.calc_recominbation_rate_coefficient_m3Ds(electron_temperature_eV))
    b = -volume_m3 * (ionization_energy_eV * ionization_rate_coefficient_m3Ds(electron_temperature_eV) * neutral_density_Dm3
         + radiation_neutral_energy_rate_coefficient_eVm3Ds(electron_temperature_eV) * neutral_density_Dm3) - (gamma + 3/2 * alpha) * electron_temperature_eV * volume_m3 * (ionization_rate_coefficient_m3Ds(electron_temperature_eV) * neutral_density_Dm3)
    c = heating_power_rf_W / simulation_common.electron_charge_C

    x1, x2 = utils.solve_quadratic_equation(a, b, c)
    assert(np.all(x2 < 0))  # we can safely drop the second solution
    Q_fraction = Q_eVm3Ds * volume_m3 * x1**2 / (heating_power_rf_W / simulation_common.electron_charge_C)
    return x1, Q_fraction

def figure6_simplified():
    """ reproduction of figure 6 in the Lechte paper with the simplified formula for electron & ion density.
    Very nice alignment for electron temperature > 10 eV
    """
    electron_temperature_eV = np.linspace(1,40)

    def plot(element, dashes):
        ion_density_Dm3 = calc_ion_density_simplified_Dm3(heating_power_rf_W=3000,
            neutral_density_Dm3=2e18,
            volume_m3=0.12,
            gamma=0,
            alpha=0.5,
            electron_temperature_eV=electron_temperature_eV,
            ionization_energy_eV=simulation_common.ionization_energies_eV[element],
            #radiation_neutral_energy_eV=average_radiation_neutral_energies_eV[element],
            ionization_rate_coefficient_m3Ds=lambda T: simulation_common.ionization_rate_coefficient_m3Ds(element, T),
            radiation_neutral_energy_rate_coefficient_eVm3Ds=lambda T: simulation_common.radiation_neutral_energy_rate_coefficient_eVm3Ds(element, T))
        plt.semilogy(electron_temperature_eV, ion_density_Dm3, label=element, dashes=dashes)

    plt.figure()
    plot('hydrogen', (1, 0))
    plot('helium', (5, 5))
    plot('argon', (10, 10))

    plt.grid('both')
    plt.xlabel('electron temperature [eV]')
    plt.ylabel('electron or ion density [1 / m³]')
    plt.xlim([0, 40])
    plt.ylim([1e16, 1e20])
    plt.legend()

def figure6():
    """ reproduction of figure 6 in the Lechte paper (excellent agreement)
    """
    electron_temperature_eV = np.linspace(1, 40, 200)

    figure6_, figure6_ax = plt.subplots()
    figure5_, figure5_ax = plt.subplots()

    def plot(element, dashes):
        # ion_density_Dm3 = calc_ion_density_simplified_Dm3(heating_power_rf_W=3000,
        #     neutral_density_Dm3=2e18,
        #     volume_m3=0.12,
        #     gamma=0,
        #     alpha=0.5,
        #     electron_temperature_eV=electron_temperature_eV,
        #     ionization_energy_eV=ionization_energies_eV[element],
        #     #radiation_neutral_energy_eV=average_radiation_neutral_energies_eV[element],
        #     ionization_rate_coefficient_m3Ds=lambda T: ionization_rate_coefficient_m3Ds(element, T),
        #     radiation_neutral_energy_rate_coefficient_eVm3Ds=lambda T: radiation_neutral_energy_rate_coefficient_eVm3Ds(element, T))
        # figure6_ax.semilogy(electron_temperature_eV, ion_density_Dm3, label=element + ' simplified', dashes=dashes)

        ion_density_Dm3, Q = calc_ion_density_Dm3(heating_power_rf_W=3000,
            neutral_density_Dm3=2e18,
            volume_m3=0.12,
            gamma=0,
            alpha=0.5,
            electron_temperature_eV=electron_temperature_eV,
            ionization_energy_eV=simulation_common.ionization_energies_eV[element],
            #radiation_neutral_energy_eV=average_radiation_neutral_energies_eV[element],
            ionization_rate_coefficient_m3Ds=lambda T: simulation_common.ionization_rate_coefficient_m3Ds(element, T),
            radiation_neutral_energy_rate_coefficient_eVm3Ds=lambda T: simulation_common.radiation_neutral_energy_rate_coefficient_eVm3Ds(element, T),
            ion_mass_kg=ion_masses_kg[element],
            coulomb_logarithm=17,  # 12 would probably be more accurate, but Prof. Stroth assumed 17 in his book and also, it fits much better to figure 6. Therefore I think they used 17
            ion_temperature_eV=300 * simulation_common.boltzmann_constant_JDK / simulation_common.electron_charge_C,  # Lechte p. 2840 middle right "The fixed properties are ion and neutral gas temperature, which are taken to be cold (300 K)"
            radiation_ion_energy_rate_coefficient_eVm3Ds=lambda T: simulation_common.radiation_ion_energy_rate_coefficient_eVm3Ds(element, T))
        figure6_ax.semilogy(electron_temperature_eV, ion_density_Dm3, label=element, dashes=dashes)
        #figure5_ax.plot(electron_temperature_eV, Q, label=element + ' Q', dashes=dashes)

    plot('hydrogen', (1, 0))
    plot('helium', (5, 5))
    plot('argon', (10, 10))

    utils.make_clickable_legend(fig=figure6_, ax=figure6_ax)
    figure6_ax.set_xlabel('electron temperature [eV]')
    figure6_ax.set_ylabel('electron or ion density [1 / m³]')
    figure6_ax.set_xlim([0, 40])
    figure6_ax.set_ylim([1e16, 1e20])

    # utils.make_clickable_legend(fig=figure5_, ax=figure5_ax)
    # figure5_ax.set_xlabel('electron temperature [eV]')
    # figure5_ax.set_ylabel('power fraction')
    # figure5_ax.set_xlim([0, 40])
    # figure5_ax.set_ylim([0, 1])

def figure7_simplified():
    """ reproduction of figure 7 in the Lechte paper with the simplified formula for electron & ion density.
    good agreement only for neutral_density_Dm3 = 2e19 and 2e18, but not 2e17
    """

    def plot(element, dashes):
        electron_temperature_eV = np.linspace(1, 40, 200)
        ion_density_Dm3 = calc_ion_density_simplified_Dm3(heating_power_rf_W=3000,
            neutral_density_Dm3=2e19,
            volume_m3=0.12,
            gamma=0,
            alpha=0.5,
            electron_temperature_eV=electron_temperature_eV,
            ionization_energy_eV=simulation_common.ionization_energies_eV[element],
            #radiation_neutral_energy_eV=average_radiation_neutral_energies_eV[element],
            ionization_rate_coefficient_m3Ds=lambda T: simulation_common.ionization_rate_coefficient_m3Ds(element, T),
            radiation_neutral_energy_rate_coefficient_eVm3Ds=lambda T: simulation_common.radiation_neutral_energy_rate_coefficient_eVm3Ds(element, T))
        plt.semilogy(electron_temperature_eV, ion_density_Dm3, label=element, dashes=dashes)

    plt.figure()
    plot('hydrogen', (1, 0))
    plot('helium', (5, 5))
    plot('argon', (10, 10))

    plt.grid('both')
    plt.xlabel('electron temperature [eV]')
    plt.ylabel('electron or ion density [1 / m³]')
    plt.legend()
    plt.xlim([0, 40])
    plt.ylim([1e15, 1e19])

def figure7():
    """ reproduction of figure 7 in the Lechte paper. Excellent agreement. Use for verification of the algorithm.

    Note: because the gamma=0 here, heat_diffusivity=0 and the only free parameter is the particle_diffusivity D.
    "A change of plasma parameters with B indicates a change in transport" (Lechte 2002 p. 6) which is reflected
    by a different diffusivity D.
    This means that to reach high electron temperature at lower density, or high density at lower electron temperature,
    one must change the magnetic field configuration (e.g. the field strength).
    """

    volume_m3 = 0.12
    heating_power_rf_W = 3000

    figure7_, figure7_ax = plt.subplots()

    def plot(element, neutral_density_Dm3, dashes, color=None):
        electron_temperature_eV = np.linspace(1, 40, 200)
        ion_density_Dm3, _ = calc_ion_density_Dm3(heating_power_rf_W=heating_power_rf_W,
            neutral_density_Dm3=neutral_density_Dm3,
            volume_m3=volume_m3,
            gamma=0,
            alpha=0.5,
            electron_temperature_eV=electron_temperature_eV,
            ionization_energy_eV=simulation_common.ionization_energies_eV[element],
            #radiation_neutral_energy_eV=average_radiation_neutral_energies_eV[element],
            ionization_rate_coefficient_m3Ds=lambda T: simulation_common.ionization_rate_coefficient_m3Ds(element, T),
            radiation_neutral_energy_rate_coefficient_eVm3Ds=lambda T: simulation_common.radiation_neutral_energy_rate_coefficient_eVm3Ds(element, T),
            ion_mass_kg=ion_masses_kg[element],
            coulomb_logarithm=17,  # 12 would probably be more accurate, but Prof. Stroth assumed 17 in his book and also, it fits much better to figure 6. Therefore I think they used 17
            ion_temperature_eV=300 * simulation_common.boltzmann_constant_JDK / simulation_common.electron_charge_C,  # Lechte p. 2840 middle right "The fixed properties are ion and neutral gas temperature, which are taken to be cold (300 K)"
            radiation_ion_energy_rate_coefficient_eVm3Ds=lambda T: simulation_common.radiation_ion_energy_rate_coefficient_eVm3Ds(element, T))
        figure7_ax.semilogy(electron_temperature_eV, ion_density_Dm3, label=f'{element} n0={neutral_density_Dm3} 1/m³', color=color, dashes=dashes)

    colors = ['r', 'g', 'b']
    for i, neutral_density_Dm3 in enumerate([2e17, 2e18, 2e19]):
        plot('hydrogen', neutral_density_Dm3, (1, 0), colors[i])
        plot('helium', neutral_density_Dm3, (5, 5), colors[i])
        plot('argon', neutral_density_Dm3, (10, 10), colors[i])

    utils.make_clickable_legend(fig=figure7_, ax=figure7_ax)
    figure7_ax.set_xlabel('electron temperature T [eV]')
    figure7_ax.set_ylabel('electron density (=ion density) $n_e$ [1 / m³]')
    figure7_ax.set_xlim([0, 40])
    figure7_ax.set_ylim([1e15, 1e19])
    figure7_ax.set_title(f'V={volume_m3} m³, $P_{{rf}}$={heating_power_rf_W} W')

def figure7_tum_graz_033():
    """Runs the 0D simulation, applying a scaling factor of 0.33 of the chosen Graz/TUM design
    """

    volume_m3 = 0.04435 # 0.078 #0.27 #0.12
    heating_power_rf_W = 3000

    figure7_, figure7_ax = plt.subplots(figsize=(12, 5))

    def plot(element, neutral_density_Dm3, dashes, color=None):
        electron_temperature_eV = np.linspace(1, 40, 200)
        ion_density_Dm3, _ = calc_ion_density_Dm3(heating_power_rf_W=heating_power_rf_W,
            neutral_density_Dm3=neutral_density_Dm3,
            volume_m3=volume_m3,
            gamma=0,
            alpha=0.5,
            electron_temperature_eV=electron_temperature_eV,
            ionization_energy_eV=simulation_common.ionization_energies_eV[element],
            #radiation_neutral_energy_eV=average_radiation_neutral_energies_eV[element],
            ionization_rate_coefficient_m3Ds=lambda T: simulation_common.ionization_rate_coefficient_m3Ds(element, T),
            radiation_neutral_energy_rate_coefficient_eVm3Ds=lambda T: simulation_common.radiation_neutral_energy_rate_coefficient_eVm3Ds(element, T),
            ion_mass_kg=ion_masses_kg[element],
            coulomb_logarithm=17,  # 12 would probably be more accurate, but Prof. Stroth assumed 17 in his book and also, it fits much better to figure 6. Therefore I think they used 17
            ion_temperature_eV=300 * simulation_common.boltzmann_constant_JDK / simulation_common.electron_charge_C,  # Lechte p. 2840 middle right "The fixed properties are ion and neutral gas temperature, which are taken to be cold (300 K)"
            radiation_ion_energy_rate_coefficient_eVm3Ds=lambda T: simulation_common.radiation_ion_energy_rate_coefficient_eVm3Ds(element, T))
        figure7_ax.semilogy(electron_temperature_eV, ion_density_Dm3, label=f'{element} $n_\\mathrm{{neu}}$={neutral_density_Dm3} 1/m³', color=color, dashes=dashes)

    colors = ['r', 'g', 'b']
    for i, neutral_density_Dm3 in enumerate([2e17, 2e18, 2e19]):
        plot('hydrogen', neutral_density_Dm3, (1, 0), colors[i])
        plot('helium', neutral_density_Dm3, (5, 5), colors[i])
        plot('argon', neutral_density_Dm3, (10, 10), colors[i])

    utils.make_clickable_legend(fig=figure7_, ax=figure7_ax)
    figure7_ax.set_xlabel('electron temperature T [eV]')
    figure7_ax.set_ylabel('electron density (=ion density) $n_e$ [1 / m³]')
    figure7_ax.set_xlim([0, 40])
    figure7_ax.set_ylim([1e15, 1e19])
    figure7_ax.set_title(f'V={volume_m3} m³, $P_{{rf}}$={heating_power_rf_W} W')

if __name__ == "__main__":
    figure7_tum_graz_033()
    plt.show()