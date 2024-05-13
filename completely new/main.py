import math
import sys

from definitions import *

def calculations(stellarator):
    stellarator.B_toroidal = stellarator.get_B_toroidal()
    stellarator.max_I_winding = stellarator.get_max_I_winding()
    stellarator.len_coil = stellarator.get_len_coil()
    stellarator.number_of_coils = stellarator.get_number_of_coils()
    stellarator.circumference_within = stellarator.get_circumference_within()
    stellarator.I_linking = stellarator.get_I_linking()
    stellarator.aspect_ratio = stellarator.get_aspect_ratio()
    stellarator.radius_within = stellarator.get_radius_within()
    stellarator.total_coil_volume_within = stellarator.get_total_coil_volume_within()
    stellarator.length_of_circuit = stellarator.get_length_of_circuit()
    stellarator.volume_of_coils_within = stellarator.get_volume_of_coils_within()
    stellarator.total_coil_radius_within = stellarator.get_total_coil_radius_within()
    stellarator.I_coil = stellarator.get_I_coil()
    stellarator.I_winding = stellarator.get_I_winding()
    stellarator.resistance_per_circuit = stellarator.get_resistance_per_circuit()

def controll():
    return True

def main():
    stellarator = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                 max_aspect_ratio=None, min_aspect_ratio=None, radius_major=None,
                 radius_minor=None, number_of_coils_per_circuit=None,
                 number_of_circuits=None, number_of_windings_x=None, number_of_windings_y=None,
                 max_current_per_m_2=None, specific_resistance=None, major_winding_radius=None,
                 winding_radius=None, cooling_radius=None)
    calculations(stellarator)
    stellarator.get_number_of_coils()
    stellarator.print_parameters()

main()