
import numpy as np
import matplotlib.pyplot as plt

"""
all variable names consist of <name>_<unit>, where unit is as follows:
Example: m3Ds -> m^3 / s
"""

# fundamental constants
electron_charge_C = 1.602176634e-19
proton_mass_kg = 1.6726219236951e-27
electron_mass_kg = 9.109383701528e-31
dielectricity_constant_C2DNm2 = 8.85418781e-12
boltzmann_constant_JDK = 1.380649e-23

# source: Lechte paper p. 2841 upper right
ionization_energies_eV = {"hydrogen": 13.6, "helium": 24.6, "argon": 15.8}

# source: Lechte paper table 1
ionization_rate_fit_coefficients = {
    "hydrogen": np.array([-46.34625936, 14.12846381, -6.76207354, 2.20991565, -0.51207028, 0.08100631, -0.00797476, 0.00037152]),
    "helium": np.array([-58.28791854, 25.15162851, -12.23322030, 4.01354839, -0.93464539, 0.15195642, -0.01568699, 0.00076701]),
    "argon": np.array([-47.12972660, 16.30483053, -7.83910110, 2.52813121, -0.56165759, 0.08389509, -0.00783425, 0.00035332]),
}

# source: Lechte paper p. 2841 lower right. Hydrogen -> see table 2 / radiation_neutral_energy_rate_hydrogen_Wcm3
average_radiation_neutral_energies_eV = {"hydrogen": None, "helium": 19.8, "argon": 11.5}

# source: Lechte paper table 2
# for electron-neutral impact excitation
radiation_neutral_energy_rate_hydrogen_temperature_eV = np.array([1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0, 50.0, 70.0])
radiation_neutral_energy_rate_hydrogen_Wcm3 = np.array([1.87e-30, 5.14e-29, 2.80e-28, 1.51e-27, 5.81e-27, 1.09e-26, 1.73e-26, 2.56e-26, 3.20e-26, 4.05e-26, 4.90e-26, 5.27e-26])

# source: Lechte paper table 3
# for electron-neutral impact excitation
radiation_neutral_energy_rate_fit_coefficients = {
    "helium": np.array([-53.23545690, 20.38978801, -9.89184875, 3.31535558, -0.94057313, 0.23505604, -0.04449103, 0.00516676, -0.00026644]),
    "argon": np.array([-43.54041883, 12.42131059, -6.00329925, 1.95177862, -0.45911173, 0.07577049, -0.00783356, 0.00037689]),
}

# source: Lechte paper table 4
# for electron-ion impact excitation
radiation_ion_energy_rate_temperatures_eV = {
    "hydrogen": np.array([0]),
    "helium": np.array([0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0, 50.0, 70.0]),
    "argon": np.array([1.00, 1.26, 1.58, 1.99, 2.51, 3.16, 3.98, 5.01, 6.31, 7.94, 9.99, 12.6, 15.8, 19.9, 25.1, 31.6, 39.8, 50.1, 63.0, 79.4])
}
radiation_ion_energy_rate_Wcm3 = {
    "hydrogen": np.array([0]),  # hydrogen is singly charged, thererfore, the ions cannot be excitated
    "helium": np.array([1.00e-74, 1.00e-74, 2.33e-61, 6.68e-51, 2.40e-43, 2.10e-37, 1.41e-34, 1.14e-31, 2.21e-29, 2.08e-28, 1.09e-27, 3.84e-27, 7.11e-27, 1.28e-26, 1.98e-26, 2.34e-26]),
    "argon": np.array([3.72e-31, 4.79e-30, 3.69e-29, 1.92e-28, 7.43e-28, 2.27e-27, 5.68e-27, 1.20e-26, 2.17e-26, 3.47e-26, 4.97e-26, 6.49e-26, 7.88e-26, 8.99e-26, 9.77e-26, 1.02e-25, 1.03e-25, 1.02e-25, 9.82e-26, 9.33e-26])
}

element_name_short = {
    "hydrogen": "H",
    "helium": "He",
    "argon": "Ar"
}

def ionization_rate_coefficient_m3Ds(element, electron_temperature_eV):
    """a.k.a. <σv>_ion"""
    fit_coefficients = ionization_rate_fit_coefficients[element]

    # if np.any(electron_temperature_eV > 40.1):
    #     print(f'Warning: fit coefficients are valid only up to 40 eV, but you specified up to {np.max(electron_temperature_eV)} eV')

    if isinstance(electron_temperature_eV, np.ndarray) and (len(electron_temperature_eV.shape) == 1):
        # this branch is only used for vectors
        exp_parameter = (np.log(electron_temperature_eV)[:, None]**np.arange(len(fit_coefficients))[None, :]) @ fit_coefficients
    else:
        # this branch is used for example if electron_temperature_eV is a single number and not a vector
        exp_parameter = np.zeros_like(electron_temperature_eV)
        for i in range(len(fit_coefficients)):
            exp_parameter += fit_coefficients[i] * np.log(electron_temperature_eV) ** i


    coefficient = np.exp(exp_parameter)

    return coefficient

def test_ionization_rate_coefficient():
    electron_temperature_eV = np.linspace(1, 40, 200)
    plt.figure()
    plt.semilogy(electron_temperature_eV, ionization_rate_coefficient_m3Ds("helium", electron_temperature_eV))
    plt.grid('both')
    plt.xlabel('electron temperature [eV]')
    plt.ylabel('ionization rate coefficient [m³/s]')

def radiation_ion_energy_rate_coefficient_eVm3Ds(element, electron_temperature_eV):
    if element == 'hydrogen':
        return np.zeros_like(electron_temperature_eV)

    # We actually want logarithmic interpolation, not linear one as provided by np.interp.
    # Therefore, we apply the logarithm it and then exponentiate the result again
    coefficient = np.exp(np.interp(electron_temperature_eV, radiation_ion_energy_rate_temperatures_eV[element], np.log(radiation_ion_energy_rate_Wcm3[element]))) * (1e-6 / electron_charge_C)

    # plt.figure()
    # plt.semilogy(electron_temperature_eV, coefficient)
    # plt.grid('both')
    # plt.xlabel('electron temperature [eV]')
    # plt.ylabel('radiation ion energy rate coefficient [eV m³/s] ' + element)
    # plt.xlim(0, 40)
    # plt.ylim(1e-30, 1e-10)

    return coefficient

def radiation_neutral_energy_rate_coefficient_eVm3Ds(element, electron_temperature_eV):
    if element in radiation_neutral_energy_rate_fit_coefficients:
        fit_coefficients = radiation_neutral_energy_rate_fit_coefficients[element]

        # if np.any(electron_temperature_eV > 40.1):
        #     print(f'Warning: fit coefficients are valid only up to 40 eV, but you specified up to {np.max(electron_temperature_eV)} eV')

        if isinstance(electron_temperature_eV, np.ndarray) and (len(electron_temperature_eV.shape) == 1):
            # this branch is only used for vectors
            exp_parameter = (np.log(electron_temperature_eV)[:, None]**np.arange(len(fit_coefficients))[None, :]) @ fit_coefficients
        else:
            # this branch is used for example if electron_temperature_eV is a single number and not a vector
            exp_parameter = np.zeros_like(electron_temperature_eV)
            for i in range(len(fit_coefficients)):
                exp_parameter += fit_coefficients[i] * np.log(electron_temperature_eV) ** i

        coefficient = np.exp(exp_parameter) * average_radiation_neutral_energies_eV[element]
    else:
        # We actually want logarithmic interpolation, not linear one as provided by np.interp.
        # Therefore, we apply the logarithm it and then exponentiate the result again
        coefficient = np.exp(np.interp(electron_temperature_eV, radiation_neutral_energy_rate_hydrogen_temperature_eV, np.log(radiation_neutral_energy_rate_hydrogen_Wcm3))) * (1e-6 / electron_charge_C)

    # plt.figure()
    # plt.semilogy(electron_temperature_eV, coefficient)
    # plt.grid('both')
    # plt.xlabel('electron temperature [eV]')
    # plt.ylabel('radiation neutral energy rate coefficient [eV m³/s] ' + element)
    # plt.xlim(0, 40)
    # plt.ylim(1e-17, 1e-12)

    return coefficient

def calc_recominbation_rate_coefficient_m3Ds(electron_temperature_eV):
    Z = 13.6 / electron_temperature_eV
    return 1.27e-19 * Z**1.5 / (Z + 0.59)

def test_calc_recominbation_rate_coefficient_m3Ds():
    electron_temperature_eV = np.linspace(1, 40)
    recominbation_rate_coefficient_m3Ds = calc_recominbation_rate_coefficient_m3Ds(electron_temperature_eV)
    plt.figure()
    plt.semilogy(electron_temperature_eV, recominbation_rate_coefficient_m3Ds)
    plt.xlim(0, 40)
    plt.ylim(1e-20, 1e-18)
    plt.grid('both')
    plt.xlabel('electron temperature [eV]')
    plt.ylabel('recombination rate coefficient [m³/s]')