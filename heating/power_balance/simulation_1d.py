import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import utils
import simulation_common

def fully_explicit(initial_electron_density_Dm3, initial_electron_temperature_eV, time_step_s, radial_step_m, num_radial_steps, num_time_steps, particle_diffusivity_m2Ds, heat_diffusivity_m2Ds, neutral_density_Dm3, ionization_rate_coefficient_m3Ds, recominbation_rate_coefficient_m3Ds, heating_power_eVDsm3, ionization_energy_eV, radiation_neutral_energy_rate_coefficient_eVm3Ds):
    """
    Same model as in Birkenmaier 2008: "Experiments and Modeling of Transport Processes in Toroidal Plasmas"
    But fully-explicit scheme instead of Crank Nichelson.

    For r = 0: Neumann boundary condition (delta n = delta T = 0)
    For r = r_max: Dirichlet boundary condition (n = n0, T = T0)

    Parameters:
    particle_diffusivity_m2Ds: a.k.a. D
    heat_diffusivity_m2Ds: a.k.a. χ
    """
    electron_density_stepped_Dm3 = np.empty((num_time_steps, num_radial_steps), dtype=np.float64)
    electron_temperature_stepped_eV = np.empty((num_time_steps, num_radial_steps), dtype=np.float64)
    electron_density_stepped_Dm3[0] = initial_electron_density_Dm3
    electron_temperature_stepped_eV[0] = initial_electron_temperature_eV

    radiuses_m = np.arange(num_radial_steps) * radial_step_m
    radiuses_m[0] = radiuses_m[1] * 0.5  # to avoid singularity when dividing by radiuses_m[0]
    for i_step in range(1, num_time_steps):
        old_electron_density_Dm3 = np.concatenate((np.array([electron_density_stepped_Dm3[i_step - 1, 0]]), electron_density_stepped_Dm3[i_step - 1], np.array([initial_electron_density_Dm3])))
        old_electron_temperature_eV = np.concatenate((np.array([electron_temperature_stepped_eV[i_step - 1, 0]]), electron_temperature_stepped_eV[i_step - 1], np.array([initial_electron_temperature_eV])))

        if i_step % 100000 == 0:
            print('step', i_step, time_step_s * np.sum(neutral_density_Dm3 * old_electron_density_Dm3[1:-1] * ionization_rate_coefficient_m3Ds(old_electron_temperature_eV[1:-1])) / num_radial_steps, time_step_s * np.sum(old_electron_density_Dm3[1:-1]**2 * recominbation_rate_coefficient_m3Ds(old_electron_temperature_eV[1:-1])) / num_radial_steps)

        delta_electron_density_Dm3 = time_step_s * (
            particle_diffusivity_m2Ds / radial_step_m**2 * (
                old_electron_density_Dm3[2:] - 2 * old_electron_density_Dm3[1:-1] + old_electron_density_Dm3[:-2])
            + particle_diffusivity_m2Ds / (2 * radial_step_m) / radiuses_m * (
                old_electron_density_Dm3[2:] - old_electron_density_Dm3[:-2])
            + neutral_density_Dm3 * old_electron_density_Dm3[1:-1] * ionization_rate_coefficient_m3Ds(old_electron_temperature_eV[1:-1])
            - old_electron_density_Dm3[1:-1]**2 * recominbation_rate_coefficient_m3Ds(old_electron_temperature_eV[1:-1]))

        delta_electron_temperature_eV = 2/3 * time_step_s * (
            heat_diffusivity_m2Ds / radial_step_m**2 * (
                old_electron_temperature_eV[2:] - 2 * old_electron_temperature_eV[1:-1] + old_electron_temperature_eV[:-2])
            + (3/2 * particle_diffusivity_m2Ds + heat_diffusivity_m2Ds) / (4 * radial_step_m**2) / old_electron_density_Dm3[1:-1] * (
                old_electron_temperature_eV[2:] - old_electron_temperature_eV[:-2]) * (
                old_electron_density_Dm3[2:] - old_electron_density_Dm3[:-2])
            + heat_diffusivity_m2Ds / (2 * radial_step_m) / radiuses_m * (
                old_electron_temperature_eV[2:] - old_electron_temperature_eV[:-2])
            + heating_power_eVDsm3 / old_electron_density_Dm3[1:-1]
            - neutral_density_Dm3 * ionization_rate_coefficient_m3Ds(old_electron_temperature_eV[1:-1]) * (
                ionization_energy_eV + 3/2 * old_electron_temperature_eV[1:-1])
            - neutral_density_Dm3 * radiation_neutral_energy_rate_coefficient_eVm3Ds(old_electron_temperature_eV[1:-1]))

        electron_density_stepped_Dm3[i_step] = electron_density_stepped_Dm3[i_step - 1] + delta_electron_density_Dm3
        electron_temperature_stepped_eV[i_step] = electron_temperature_stepped_eV[i_step - 1] + delta_electron_temperature_eV

    return electron_density_stepped_Dm3, electron_temperature_stepped_eV

def calc_normalized_power_distribution_WDm3(radiuses_m, absolute_power_W, major_radius_m, deposition_radius_m, standard_deviation):
    """implements formula 3.16 from Birkenmaier"""
    exp_term = np.exp(-(radiuses_m - deposition_radius_m)**2 / (2 * standard_deviation**2))
    radial_step_m = radiuses_m[1]
    I = np.sum(exp_term * radiuses_m) * radial_step_m
    return absolute_power_W / (4 * np.pi**2 * major_radius_m * I) * exp_term

def figure_5_3_fully_explicit():
    num_radial_steps = 200
    radiuses_m = np.linspace(0, 0.175, num_radial_steps)  # Birkenmaier p. 19: "The maximum radius in the simulation was assumed to be rves = 0.175 m, corresponding to the vacuum-vessel radius of TJ-K"
    heating_power_WDm3 = calc_normalized_power_distribution_WDm3(
        radiuses_m=radiuses_m,
        absolute_power_W=1.8e3,
        major_radius_m=0.6,  # Birkenmaier p. 24
        deposition_radius_m=0.14,
        standard_deviation=0.007)  # Birkenmaier p. 20 "width of the heating profile"
    heating_power_eVDsm3 = heating_power_WDm3 / simulation_common.electron_charge_C

    neutral_density_Dm3 = 5.1e-3 / (simulation_common.boltzmann_constant_JDK * 290)
    print(f'neutral density = {neutral_density_Dm3} 1/m³')
    time_step_s = 2e-9  # 1e-6

    element = "hydrogen"
    electron_density_stepped_Dm3, electron_temperature_stepped_eV = fully_explicit(
        initial_electron_density_Dm3=0.2e17, # it is very strange but this value corresponds to the initial density in the plots of Birkenmaier #neutral_density_Dm3 * 0.01, #1e14,  # Birkeinmaier p. 19
        initial_electron_temperature_eV=0.025,  # Birkenmaier p. 19 (290 K)
        time_step_s=time_step_s,
        radial_step_m=radiuses_m[1],
        num_radial_steps=num_radial_steps,
        num_time_steps=900001, #2035,
        particle_diffusivity_m2Ds=17,
        heat_diffusivity_m2Ds=170,
        neutral_density_Dm3=neutral_density_Dm3,
        ionization_rate_coefficient_m3Ds=lambda T: simulation_common.ionization_rate_coefficient_m3Ds(element, T),
        recominbation_rate_coefficient_m3Ds=simulation_common.calc_recominbation_rate_coefficient_m3Ds,
        heating_power_eVDsm3=heating_power_eVDsm3,
        ionization_energy_eV=simulation_common.ionization_energies_eV[element],
        radiation_neutral_energy_rate_coefficient_eVm3Ds=lambda T: simulation_common.radiation_neutral_energy_rate_coefficient_eVm3Ds(element, T))

    plotted_steps = [0, 500, 4500, 22500, 202500, 900000]

    fig_density, ax_density = plt.subplots(1)
    step_colormap = lambda i_step: matplotlib.colormaps['cool'](matplotlib.colors.Normalize(vmin=0, vmax=len(plotted_steps))(i_step))
    for i_step, step in enumerate(plotted_steps):
        ax_density.plot(radiuses_m, electron_density_stepped_Dm3[step], label=f'step={step} t={step * time_step_s * 1e6:5.3f} µs', color=step_colormap(i_step))
    ax_density.set_ylabel('density [1/m³]')
    ax_density.set_xlabel('radius [m]')
    ax_density.set_xlim([0, 0.2])
    ax_density.set_ylim([0, 2e17])
    utils.make_clickable_legend('upper right', fig_density, ax_density)
    fig_density.canvas.manager.set_window_title('Figure 5.3 density')

    fig_temperature, ax_temperature = plt.subplots(1)
    for i_step, step in enumerate(plotted_steps):
        ax_temperature.plot(radiuses_m, electron_temperature_stepped_eV[step], label=f'step={step} t={step * time_step_s * 1e6:5.3f} µs', color=step_colormap(i_step))
    ax_temperature.set_ylabel('temperature [eV]')
    ax_temperature.set_xlabel('radius [m]')
    ax_temperature.set_xlim([0, 0.2])
    ax_temperature.set_ylim([0, 20])
    utils.make_clickable_legend('upper left', fig_temperature, ax_temperature)
    fig_temperature.canvas.manager.set_window_title('Figure 5.3 temperature')

if __name__ == "__main__":
    figure_5_3_fully_explicit()
    plt.show()
