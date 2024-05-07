from variables import * 
from functions import *


def set_max_current_per_winding():
    global max_current_per_winding
    max_current_per_winding = get_max_current_per_winding()
    print("Max current per winding:", max_current_per_winding)

def set_length_of_winding():
    global length_of_winding
    length_of_winding = get_length_of_winding()

def set_length_of_coil():
    global length_of_coil
    length_of_coil = get_length_of_coil()

def set_length_of_circuit():
    global length_of_circuit
    length_of_circuit = get_length_of_circuit()

def set_current_within():
    global current_within
    current_within = get_current_within() #kA, within labels the stuff which is at positions < major radius

def set_radius_within():    
    global radius_within
    radius_within = get_radius_within() #m

def set_total_coil_radius_within():
    global total_coil_radius_within
    total_coil_radius_within = get_total_coil_radius_within() #m

def set_total_coil_volume_within():
    global total_coil_volume_within
    total_coil_volume_within = get_total_coil_volume_within() #m²

def set_number_of_coils():
    global number_of_coils
    number_of_coils = get_number_of_coils()