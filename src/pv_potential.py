#!/usr/bin/env python3
"""
# Destination Earth: Energy Onshore Application
# Author: Sushovan Ghosh
# Version: x.y.z
"""

# Load necessary libraries
import xarray as xr
import numpy as np
import sys

# Add core module path
#sys.path.append("/scratch/b/b383073/solar_ind")
#from core import get_type, convert_temperature

# Relative Import (Works Inside `src/` Package)
from core import get_type, convert_temperature

# Define PV potential calculation function
def pv_pot(temp_file, rad_file, sfcwind_file):
    """
    Compute the PV potential (PV_pot) based on hourly solar radiation, temperature, and wind speed.

    Input
    -------
    temp_file: str
        Path to the NetCDF file containing 2m air temperature (tas).
    rad_file: str
        Path to the NetCDF file containing surface solar radiation downwards (rsds).
    sfcwind_file: str
        Path to the NetCDF file containing surface wind speed (sfcWind).

    Output
    -------
    pv_pot_hourly: xarray.DataArray ; (time, lat, lon)
        Computed PV potential values at an hourly frequency.

    References
    -------
    [1]: https://iopscience.iop.org/article/10.1088/1748-9326/ad8c68/meta
    [2]: https://doi.org/10.1038/ncomms10014
    """

    # Load datasets
    ds_tas = xr.open_dataset(temp_file)
    ds_rsds = xr.open_dataset(rad_file)
    ds_sfcWind = xr.open_dataset(sfcwind_file)

    # Extract variables and **force loading into memory**
    T_K = ds_tas["tas"].load()  # 2m temperature (Kelvin)
    G = ds_rsds["rsds"].load()  # Solar radiation (W/m²)
    V = ds_sfcWind["sfcWind"].load()  # Wind speed (m/s)

    # Convert temperature to Celsius
    T_C = convert_temperature(T_K, unit="C")

    # Check input dimensions
    for var, name in zip([T_C, G, V], ["T_C", "G", "V"]):
        assert var.ndim == 3, f"The input variable {name} does not have the required dimensions (time, lat, lon)."

    # Define PV potential coefficients
    alpha1 = 1.1035e-3  # (W m^-2)^-1
    alpha2 = 1.4e-7  # (W m^-2)^-2
    alpha3 = -4.715e-6  # (W°C m^-2)^-1
    alpha4 = 7.64e-6  # (W ms)^-1

    # Compute PV potential (PV_pot)
    PV_pot = alpha1 * G + alpha2 * G**2 + alpha3 * G * T_C + alpha4 * G * V

    # Assign attributes correctly
    attrs = {
        "shortname": "PVP",
        "longname": "PV Potential",
        "units": "dimensionless",
        "description": "Computed PV potential using surface solar radiation, temperature, and wind speed."
    }
    coords = {"time": G.time, "lat": G.lat, "lon": G.lon}
    dims = ("time", "lat", "lon")

    # Convert to xarray DataArray
    pv_pot_hourly = xr.DataArray(PV_pot, dims=dims, coords=coords, attrs=attrs, name=attrs["shortname"])

    return pv_pot_hourly

