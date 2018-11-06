# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:39:08 2018

@author: Chinmay Deval
"""
import numpy as np

def celsius2kelvin(celsius):
    """
    Convert temperature in degrees Celsius to degrees Kelvin.
    :param celsius: Degrees Celsius
    :return: Degrees Kelvin
    :rtype: float
    """
    return celsius + 273.15


def kelvin2celsius(kelvin):
    """
    Convert temperature in degrees Kelvin to degrees Celsius.
    :param kelvin: Degrees Kelvin
    :return: Degrees Celsius
    :rtype: float
    """
    return kelvin - 273.15


def deg2rad(deg):
    """
    Convert angular degrees to radians
    :param degrees: Value in degrees to be converted.
    :return: Value in radians
    :rtype: float
    """
    return deg * (np.pi / 180.0)


def rad2deg(rads):
    """
    Convert radians to angular degrees
    :param radians: Value in radians to be converted.
    :return: Value in angular degrees
    :rtype: float
    """
    return rads * (180.0 / np.pi)


def ymd_to_doy(y,m,d):
    """
    converts year(m),month (m),day(d) columns to day of year (1-366)
    """
    J = np.add(np.add(np.subtract(d, 32.0),np.trunc(np.multiply(275.0, np.divide(m, 9.0)))),\
               np.add(np.multiply(2.0, np.trunc(np.divide(3.0, np.add(m, 1.0)))),np.trunc(np.add(np.subtract(np.divide(m, 100.0), np.divide(np.remainder(y, 4.0), 4.0)), 0.975))))
    
    return J.astype(int)
    