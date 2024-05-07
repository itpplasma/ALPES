import math
import sys

from definitions import *

def calculations(stellarator):
    stellarator.max_current_per_winding = stellarator.get_max_current_per_winding()
    stellarator.length_of_winding = stellarator.get_length_of_winding()
    stellarator.length_of_coil = stellarator.get_length_of_coil()
    stellarator.number_of_coils = stellarator.get_number_of_coils()
    stellarator.circumference_within = stellarator.get_circumference_within()
    stellarator.current_within = stellarator.get_current_within()
    stellarator.aspect_ratio = stellarator.get_aspect_ratio()
    stellarator.radius_within = stellarator.get_radius_within()
    stellarator.total_coil_volume_within = stellarator.get_total_coil_volume_within()
    stellarator.length_of_circuit = stellarator.get_length_of_circuit()
    stellarator.volume_of_coils_within = stellarator.get_volume_of_coils_within()
    stellarator.total_coil_radius_within = stellarator.get_total_coil_radius_within()
    stellarator.current_per_coil = stellarator.get_current_per_coil()
    stellarator.current_per_winding = stellarator.get_current_per_winding()
    stellarator.resistance_per_circuit = stellarator.get_resistance_per_circuit()



def main():
    stellerator = StelleratorDesign(B_middle=None, mu_0=None, max_radius=None, max_height=None,
                 max_aspect_ratio=None, min_aspect_ratio=None, major_radius_plasma=None,
                 minor_radius_plasma=None, number_of_coils_per_circuit=None,
                 number_of_circuits=None, number_of_windings_x=None, number_of_windings_y=None,
                 max_current_per_m_2=None, specific_resistance=None, major_winding_radius=None,
                 winding_radius=None, cooling_radius=None)
    stellerator.print_parameters()
    calculations(stellerator)
    stellerator.print_parameters()

main()