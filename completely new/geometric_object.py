import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class coil_geometry:
    '''geometric object'''
    def __init__(self, name):
        self.name = name
    
    def get_area(self):
        pass

    def perimeter(self):
        pass

class rund(coil_geometry):
    def __init__(self, name, radius_winding, radius_cooling, number_of_windings_x, number_of_windings_y):
        super().__init__(name)
        self.radius_winding = radius_winding
        self.radius_cooling = radius_cooling
        self.number_of_windings_x = number_of_windings_x
        self.number_of_windings_y = number_of_windings_y
        self.area = math.pi * self.radius_winding ** 2
    
    def get_area(self):
        return 3.14 * self.radius_winding ** 2
    
    def paint(self):
        return 2 * 3.14 * self.radius

class Rectangle(GeometricObject):
    def __init__(self, name, length, width):
        super().__init__(name)
        self.length = length
        self.width = width
    
    def get_area(self):
        return self.length * self.width
    
    def perimeter(self):
        return 2 * (self.length + self.width)

