import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import utils
import simulation_1d
import simulation_common

def number_for_filename(number, suffix):
    if np.abs(number - np.round(number)) < number * 1e-9:
        return str(int(number)) + suffix
    else:
        return str(number).replace('.', suffix)

def construct_filename(element, power_W, initial_electron_density_Dm3, scaling_033=False):
    filename = f"sim1d_{simulation_common.element_name_short[element]}_{number_for_filename(power_W * 1e-3, 'kW')}_{initial_electron_density_Dm3:e}{'_033' if scaling_033 else ''}.npz"
    return filename

# Source: Birkenmaier p. 35
particle_diffusivity_m2Ds = {'hydrogen': 17, 'helium': 8.5, 'argon': 6}
heat_diffusivity_m2Ds = {'hydrogen': 170, 'helium': 200, 'argon': 18}

def studies_graz_033():
    """
    Runs the 0D simulations with the parameters for the upcoming stellerator design and saves them into compressed numpy files.
    One numpy file per element and heating power is generated.
    """
    initial_electron_density_Dm3 = 1e15

    for element in ["helium", "argon"]:
        if element == 'hydrogen':
            neutral_density_mbar = 5.1e-5
        elif element == 'helium':
            neutral_density_mbar = 9.2e-5
        elif element == 'argon':
            neutral_density_mbar = 0.93e-5
        else:
            raise Exception(f'unknown element {element}')

        neutral_density_Dm3 = neutral_density_mbar * 1e2 / (simulation_common.boltzmann_constant_JDK * 290)
        print(f'neutral density = {neutral_density_Dm3} 1/m³')

        for power_W in [0.5e3, 1e3, 2e3, 3e3]:
            if (element == 'argon') and (power_W >= 2e3):
                # For some configurations, the radial stepsize had to be increased. The reason is
                # probably the very steep temperature gradient at the edge.
                # Otherwise, the edge of the temperature will go slighly up instead of down.
                num_radial_steps = 1000
                radiuses_m = np.linspace(0, 0.0825, num_radial_steps)
                time_step_s = 0.5e-9
                num_time_steps = 1120001
            else:
                num_radial_steps = 500
                radiuses_m = np.linspace(0, 0.0825, num_radial_steps)
                time_step_s = 0.8e-9
                num_time_steps = 700001

            heating_power_WDm3 = simulation_1d.calc_normalized_power_distribution_WDm3(
                radiuses_m=radiuses_m,
                absolute_power_W=power_W,
                major_radius_m=0.33,
                deposition_radius_m=0.066,
                standard_deviation=0.0033)
            heating_power_eVDsm3 = heating_power_WDm3 / simulation_common.electron_charge_C

            description = f'{element} P={power_W * 1e-3}kW initial={initial_electron_density_Dm3:e}/m³'
            print(description)

            electron_density_stepped_Dm3, electron_temperature_stepped_eV = simulation_1d.fully_explicit(
                initial_electron_density_Dm3=initial_electron_density_Dm3,
                initial_electron_temperature_eV=0.025,  # 290 K
                time_step_s=time_step_s,
                radial_step_m=radiuses_m[1],
                num_radial_steps=num_radial_steps,
                num_time_steps=num_time_steps,
                particle_diffusivity_m2Ds=particle_diffusivity_m2Ds[element],
                heat_diffusivity_m2Ds=particle_diffusivity_m2Ds[element],
                neutral_density_Dm3=neutral_density_Dm3,
                ionization_rate_coefficient_m3Ds=lambda T: simulation_common.ionization_rate_coefficient_m3Ds(element, T),
                recominbation_rate_coefficient_m3Ds=simulation_common.calc_recominbation_rate_coefficient_m3Ds,
                heating_power_eVDsm3=heating_power_eVDsm3,
                ionization_energy_eV=simulation_common.ionization_energies_eV[element],
                radiation_neutral_energy_rate_coefficient_eVm3Ds=lambda T: simulation_common.radiation_neutral_energy_rate_coefficient_eVm3Ds(element, T))

            plotted_steps = [0, 500, 4500, 22500, 202500, 500000, 700000]

            filename = construct_filename(element, power_W, initial_electron_density_Dm3, True)
            print(f"saving to {filename}")
            np.savez(filename, electron_density_stepped_Dm3=electron_density_stepped_Dm3[::500], electron_temperature_stepped_eV=electron_temperature_stepped_eV[::500])

            fig_density, ax_density = plt.subplots(1)
            step_colormap = lambda i_step: matplotlib.colormaps['cool'](matplotlib.colors.Normalize(vmin=0, vmax=len(plotted_steps))(i_step))
            for i_step, step in enumerate(plotted_steps):
                ax_density.plot(radiuses_m, electron_density_stepped_Dm3[step], label=f'step={step} t={step * time_step_s * 1e6:5.3f} µs', color=step_colormap(i_step))
            ax_density.set_ylabel('density [1/m³]')
            ax_density.set_xlabel('radius [m]')
            ax_density.set_xlim([0, 0.12])
            ax_density.set_ylim([0, 1.2e18])
            utils.make_clickable_legend('upper right', fig_density, ax_density)
            fig_density.canvas.manager.set_window_title(f'density {description}')

            fig_temperature, ax_temperature = plt.subplots(1)
            for i_step, step in enumerate(plotted_steps):
                ax_temperature.plot(radiuses_m, electron_temperature_stepped_eV[step], label=f'step={step} t={step * time_step_s * 1e6:5.3f} µs', color=step_colormap(i_step))
            ax_temperature.set_ylabel('temperature [eV]')
            ax_temperature.set_xlabel('radius [m]')
            ax_temperature.set_xlim([0, 0.12])
            ax_temperature.set_ylim([0, 40])
            utils.make_clickable_legend('upper left', fig_temperature, ax_temperature)
            fig_temperature.canvas.manager.set_window_title(f'temperature {description}')

            # free up memory
            electron_density_stepped_Dm3 = None
            electron_temperature_stepped_eV = None

def r_033():
    """
    Reads in a compressed numpy file written by studies_graz_033 and visualizes it.
    This function must be changed depending on what case you want to visualize.
    It will take up to around 20GB of RAM (the npz files will be small, though, because only a subset of steps is saved)
    """
    element = "argon"
    num_radial_steps = 1000
    radiuses_m = np.linspace(0, 0.1, num_radial_steps)
    power_W = 3e3
    initial_electron_density_Dm3 = 1e15
    time_step_s = 0.5e-9
    plotted_steps = [0, 500, 4500, 22500, 202500, 500000, 700000, 900000]

    filename = construct_filename(element, power_W, initial_electron_density_Dm3, True)
    file = np.load(filename)
    electron_density_stepped_Dm3 = file['electron_density_stepped_Dm3']
    electron_temperature_stepped_eV = file['electron_temperature_stepped_eV']

    fig_density, ax_density = plt.subplots(1)
    step_colormap = lambda i_step: matplotlib.colormaps['cool'](matplotlib.colors.Normalize(vmin=0, vmax=len(plotted_steps))(i_step))
    for i_step, step in enumerate(plotted_steps):
        ax_density.plot(radiuses_m, electron_density_stepped_Dm3[step // 500], label=f'step={step} t={step * time_step_s * 1e6:5.3f} µs', color=step_colormap(i_step))
    ax_density.set_ylabel('density [1/m³]')
    ax_density.set_xlabel('radius [m]')
    ax_density.set_xlim([0, 0.12])
    ax_density.set_ylim([0, 1.2e18])
    utils.make_clickable_legend('upper right', fig_density, ax_density)
    fig_density.canvas.manager.set_window_title(f'density {element} P={power_W * 1e3}kW initial={initial_electron_density_Dm3:e}/m³')

    fig_temperature, ax_temperature = plt.subplots(1)
    for i_step, step in enumerate(plotted_steps):
        ax_temperature.plot(radiuses_m, electron_temperature_stepped_eV[step // 500], label=f'step={step} t={step * time_step_s * 1e6:5.3f} µs', color=step_colormap(i_step))
    ax_temperature.set_ylabel('temperature [eV]')
    ax_temperature.set_xlabel('radius [m]')
    ax_temperature.set_xlim([0, 0.12])
    ax_temperature.set_ylim([0, 50])
    utils.make_clickable_legend('upper left', fig_temperature, ax_temperature)
    fig_temperature.canvas.manager.set_window_title(f'temperature {element} P={power_W * 1e3}kW initial={initial_electron_density_Dm3:e}/m³')

def visualize_033():
    initial_electron_density_Dm3 = 1e15

    neutral_density_Dm3 = 4e-3 / (simulation_common.boltzmann_constant_JDK * 290)  # 4e-5 mbar = 1e18/m3
    print(f'neutral density = {neutral_density_Dm3} 1/m³')

    for element in ["helium", "argon"]:
        # fig_density, ax_density = plt.subplots(1)
        # fig_temperature, ax_temperature = plt.subplots(1)
        fig, axs = plt.subplots(ncols=2, figsize=(12, 5))
        ax_temperature = axs[0]
        ax_density = axs[1]

        for power_W in [0.5e3, 1e3, 2e3, 3e3]:
            if (element == "argon") and power_W in [2e3, 3e3]:
                num_radial_steps = 1000
            else:
                num_radial_steps = 500
            radiuses_m = np.linspace(0, 0.0825, num_radial_steps)

            description = f'{element} P={power_W * 1e-3}kW initial={initial_electron_density_Dm3:e}/m³'
            print(description)

            filename = construct_filename(element, power_W, initial_electron_density_Dm3, True)
            file = np.load(filename)
            electron_density_stepped_Dm3 = file['electron_density_stepped_Dm3']
            electron_temperature_stepped_eV = file['electron_temperature_stepped_eV']

            ax_density.plot(radiuses_m, electron_density_stepped_Dm3[-1], label=f'P={power_W * 1e-3} kW')
            ax_temperature.plot(radiuses_m, electron_temperature_stepped_eV[-1], label=f'P={power_W * 1e-3} kW')

        ax_density.set_ylabel('electron density (= ion density) [1/m³]')
        ax_density.set_xlabel('minor radius [m]')
        ax_density.set_xlim([0, 0.1])
        ax_density.set_ylim([0, 1.3e18])
        utils.make_clickable_legend('upper right', fig, ax_density)
        ax_density.set_title(f'density {element}')
        #fig_density.canvas.manager.set_window_title(f'density {element}')

        ax_temperature.set_ylabel('electron temperature [eV]')
        ax_temperature.set_xlabel('minor radius [m]')
        ax_temperature.set_xlim([0, 0.1])
        ax_temperature.set_ylim([0, 50])
        utils.make_clickable_legend('upper left', fig, ax_temperature)
        ax_temperature.set_title(f'temperature {element}')
        #fig_temperature.canvas.manager.set_window_title(f'temperature {element}')

        fig.tight_layout()

if __name__ == "__main__":
    studies_graz_033()
    #r_033()
    visualize_033()
    plt.show()