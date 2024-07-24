"""
Library of functions to pertubate coils
"""

import numpy as np
from simsopt.geo import CurveXYZFourier, RotatedCurve
from simsopt.field import Coil

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

# a simmilar function but using a translation vector
def translate_coil(coil_in, translation_vector):
    # evaluate order and dofs of the coil curve
    current = coil_in.current
    # print(type(coil_in.curve))
    if isinstance(coil_in.curve, RotatedCurve):
        rotatedCurve = True
        # print(dir(coil_in.curve))
        # print(coil_in.curve.x)
        # print(coil_in.curve.curve.get_dofs())
        # print(np.allclose(coil_in.curve.x, coil_in.curve.curve.get_dofs()))
        phi = coil_in.curve._phi
        flip = coil_in.curve.flip
        order = coil_in.curve.curve.order
        coil_dofs = coil_in.curve.curve.get_dofs()
    #print(dir(coil_in.curve))
    else:
        rotatedCurve = False
        order = coil_in.curve.order
        coil_dofs = coil_in.curve.get_dofs()
    # print(len(coil_dofs))

    # shift the curve by the given amount in the given axis
    for i in range(3):
        coil_dofs[i*(2 * order + 1)] = coil_dofs[i*(2 * order + 1)] + translation_vector[i]

    # create a new curve object with the shifted dofs
    curve_out = CurveXYZFourier(coil_in.curve.quadpoints, order)
    curve_out.set_dofs(coil_dofs)
    if rotatedCurve:
        curve_out = RotatedCurve(curve_out, phi, flip)
    coil_out = Coil(curve_out, current)

    return coil_out


def rotate_coil_y(coil_in, angle):
    # evaluate order and dofs of the coil curve
    current = coil_in.current
    order = coil_in.curve.order
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

def rotate_coil_x(coil_in, angle):
    # evaluate order and dofs of the coil curve
    current = coil_in.current
    order = coil_in.curve.order
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
    curve_out = CurveXYZFourier(coil_in.curve.quadpoints, order)
    curve_out.set_dofs(coil_dofs)
    coil_out = Coil(curve_out, current)

    return coil_out

def rotate_coil_z(coil_in, angle):
    # evaluate order and dofs of the coil curve
    current = coil_in.current
    order = coil_in.curve.order
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