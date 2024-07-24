"""
Library of functions to pertubate coils in shape and position
"""

import numpy as np
from simsopt.geo import CurveXYZFourier
from simsopt.field import Coil

# function to scale coil by maximum +/- scalefactor*rand percent
# takes the coil and multiplies all curve dofs except for 
# xc(0), yc(0) and zc(0) with scalefactor (in percent) * rand[-1,1]
def scale_coil(coil_in, scalefactor):

    current = coil_in.current
    try:
        coil_in.curve.order
        curve_in = coil_in.curve
    except AttributeError:
        curve_in = coil_in.curve.curve
    order = curve_in.order
    coil_dofs = curve_in.get_dofs()
    num_dofs = len(coil_dofs)
    modes = int(num_dofs/3)

    # exclude xc(0), yc(0) and zc(0)
    excluded_indices = [0, modes, 2*modes]

    # Create a mask that is True for elements to be multiplied
    mask = np.ones(len(coil_dofs), dtype=bool)
    mask[excluded_indices] = False

    # Multiply elements by the factor using the mask
    scalefactor_rand = scalefactor/100 * (-1 + 2*np.random.rand(1))
    print(scalefactor_rand)
    coil_dofs[mask] *= 1+scalefactor_rand

    # create a new curve object with the shifted dofs
    curve_out = CurveXYZFourier(coil_in.curve.quadpoints, order)#curve_in#CurveXYZFourier(coil_in.curve.quadpoints, order)
    curve_out.set_dofs(coil_dofs)
    coil_out = Coil(curve_out, current)

    return coil_out

# a function that takes a coil and shifts it by a given amount in a given axis
def shift_coil(coil_in, axis, amount):
    # evaluate order and dofs of the coil curve
    current = coil_in.current
    order = coil_in.curve.order
    coil_dofs = coil_in.curve.get_dofs()

    # shift the curve by the given amount in the given axis
    coil_dofs[axis*(2 * order + 1)] = coil_dofs[axis*order] + amount

    # create a new curve object with the shifted dofs
    curve_out = CurveXYZFourier(coil_in.curve.quadpoints, order)
    curve_out.set_dofs(coil_dofs)
    coil_out = Coil(curve_out, current)
    
    return coil_out


# wiggles the coil by adding a disturbance to the modes
# xs(1),xc(1), ys(1),yc(1), zs(1),zc(1)
def wiggle_coil(coil_in, disturbance):

    current = coil_in.current
    try:
        coil_in.curve.order
        curve_in = coil_in.curve
    except AttributeError:
        curve_in = coil_in.curve.curve
    order = curve_in.order
    coil_dofs = curve_in.get_dofs()
    num_dofs = len(coil_dofs)
    modes = int(num_dofs/3)

    xs = int(3)
    xc = int(4)
    excluded_indices = [xs,xc, xs+modes,xc+modes, xs+2*modes,xc+2*modes]

    # Create a mask that is True for elements to be multiplied
    mask = np.zeros(len(coil_dofs), dtype=bool)
    mask[excluded_indices] = True

    # Multiply elements by the factor using the mask
    coil_dofs[mask] += disturbance

    # create a new curve object with the shifted dofs
    curve_out = curve_in #CurveXYZFourier(coil_in.curve.quadpoints, order)
    curve_out.set_dofs(coil_dofs)
    coil_out = Coil(curve_out, current)

    return coil_out

# function to scale current by max +/- scalefactor*rand percent 
# takes the coil and multiplies the currnet dof by scalefactor(in percent) * rand[-1,1]
def scale_current(coil_in, scalefactor, *args, **kwargs):

    current_to_scale = coil_in.current
    
    current = current_to_scale.current_to_scale
    currentVals = current.get_dofs()
    
    
    # Multiply elements by the factor using the mask
    scalefactor_rand = scalefactor/100 * (-1 + 2*np.random.rand(1))
    currentVals *= 1+scalefactor_rand

    # copy coil_in into coil_out and change the dof-Value for the current
    coil_out = coil_in
    coil_out.current.current_to_scale.set_dofs(currentVals)
    
    return coil_out

#rotates the specified coil by angle degrees.
#Ask Jakob about mechanism!
def rotate_coil_x(coil_in, angle):
    # evaluate order and dofs of the coil curve
    current = coil_in.current
    order = coil_in.curve.order
    curve_in = coil_in.curve
    # print('order:', order)
    coil_dofs = coil_in.curve.get_dofs()

    rot_mat = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])

    x_c = range(0, 2 * order + 1, 2)
    x_s = range(-1, 2 * order + 1, 2)
    y_c = range(2 * order + 1, 4 * order + 2, 2)
    y_s = range(2 * order , 4 * order + 2, 2)
    z_c = range(4 * order + 2, 6 * order + 3, 2)
    z_s = range(4 * order + 1 , 6 * order + 3, 2)

    for m in range(1, order + 1):
        coil_v = np.array([coil_dofs[x_c[m]], coil_dofs[y_c[m]], coil_dofs[z_c[m]]]) # x, y, z
        coil_s = np.array([coil_dofs[x_s[m]], coil_dofs[y_s[m]], coil_dofs[z_s[m]]]) # x, y, z

        # print(f'c values, order: {m}, x: {x_c[m]}, y: {y_c[m]}, z: {z_c[m]}')
        # print(f's values order: {m}, x: {x_s[m]}, y: {y_s[m]}, z: {z_s[m]}')

        # rotate the curve by the given angle
        
        rot_coil_v = np.dot(rot_mat, coil_v)
        rot_coil_s = np.dot(rot_mat, coil_s)
        
        coil_dofs[x_c[m]] = rot_coil_v[0]
        coil_dofs[y_c[m]] = rot_coil_v[1]
        coil_dofs[z_c[m]] = rot_coil_v[2]
        coil_dofs[x_s[m]] = rot_coil_s[0]
        coil_dofs[y_s[m]] = rot_coil_s[1]
        coil_dofs[z_s[m]] = rot_coil_s[2]
    

    # create a new curve object with the shifted dofs
    curve_out = CurveXYZFourier(coil_in.curve.quadpoints, order) #curve_in#
    curve_out.set_dofs(coil_dofs)
    coil_out = Coil(curve_out, current)

    return coil_out


def rotate_coil_y(coil_in, angle):
    # evaluate order and dofs of the coil curve
    current = coil_in.current
    order = coil_in.curve.order
    curve_in = coil_in.curve
    # print('order:', order)
    coil_dofs = coil_in.curve.get_dofs()

    rot_mat = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])

    x_c = range(0, 2 * order + 1, 2)
    x_s = range(-1, 2 * order + 1, 2)
    y_c = range(2 * order + 1, 4 * order + 2, 2)
    y_s = range(2 * order , 4 * order + 2, 2)
    z_c = range(4 * order + 2, 6 * order + 3, 2)
    z_s = range(4 * order + 1 , 6 * order + 3, 2)

    for m in range(1, order + 1):
        coil_v = np.array([coil_dofs[x_c[m]], coil_dofs[y_c[m]], coil_dofs[z_c[m]]]) # x, y, z
        coil_s = np.array([coil_dofs[x_s[m]], coil_dofs[y_s[m]], coil_dofs[z_s[m]]]) # x, y, z

        # print(f'c values, order: {m}, x: {x_c[m]}, y: {y_c[m]}, z: {z_c[m]}')
        # print(f's values order: {m}, x: {x_s[m]}, y: {y_s[m]}, z: {z_s[m]}')

        # rotate the curve by the given angle
        
        rot_coil_v = np.dot(rot_mat, coil_v)
        rot_coil_s = np.dot(rot_mat, coil_s)
        
        coil_dofs[x_c[m]] = rot_coil_v[0]
        coil_dofs[y_c[m]] = rot_coil_v[1]
        coil_dofs[z_c[m]] = rot_coil_v[2]
        coil_dofs[x_s[m]] = rot_coil_s[0]
        coil_dofs[y_s[m]] = rot_coil_s[1]
        coil_dofs[z_s[m]] = rot_coil_s[2]
    

    # create a new curve object with the shifted dofs
    curve_out = CurveXYZFourier(coil_in.curve.quadpoints, order)
    curve_out.set_dofs(coil_dofs)
    coil_out = Coil(curve_out, current)

    return coil_out


def rotate_coil_z(coil_in, angle):
    # evaluate order and dofs of the coil curve
    current = coil_in.current
    order = coil_in.curve.order
    curve_in = coil_in.curve
    # print('order:', order)
    coil_dofs = coil_in.curve.get_dofs()

    rot_mat = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])

    x_c = range(0, 2 * order + 1, 2)
    x_s = range(-1, 2 * order + 1, 2)
    y_c = range(2 * order + 1, 4 * order + 2, 2)
    y_s = range(2 * order , 4 * order + 2, 2)
    z_c = range(4 * order + 2, 6 * order + 3, 2)
    z_s = range(4 * order + 1 , 6 * order + 3, 2)

    for m in range(1, order + 1):
        coil_v = np.array([coil_dofs[x_c[m]], coil_dofs[y_c[m]], coil_dofs[z_c[m]]]) # x, y, z
        coil_s = np.array([coil_dofs[x_s[m]], coil_dofs[y_s[m]], coil_dofs[z_s[m]]]) # x, y, z

        # print(f'c values, order: {m}, x: {x_c[m]}, y: {y_c[m]}, z: {z_c[m]}')
        # print(f's values order: {m}, x: {x_s[m]}, y: {y_s[m]}, z: {z_s[m]}')

        # rotate the curve by the given angle
        
        rot_coil_v = np.dot(rot_mat, coil_v)
        rot_coil_s = np.dot(rot_mat, coil_s)
        
        coil_dofs[x_c[m]] = rot_coil_v[0]
        coil_dofs[y_c[m]] = rot_coil_v[1]
        coil_dofs[z_c[m]] = rot_coil_v[2]
        coil_dofs[x_s[m]] = rot_coil_s[0]
        coil_dofs[y_s[m]] = rot_coil_s[1]
        coil_dofs[z_s[m]] = rot_coil_s[2]
    

    # create a new curve object with the shifted dofs
    curve_out = CurveXYZFourier(coil_in.curve.quadpoints, order)
    curve_out.set_dofs(coil_dofs)
    coil_out = Coil(curve_out, current)

    return coil_out