# Load libraries
import xarray as xr
import numpy as np
import pandas as pd


def get_type(var):
    """Returns the type of xarray object."""
    return str(type(var)).split("'")[1].split(".")[-1]

def convert_temperature(temp_K, unit="C"):
    """Convert temperature from Kelvin to Celsius."""
    if unit == "C":
        return temp_K - 273.15
    else:
        raise ValueError("Unsupported temperature unit")

