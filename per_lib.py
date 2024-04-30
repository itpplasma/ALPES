'''my personal library'''


class VariableWithUnit:
    '''A variable with unit included; if you give the variable name, it will give you the value; 
    if you give Variable_name.unit, it gives you the unit'''
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __getattr__(self, name):
        '''Override __getattr__ to delegate attribute access'''
        if name in ('value', 'unit'):
            return getattr(self, name)
        elif name.startswith('__') and name.endswith('__'):
            # Allow other magic methods to proceed as usual
            raise AttributeError
        else:
            # Otherwise, assume mathematical operation with self.value
            return getattr(self.value, name)

    def __str__(self):
        '''Override __str__ to return the value when the object is converted to a string'''
        return str(self.value)

    def __lt__(self, other):
        '''Override less than comparison'''
        return self.value < other

    def __le__(self, other):
        '''Override less than or equal to comparison'''
        return self.value <= other

    def __eq__(self, other):
        '''Override equal to comparison'''
        return self.value == other

    def __ne__(self, other):
        '''Override not equal to comparison'''
        return self.value != other

    def __gt__(self, other):
        '''Override greater than comparison'''
        return self.value > other

    def __ge__(self, other):
        '''Override greater than or equal to comparison'''
        return self.value >= other