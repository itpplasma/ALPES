import math
import sys


from variables import * 
from setters import *
from functions import *
from controll import *

def main():
    

    #do the calculations
    do_calculations_1()

    all_variables =  get_global_variables()
    output_variables = all_variables[len(input_variables)+1:len(all_variables)]
    give_system_status(input_variables[0:len(input_variables)-2], output_variables)
    return 0

main()