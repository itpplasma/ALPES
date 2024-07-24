import math
import sys
import pressure_loss_calculator.PressureLossMod as PL
from geometric_object import *

def isNr(val):
	if isinstance(val, int) or isinstance(val, float):
		return True
	return False


def notNr(val):
	if isinstance(val, int) or isinstance(val, float):
		return False
	return True



class StellaratorDesign:
    '''a wonderfull class to descibe the whole system'''
    def __init__(self, material, diam_max=None, max_height=None,
                 max_aspect_ratio=None, min_aspect_ratio=None, radius_major=None,
                 radius_minor=None, frequency_rotation=None,
                  number_of_coils_per_circuit=None,
                 number_of_circuits=None, number_of_windings_x=None, number_of_windings_y=None,
                 max_current_per_m_2=None, specific_resistance=None,
                 winding_radius=None, inner_radius=None, isolation_width=None, geometry = None):
        
        #constants
        self.mu_0 = float(1.25663706212e-6) # magnetic permeability, N/A²
        self.electron_mass = float(9.1093837015e-31) #kg
        self.electron_charge = float(1.602176634e-19) #C
        
        # Dimension restrictions
        self.diam_max = diam_max if diam_max is not None else float(1.6) # meter
        self.max_height = max_height if max_height is not None else float(0.7) # meter
        self.max_aspect_ratio = max_aspect_ratio if max_aspect_ratio is not None else float(14.) # no dimension
        self.min_aspect_ratio = min_aspect_ratio if min_aspect_ratio is not None else float(1.) # no dimension
        self.radius_major = radius_major if radius_major is not None else float(0.38) # meter
        self.radius_minor = radius_minor if radius_minor is not None else float(0.29) # meter
        
        #dimensions parameters
        self.len_of_winding = float(0.) #m
        self.len_coil = float(0.) # m
        self.length_of_circuit = float(0.) # m
        self.total_circumference_of_coils_within = float(0.) # m
        self.number_of_coils = int(0) 
        self.volume_within = float(0.) # m^2
        self.aspect_ratio = float(0.) # no dimension

        # fields and stuff
        self.frequency_rotation = frequency_rotation if frequency_rotation is not None else float(2.45e9)#Hz
        self.number_of_coils_per_circuit = number_of_coils_per_circuit if number_of_coils_per_circuit is not None else int(4)
        self.number_of_circuits = number_of_circuits if number_of_circuits is not None else int(3)
        self.max_current_per_m_2 = max_current_per_m_2 if max_current_per_m_2 is not None else float(500000.) # A/m² 
        self.specific_resistance = specific_resistance if specific_resistance is not None else float(0.)
        #self.winding_radius = winding_radius if winding_radius is not None else float(0.0075) # m
        #self.inner_radius = inner_radius if inner_radius is not None else float(0.005) # cooling coil + winding coil
        
        # fields and stuff to calculate
        self.B_toroidal = float(0.) #Tesla #B_toroidal if B_toroidal is not None else float(87.3/1000) # T
        self.max_I_winding = float(0.) # A
        self.I_linking = float(0.) # kA, within labels the stuff which is at positions < major radius
        self.I_coil = float(0.) # kA
        self.I_winding = float(0.) # kA
        self.resistance_per_circuit = float(0.) # ohm
        self.resistance_per_winding = float(0.) # ohm
        self.voltage_per_circuit = float(0.) # Volt
        self.voltage_per_winding = float(0.) # Volt
        self.power_per_winding = float(0.)
        self.power_per_circuit = float(0.)

        #geometry of the windings stuff
        isolation_width = isolation_width if isolation_width is not None else float(0.00025)
        number_of_windings_x = number_of_windings_x if number_of_windings_x is not None else int(6)
        number_of_windings_y = number_of_windings_y if number_of_windings_y is not None else int(6)
        winding_radius = winding_radius if winding_radius is not None else float(0.005)
        inner_radius = inner_radius if inner_radius is not None else float(0.004)
        self.geometry = rund("rund", winding_radius, inner_radius, number_of_windings_x, number_of_windings_y, isolation_width)
        #self.geometry = rechteckig("rechteckig", self.winding_radius, self.winding_radius, self.inner_radius, self.inner_radius, number_of_windings_x, num_of_windings_y, 0.002)

        #cooling stuff
        self.massflow = float(0.)
        self.d_pressure = float(0.)

        #expenses stuff
        self.cond_volume = float(0.)

        self.material = material
        if self.material == 'copper':
            self.specific_resistance = 1.68e-8#Ohm*m @ 77°C
            self.material_price = float(0.5) #Euro/m³
		    # heat capacity =
		    # heat conduction =
        elif self.material == "aluminum" or "aluminium":
            self.specific_resistance = 3.875e-8
            self.material_price = float(0.5) 
		    #self.specific_resistance = 3.875*10**(-8)#Ohm*m @ 77°C (source: https://hypertextbook.com/facts/2004/ValPolyakov.shtml)
		    # heat capacity = 
		    # heat conduction = 
        if self.specific_resistance == None:
            raise Exception('Missing conductor material properties')
        
        super().__setattr__('_number_of_windings_x', number_of_windings_x)
        super().__setattr__('_number_of_windings_y', number_of_windings_y)
        super().__setattr__('_winding_radius', winding_radius)
        super().__setattr__('_inner_radius', inner_radius)

    def __setattr__(self, name, value):
        if name == 'number_of_windings_x':
            self.geometry.number_of_windings_x = value
        elif name == 'outer_radius':
            self.geometry.winding_radius = value
        elif name == 'number_of_windings_y':
            self.geometry.number_of_windings_y = value
        elif name == 'inner_radius':
            self.geometry.inner_radius = value
        #elif name == 'outer_radius':
        #    self.geometry.winding_radius = value
        #elif name == 'inner_radius':
        #    self.geometry.inner_radius = value
        else:
            super().__setattr__(name, value)
    ###########################################################################################
    
    #getters

    ###########################################################################################

    #dimension calculations
    
    def get_len_of_winding(self):
        return 2 * math.pi * self.radius_minor

    def get_len_coil(self):
        return self.geometry.number_of_windings_total * 2 * math.pi * self.radius_minor

    def get_number_of_coils(self):
        '''gives number of coils'''
        return self.number_of_circuits * self.number_of_coils_per_circuit

    def get_circumference_within(self):
        '''gives the radius within, based on outer dimensions in mm'''
        radius = self.radius_major - self.radius_minor - self.geometry.len_x
        return 2 * math.pi * radius

    def get_aspect_ratio(self):
        '''dimensionless, R_0/a, integrated control, should be 6 ~ 10'''
        if (self.radius_major / self.radius_minor > self.max_aspect_ratio or
            self.radius_major / self.radius_minor < self.min_aspect_ratio):
            print(f'ERROR: aspect ratio out of boundary; aspect ratio = ', self.radius_major / self.radius_minor)
            sys.exit()
        return self.radius_major / self.radius_minor

    def get_length_of_circuit(self):
        return self.geometry.number_of_windings_x * self.geometry.number_of_windings_y * 2 * math.pi * self.radius_minor * self.number_of_coils_per_circuit

    def get_volume_of_coils_within(self):
        '''gives the volume of the inner circuit in m²'''
        return self.get_number_of_coils() * self.geometry.total_area

    #current and fields
    def get_B_toroidal(self):
        "Tesla"
        return self.electron_mass*self.frequency_rotation*2*math.pi/self.electron_charge

    def get_max_I_winding(self):
        '''Ampere'''
        return self.max_current_per_m_2 / self.geometry.area_winding
    
    def get_I_linking(self):
        '''gives the current on the inside of the plasma loop in kA, with Formula mu_0 I = int B * dl'''
        return self.B_toroidal * self.radius_major * 2 * math.pi / self.mu_0

    def get_I_coil(self):
        '''kA'''
        return self.get_I_linking() / self.get_number_of_coils()

    def get_I_winding(self):
        '''kA, integrated control, does not exceed max_current'''
        c_p_w = self.get_I_linking() / (self.get_number_of_coils() * self.geometry.number_of_windings_total)
        #print(self.geometry.number_of_windings_total)
        if (c_p_w > self.max_I_winding):
            print(f'ERROR: too much current per winding; maximal current = ', self.max_I_winding, 'actual current = ', c_p_w)
            sys.exit()
        return c_p_w

    def get_resistance_per_circuit(self):
        '''ohm, calculated as rho*l/A'''
        return self.specific_resistance * self.get_length_of_circuit() / self.geometry.area_winding
    
    def get_resistance_per_winding(self):
        '''ohm, calculated as rho*l/A'''
        return self.specific_resistance * self.get_len_of_winding() / self.geometry.area_winding

    def get_voltage_per_circuit(self):
        '''Volt, claculated as U = I*R'''
        return self.get_resistance_per_circuit()*self.get_I_winding()

    def get_voltage_per_winding(self):
        '''Volt, claculated as U = I*R'''
        return self.get_resistance_per_winding()*self.get_I_winding()

    def get_power_per_winding(self):
        return self.get_voltage_per_winding() * self.get_I_winding()

    def get_power_per_circuit(self):
        return self.get_voltage_per_circuit() * self.get_I_winding()

    def get_number_of_windings(self):
        '''tries to assign a reasonable number of windings per coil, asks for permission'''
        number_of_windings = self.get_I_linking() / (self.max_I_winding * self.geometry.area_winding)
        print(number_of_windings)
        number_of_windings_x_test = int(math.sqrt(number_of_windings))
        number_of_windings_y_test = number_of_windings_x_test + 1
        print("It will be calculated with number_of_windings_x: ", number_of_windings_x_test, "and number_of_windings_y: ", number_of_windings_y_test)
        user_input = input("Do you want to continue with those values?[Y/N]: ")
        if user_input.lower().startswith('y'):
            self.geometry.number_of_windings_x = number_of_windings_x_test
            self.geometry.number_of_windings_y = number_of_windings_y_test
            return self.geometry.number_of_windings_x * self.geometry.number_of_windings_y
        elif user_input.lower().startswith('n'):#
            try:
                inp = input("Please give a value for the number_of_windings_x: ")
                self.geometry.number_of_windings_x = int(inp)
            except ValueError:
                print("Asshole, put in a valid value")
                return self.get_number_of_windings()
            try:
                inp = input("Please give a value for the number_of_windings_y: ")
                self.geometry.number_of_windings_y = int(inp)
            except ValueError:
                print("Asshole, put in a valid value")
                return self.get_number_of_windings()
        else:
            print("Please enter 'yes' or 'no'.")
            return self.get_number_of_windings() 

    def get_massflow(self):
        """calculates mass flow in kg/s"""
        c_spec = 4184 #J/(kg*K) 
        delta_T = 20 #°C
        P_tot = self.get_power_per_winding()*self.geometry.number_of_windings_x*2
        return P_tot/(c_spec*delta_T)

    def get_d_pressure(self):
        """pressure loss in a double pancake in bar"""
        roughness = 0.000005*1000 #convert m to mm
        pipeInnerDiam = 2*self.geometry.inner_radius/0.001
        massFlow = self.get_massflow()
        length = self.geometry.number_of_windings_x * 2 * 2 * math.pi * self.radius_minor
        delta_T = 20 #°C
        return(PL.PressureLoss_DW(length, pipeInnerDiam, massFlow, 20, roughness))

    def get_cond_volume(self):
        return self.geometry.area_winding * self.geometry.number_of_windings_total * self.number_of_coils_per_circuit*self.number_of_circuits

    def get_cupper_prize_total(self):
        return self.get_cond_volume()*cupper_price

    ##############################################################################################

    #controll

    ##############################################################################################

    def controll_radius_major(self):
        try:
            float(self.radius_major)
        except ValueError:
            raise Exception("not a valid value for major radius")
        
    ##############################################################################################
    
    def controll_outer_dimension(self):
        if (self.radius_major + self.radius_minor + self.geometry.len_x)*2 > self.diam_max:
            raise Exception(f"the construction diameter = {(self.radius_major + self.radius_minor + self.geometry.len_x + self.safety)*2} doesn't fit into the diam_max {self.diam_max}")
        if (self.radius_minor + self.geometry.len_x)*2 > self.max_height:
            raise Exception(f"the construction height = {(radius_minor + self.geometry)*2} doesn't fit into the max_height = {self.max_height}")
        if self.aspect_ratio > self.max_aspect_ratio or self.aspect_ratio < self.min_aspect_ratio:
            raise Exception(f"the aspect_ratio = {self.aspect_ratio} out of boundaries")

    def controll_number_of_windings_y(self):
        try:
            int(self.geometry.number_of_windings_y)
        except ValueError:
            raise Exception("not a valid value for number_of_windings_y")
        try:
            int(self.geometry.number_of_windings_y/2)
        except ValueError:
            raise Exception("number_of_windings_y needs to be even")

    def controll_circumference_within(self):
        if self.number_of_coils_per_circuit * self.number_of_circuits * self.geometry.len_y > self.get_circumference_within():
            raise Exception(f"inner coils radius = {self.number_of_coils_per_circuit * self.number_of_circuits * self.geometry.len_y} exceed radius = {self.get_circumference_within()}")
        
    def controll_geometry(self):
        if self.geometry.winding_radius <= self.geometry.inner_radius:
            raise Exception(f"inner_radius = {self.geometry.inner_radius} needs to be smaller than outer_radius {self.geometry.winding_radius}")
    ##############################################################################################

    #setters

    ##############################################################################################

    def set_B_toroidal(self, value):
        self.B_toroidal = value

    def set_mu_0(self, value):
        self.mu_0 = value

    def set_diam_max(self, value):
        self.diam_max = value

    def set_max_height(self, value):
        self.max_height = value

    def set_max_aspect_ratio(self, value):
        self.max_aspect_ratio = value

    def set_min_aspect_ratio(self, value):
        self.min_aspect_ratio = value

    def set_radius_major(self, value):
        self.radius_major = value

    def set_radius_minor(self, value):
        self.radius_minor = value

    def set_number_of_coils_per_circuit(self, value):
        self.number_of_coils_per_circuit = value

    def set_number_of_circuits(self, value):
        self.number_of_circuits = value

    def set_max_current_per_m_2(self, value):
        self.max_current_per_m_2 = value

    def set_specific_resistance(self, value):
        self.specific_resistance = value

    def set_winding_radius(self, value):
        self.winding_radius = value

    def set_inner_radius(self, value):
        self.inner_radius = value

    def set_max_I_winding(self, value):
        self.max_I_winding = value

    def set_len_coil(self, value):
        self.len_coil = value

    def set_length_of_circuit(self, value):
        self.length_of_circuit = value

    def set_I_linking(self, value):
        self.I_linking = value

    def set_radius_within(self, value):
        self.radius_within = value

    def set_total_circumference_of_coils_within(self, value):
        self.total_circumference_of_coils_within = value

    def set_number_of_coils(self, value):
        self.number_of_coils = value

    def set_I_coil(self, value):
        self.I_coil = value

    def set_I_winding(self, value):
        self.I_winding = value

    def set_volume_within(self, value):
        self.volume_within = value

    def set_aspect_ratio(self, value):
        self.aspect_ratio = value

    def set_resistance_per_circuit(self, value):
        self.resistance_per_circuit = value

    def set_voltage_per_circuit(self, value):
        self.voltage_per_circuit = value

    def set_frequency_rotation(self, value):
        self.frequency_rotation = value
        
    def set_B_toroidal(self, value):
        self.B_toroidal = value #Tesla

    def set_material(self, value):
        if value == 'copper':
            self.specific_resistance = 1.68e-8#Ohm*m @ 77°C
		    # heat capacity =
		    # heat conduction =
        elif value == "aluminum" or "aluminium":
            self.specific_resistance = 3.875e-8
		    #self.specific_resistance = 3.875*10**(-8)#Ohm*m @ 77°C (source: https://hypertextbook.com/facts/2004/ValPolyakov.shtml)
		    # heat capacity = 
		    # heat conduction = 
        if self.specific_resistance == None:
            raise Exception('Missing conductor material properties')
        self.material = value

    ##############################################################################################

    #other random but important functions

    ##############################################################################################

    def print_parameters(self):
        params = vars(self)
        for key, value in self.__dict__.items():
            if not key.startswith("__"):
                print(f"{key} = {value}")
        #self.geometry.draw_coil()

    