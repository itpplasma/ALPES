import math
import sys


from variables import * 

#basic calculations, don't need any precalculations
def get_max_current_per_winding():
    '''Ampere'''
    return max_current_per_mm_2/(math.pi*winding_radius**2)

def get_length_of_winding():
    return 2*math.pi*major_winding_radius

def get_length_of_coil():
    return number_of_windings_x*number_of_windings_y*2*math.pi*major_winding_radius

def get_number_of_coils():
    '''gives number of coils'''
    return number_of_circuits*number_of_coils_per_circuit

def get_circumference_within():
    '''gives the radius within, based on outer dimensions in mm'''
    radius = major_radius_plasma-minor_radius_plasma-2*number_of_windings_y*winding_radius
    return 2*math.pi*radius

def get_current_within():
    '''gives the current on the inside of the plasma loop in kA, with Formula mu_0 I = int B * dl'''
    return B_middle*major_radius_plasma*2*math.pi/mu_0

def get_aspect_ratio():
    '''dimensionless, R_0/a, integrated controll, should be 6 ~ 10'''
    if (major_radius_plasma/minor_radius_plasma > max_aspect_ratio or major_radius_plasma/minor_radius_plasma < min_aspect_ratio):
        print(f'ERROR: aspect ratio out of boundary; aspect ratio = ', major_radius_plasma/minor_radius_plasma)
        sys.exit()
    return major_radius_plasma/minor_radius_plasma

def get_radius_within():
    '''the available space on the inside of the torus'''
    return 2*math.pi*(major_radius_plasma - minor_radius_plasma - cooling_radius*2*number_of_windings_y)

def get_total_coil_volume_within():
    '''gives'''
    return number_of_windings_y*number_of_windings_x*2*cooling_radius



#from here, precalculations are needed, direct use of functions before to prevent errors, checkpoint !!!not implemented yet!!!

def get_length_of_circuit():
    return number_of_windings_x*number_of_windings_y*2*math.pi*major_winding_radius*get_number_of_coils()

def get_volume_of_coils_within():
    '''gives the volume of the inner circuit in mm²'''
    return get_number_of_coils()*number_of_windings_x*number_of_windings_y*(coil_width + cooling_coil_width)

def get_total_coil_radius_within():
    '''gives the radius of the inner circuit in mm, integrated controll with the dimensions'''
    total_circumference = get_number_of_coils()*number_of_windings_x*cooling_radius
    if (total_circumference > get_radius_within()):
        print(f'ERROR: circumference of inner circuit exceeds dimensions; max circumference = ', get_radius_within(), ', actual circumference = ', total_circumference)
        sys.exit()
    return total_circumference

def get_current_per_coil():
    '''kA'''
    return get_current_within()/number_of_coils

def get_current_per_winding():
    '''kA, integrated controll, does not exceed max_current'''
    c_p_w = get_current_within()/(number_of_coils*number_of_windings_x*number_of_windings_y)
    if (c_p_w > max_current_per_winding):
        print(f'ERROR: too much current per winding; maximal current = ', max_current_per_winding, 'actual current = ', c_p_w)
        sys.exit()
    return c_p_w

def get_resistance_per_circuit():
    '''ohm, calculated as rho*l/A'''
    return specific_restistance*length_of_circuit/(math.pi*winding_radius**2)



