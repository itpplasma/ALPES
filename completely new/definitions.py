import math
import sys

class StelleratorDesign:
    '''a wonderfull class to descibe the whole system'''
    def __init__(self, B_middle=None, mu_0=None, max_radius=None, max_height=None,
                 max_aspect_ratio=None, min_aspect_ratio=None, major_radius_plasma=None,
                 minor_radius_plasma=None, number_of_coils_per_circuit=None,
                 number_of_circuits=None, number_of_windings_x=None, number_of_windings_y=None,
                 max_current_per_m_2=None, specific_resistance=None, major_winding_radius=None,
                 winding_radius=None, cooling_radius=None):
        
        # B-field specifications
        self.B_middle = B_middle if B_middle is not None else float(87.3/1000) # T
        self.mu_0 = mu_0 if mu_0 is not None else float(1.25663706212*10**(-6)) # magnetic permeability, N/A²
        
        # Dimension restrictions
        self.max_radius = max_radius if max_radius is not None else float(0.8) # meter
        self.max_height = max_height if max_height is not None else float(0.8) # meter
        self.max_aspect_ratio = max_aspect_ratio if max_aspect_ratio is not None else float(10.) # no dimension
        self.min_aspect_ratio = min_aspect_ratio if min_aspect_ratio is not None else float(6.) # no dimension
        self.major_radius_plasma = major_radius_plasma if major_radius_plasma is not None else float(0.5) # meter
        self.minor_radius_plasma = minor_radius_plasma if minor_radius_plasma is not None else float(0.08) # meter
        
        # Coil assumptions
        self.number_of_coils_per_circuit = number_of_coils_per_circuit if number_of_coils_per_circuit is not None else int(10)
        self.number_of_circuits = number_of_circuits if number_of_circuits is not None else int(4)
        self.number_of_windings_x = number_of_windings_x if number_of_windings_x is not None else int(3)
        self.number_of_windings_y = number_of_windings_y if number_of_windings_y is not None else int(4)
        self.max_current_per_m_2 = max_current_per_m_2 if max_current_per_m_2 is not None else float(50000000.) # A/m² 
        self.specific_resistance = specific_resistance if specific_resistance is not None else float(0.)
        self.major_winding_radius = major_winding_radius if major_winding_radius is not None else float(0.16) # m
        self.winding_radius = winding_radius if winding_radius is not None else float(0.015) # m
        self.cooling_radius = cooling_radius if cooling_radius is not None else float(0.02) # cooling coil + winding coil
        
        # Calculated from basis variables
        self.max_current_per_winding = float(0.) # A
        self.length_of_winding = float(0.) # m
        self.length_of_coil = float(0.) # m
        self.length_of_circuit = float(0.) # m
        self.current_within = float(0.) # kA, within labels the stuff which is at positions < major radius
        self.radius_within = float(0.) # mm available space within torus
        self.total_circumference_of_coils_within = float(0.) # mm
        self.total_coil_volume_within = float(0.) # mm²
        self.number_of_coils = int(0) 
        
        # Calculated from precalculations
        self.current_per_coil = float(0.) # kA
        self.current_per_winding = float(0.) # kA
        self.volume_within = float(0.) # mm²
        self.aspect_ratio = float(0.) # no dimension
        self.resistance_per_circuit = float(0.) # ohm
        self.voltage_per_circuit = float(0.) # Volt

    ###########################################################################################
    
    #getters

    ###########################################################################################

    #basic calculations, don't need any precalculations
    def get_max_current_per_winding(self):
        '''Ampere'''
        return self.max_current_per_m_2 / (math.pi * self.winding_radius**2)

    def get_length_of_winding(self):
        return 2 * math.pi * self.major_winding_radius

    def get_length_of_coil(self):
        return self.number_of_windings_x * self.number_of_windings_y * 2 * math.pi * self.major_winding_radius

    def get_number_of_coils(self):
        '''gives number of coils'''
        return self.number_of_circuits * self.number_of_coils_per_circuit

    def get_circumference_within(self):
        '''gives the radius within, based on outer dimensions in mm'''
        radius = self.major_radius_plasma - self.minor_radius_plasma - 2 * self.number_of_windings_y * self.winding_radius
        return 2 * math.pi * radius

    def get_current_within(self):
        '''gives the current on the inside of the plasma loop in kA, with Formula mu_0 I = int B * dl'''
        return self.B_middle * self.major_radius_plasma * 2 * math.pi / self.mu_0

    def get_aspect_ratio(self):
        '''dimensionless, R_0/a, integrated control, should be 6 ~ 10'''
        if (self.major_radius_plasma / self.minor_radius_plasma > self.max_aspect_ratio or
            self.major_radius_plasma / self.minor_radius_plasma < self.min_aspect_ratio):
            print(f'ERROR: aspect ratio out of boundary; aspect ratio = ', self.major_radius_plasma / self.minor_radius_plasma)
            #sys.exit()
        return self.major_radius_plasma / self.minor_radius_plasma

    def get_radius_within(self):
        '''the available space on the inside of the torus'''
        return 2 * math.pi * (self.major_radius_plasma - self.minor_radius_plasma - self.cooling_radius * 2 * self.number_of_windings_y)

    def get_total_coil_volume_within(self):
        '''gives'''
        return self.number_of_windings_y * self.number_of_windings_x * 2 * self.cooling_radius

    def get_length_of_circuit(self):
        return self.number_of_windings_x * self.number_of_windings_y * 2 * math.pi * self.major_winding_radius * self.get_number_of_coils()

    def get_volume_of_coils_within(self):
        '''gives the volume of the inner circuit in mm²'''
        return self.get_number_of_coils() * self.number_of_windings_x * self.number_of_windings_y * 2* self.cooling_radius

    def get_total_coil_radius_within(self):
        '''gives the radius of the inner circuit in mm, integrated control with the dimensions'''
        total_circumference = self.get_number_of_coils() * self.number_of_windings_x * self.cooling_radius
        if (total_circumference > self.get_radius_within()):
            print(f'ERROR: circumference of inner circuit exceeds dimensions; max circumference = ', self.get_radius_within(), ', actual circumference = ', total_circumference)
            #sys.exit()
        return total_circumference

    def get_current_per_coil(self):
        '''kA'''
        return self.get_current_within() / self.get_number_of_coils()

    def get_current_per_winding(self):
        '''kA, integrated control, does not exceed max_current'''
        c_p_w = self.get_current_within() / (self.get_number_of_coils() * self.number_of_windings_x * self.number_of_windings_y)
        if (c_p_w > self.max_current_per_winding):
            print(f'ERROR: too much current per winding; maximal current = ', self.max_current_per_winding, 'actual current = ', c_p_w)
            sys.exit()
        return c_p_w

    def get_resistance_per_circuit(self):
        '''ohm, calculated as rho*l/A'''
        return self.specific_resistance * self.length_of_circuit / (math.pi * self.winding_radius**2)

    ##############################################################################################

    #setters

    ##############################################################################################
    
    def set_B_middle(self, value):
        self.B_middle = value

    def set_mu_0(self, value):
        self.mu_0 = value

    def set_max_radius(self, value):
        self.max_radius = value

    def set_max_height(self, value):
        self.max_height = value

    def set_max_aspect_ratio(self, value):
        self.max_aspect_ratio = value

    def set_min_aspect_ratio(self, value):
        self.min_aspect_ratio = value

    def set_major_radius_plasma(self, value):
        self.major_radius_plasma = value

    def set_minor_radius_plasma(self, value):
        self.minor_radius_plasma = value

    def set_number_of_coils_per_circuit(self, value):
        self.number_of_coils_per_circuit = value

    def set_number_of_circuits(self, value):
        self.number_of_circuits = value

    def set_number_of_windings_x(self, value):
        self.number_of_windings_x = value

    def set_number_of_windings_y(self, value):
        self.number_of_windings_y = value

    def set_max_current_per_m_2(self, value):
        self.max_current_per_m_2 = value

    def set_specific_resistance(self, value):
        self.specific_resistance = value

    def set_major_winding_radius(self, value):
        self.major_winding_radius = value

    def set_winding_radius(self, value):
        self.winding_radius = value

    def set_cooling_radius(self, value):
        self.cooling_radius = value

    def set_max_current_per_winding(self, value):
        self.max_current_per_winding = value

    def set_length_of_winding(self, value):
        self.length_of_winding = value

    def set_length_of_coil(self, value):
        self.length_of_coil = value

    def set_length_of_circuit(self, value):
        self.length_of_circuit = value

    def set_current_within(self, value):
        self.current_within = value

    def set_radius_within(self, value):
        self.radius_within = value

    def set_total_circumference_of_coils_within(self, value):
        self.total_circumference_of_coils_within = value

    def set_total_coil_volume_within(self, value):
        self.total_coil_volume_within = value

    def set_number_of_coils(self, value):
        self.number_of_coils = value

    def set_current_per_coil(self, value):
        self.current_per_coil = value

    def set_current_per_winding(self, value):
        self.current_per_winding = value

    def set_volume_within(self, value):
        self.volume_within = value

    def set_aspect_ratio(self, value):
        self.aspect_ratio = value

    def set_resistance_per_circuit(self, value):
        self.resistance_per_circuit = value

    def set_voltage_per_circuit(self, value):
        self.voltage_per_circuit = value

    ##############################################################################################

    #other random but important functions

    ##############################################################################################

    def print_parameters(self):
        params = vars(self)
        for key, value in self.__dict__.items():
            if not key.startswith("__"):
                print(f"{key} = {value}")

    