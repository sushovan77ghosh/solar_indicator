#!/usr/bin/env python3
"""
# Destination Earth: Energy Onshore application
# Author: Sushovan Ghosh
# Version: x.y.z
"""

# Load libraries
import xarray as xr
import numpy as np
from .core import convert_temperature  # Use relative import for package structure

# Define constants from the equation
C1 = 4.3
C2 = 0.943
C3 = 0.028
C4 = -1.528


def Tcell_hourly(temp_file, rad_file, wind_file):
    """
    Compute hourly cell temperature (Tcell) based on air temperature, solar radiation, and wind speed.

    Input
    -------
    temp_file: str  → Path to NetCDF file containing 2m air temperature (tas in K).
    rad_file: str   → Path to NetCDF file containing downward solar radiation (rsds in W/m²).
    wind_file: str  → Path to NetCDF file containing surface wind speed (sfcWind in m/s).

    Output
    -------
    Tcell: xarray.DataArray (time, lat, lon)  → Computed hourly cell temperature in °C.
    """

    # Load datasets
    ds_tas = xr.open_dataset(temp_file)
    ds_rsds = xr.open_dataset(rad_file)
    ds_sfcWind = xr.open_dataset(wind_file)

    # Extract variables and force loading into memory
    T_K = ds_tas["tas"].load()  # 2m temperature (Kelvin)
    G = ds_rsds["rsds"].load()  # Solar radiation (W/m²)
    V = ds_sfcWind["sfcWind"].load()  # Wind speed (m/s)

    # Convert air temperature to Celsius
    T_C = convert_temperature(T_K, unit="C")

    # Compute Tcell
    Tcell = C1 + C2 * T_C + C3 * G + C4 * V

    # Assign attributes
    Tcell.name = "Tcell"
    Tcell.attrs = {
        "shortname": "Tcell",
        "long_name": "Hourly Cell Temperature",
        "units": "°C",
        "description": "Computed hourly cell temperature using air temperature, solar radiation, and wind speed."
    }

    return Tcell


def Tcell_daily_mean(temp_file, rad_file, wind_file):
    """
    Compute the daily mean of cell temperature (Tcell).

    Output
    -------
    Tcell_daily_mean: xarray.DataArray (time, lat, lon)
        Daily mean cell temperature.
    """

    Tcell = Tcell_hourly(temp_file, rad_file, wind_file)
    Tcell_daily_mean = Tcell.resample(time="1D").mean()

    # Assign attributes
    Tcell_daily_mean.name = "Tcell_daily_mean"
    Tcell_daily_mean.attrs = {
        "shortname": "Tcell_daily_mean",
        "long_name": "Daily Mean Cell Temperature",
        "units": "°C",
        "description": "Daily mean of computed cell temperature."
    }

    return Tcell_daily_mean


def Tcell_daily_max(temp_file, rad_file, wind_file):
    """
    Compute the daily maximum of cell temperature (Tcell).

    Output
    -------
    Tcell_daily_max: xarray.DataArray (time, lat, lon)
        Daily maximum cell temperature.
    """

    Tcell = Tcell_hourly(temp_file, rad_file, wind_file)
    Tcell_daily_max = Tcell.resample(time="1D").max()

    # Assign attributes
    Tcell_daily_max.name = "Tcell_daily_max"
    Tcell_daily_max.attrs = {
        "shortname": "Tcell_daily_max",
        "long_name": "Daily Maximum Cell Temperature",
        "units": "°C",
        "description": "Daily maximum of computed cell temperature."
    }

    return Tcell_daily_max


def efficiency_derating_days(temp_file, rad_file, wind_file):
    """
    Compute days with efficiency derating (Tcell_daily_max > 45°C) and de-rating hours per day.

    Output
    -------
    derating_days: xarray.DataArray (time, lat, lon)
        Boolean mask for days with Tcell_daily_max > 45°C.
    derating_hours: xarray.DataArray (time, lat, lon)
        Number of hourly instances per day where Tcell_hourly > 45°C.
    """

    # Compute hourly and daily max cell temperature
    Tcell = Tcell_hourly(temp_file, rad_file, wind_file)
    Tcell_max_daily = Tcell_daily_max(temp_file, rad_file, wind_file)

    # Identify days where Tcell_daily_max > 45°C
    derating_days = (Tcell_max_daily > 45).astype(int)  # Convert boolean mask to int (0 or 1)

    # Compute de-rating hours per day (Tcell_hourly > 45°C)
    derating_hours = Tcell.where(Tcell > 45).resample(time="1D").count()

    # Assign attributes
    derating_days.name = "efficiency_derating_days"
    derating_days.attrs = {
        "shortname": "efficiency_derating_days",
        "long_name": "Days with Efficiency Derating",
        "units": "Boolean (0 or 1)",
        "description": "Days where the maximum cell temperature exceeds 45°C."
    }

    derating_hours.name = "derating_hours"
    derating_hours.attrs = {
        "shortname": "derating_hours",
        "long_name": "De-rating Hours per Day",
        "units": "hours",
        "description": "Number of hours per day where the cell temperature exceeds 45°C."
    }

    return derating_days, derating_hours
# Define constants from the equation
C1 = 4.3
C2 = 0.943
C3 = 0.028
C4 = -1.528


def Tcell_hourly(temp_file, rad_file, wind_file):
    """
    Compute hourly cell temperature (Tcell) based on air temperature, solar radiation, and wind speed.

    Input
    -------
    temp_file: str  → Path to NetCDF file containing 2m air temperature (tas in K).
    rad_file: str   → Path to NetCDF file containing downward solar radiation (rsds in W/m²).
    wind_file: str  → Path to NetCDF file containing surface wind speed (sfcWind in m/s).

    Output
    -------
    Tcell: xarray.DataArray (time, lat, lon)  → Computed hourly cell temperature in °C.
    """

    # Load datasets
    ds_tas = xr.open_dataset(temp_file)
    ds_rsds = xr.open_dataset(rad_file)
    ds_sfcWind = xr.open_dataset(sfcwind_file)

    # Extract variables and force loading into memory
    T_K = ds_tas["tas"].load()  # 2m temperature (Kelvin)
    G = ds_rsds["rsds"].load()  # Solar radiation (W/m²)
    V = ds_sfcWind["sfcWind"].load()  # Wind speed (m/s)

    # Convert air temperature to Celsius
    T_C = convert_temperature(T_K, unit="C")

    # Compute Tcell
    Tcell = C1 + C2 * T_C + C3 * G + C4 * V

    # Assign attributes
    Tcell.name = "Tcell"
    Tcell.attrs = {
        "long_name": "Hourly Cell Temperature",
        "units": "°C",
        "description": "Computed hourly cell temperature using air temperature, solar radiation, and wind speed."
    }

    return Tcell


def Tcell_daily_mean(temp_file, rad_file, wind_file):
    """
    Compute the daily mean of cell temperature (Tcell).

    Output
    -------
    Tcell_daily_mean: xarray.DataArray (time, lat, lon)
        Daily mean cell temperature.
    """

    Tcell = Tcell_hourly(temp_file, rad_file, wind_file)
    Tcell_daily_mean = Tcell.resample(time="1D").mean()

    # Assign attributes
    Tcell_daily_mean.name = "Tcell_daily_mean"
    Tcell_daily_mean.attrs = {
        "long_name": "Daily Mean Cell Temperature",
        "units": "°C",
        "description": "Daily mean of computed cell temperature."
    }

    return Tcell_daily_mean


def Tcell_daily_max(temp_file, rad_file, wind_file):
    """
    Compute the daily maximum of cell temperature (Tcell).

    Output
    -------
    Tcell_daily_max: xarray.DataArray (time, lat, lon)
        Daily maximum cell temperature.
    """

    Tcell = Tcell_hourly(temp_file, rad_file, wind_file)
    Tcell_daily_max = Tcell.resample(time="1D").max()

    # Assign attributes
    Tcell_daily_max.name = "Tcell_daily_max"
    Tcell_daily_max.attrs = {
        "long_name": "Daily Maximum Cell Temperature",
        "units": "°C",
        "description": "Daily maximum of computed cell temperature."
    }

    return Tcell_daily_max


def efficiency_derating_days(temp_file, rad_file, wind_file):
    """
    Compute days with efficiency derating (Tcell_daily_max > 45°C) and de-rating hours per day.

    Output
    -------
    derating_days: xarray.DataArray (time, lat, lon)
        Boolea--------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[12], line 7
      4 rad_filen mask for days with Tcell_daily_max > 45°C.
    derating_hours: xarray.DataArray (time, lat, lon)
        Number of hourly instances per day where Tcell_hourly > 45°C.
    """

    # Compute hourly and daily max cell temperature
    Tcell = Tcell_hourly(temp_file, rad_file, wind_file)
    Tcell_max_daily = Tcell_daily_max(temp_file, rad_file, wind_file)

    # Identify days where Tcell_daily_max > 45°C
    derating_days = (Tcell_max_daily > 45).astype(int)  # Convert boolean mask to int (0 or 1)

    # Compute de-rating hours per day (Tcell_hourly > 45°C)
    derating_hours = Tcell.where(Tcell > 45).resample(time="1D").count()

    # Assign attributes
    derating_days.name = "efficiency_derating_days"
    derating_days.attrs = {
        "long_name": "Days with Efficiency Derating",
        "units": "Boolean (0 or 1)",
        "description": "Days where the maximum cell temperature exceeds 45°C."
    }

    derating_hours.name = "derating_hours"
    derating_hours.attrs = {
        "long_name": "De-rating Hours per Day",
        "units": "hours",
        "description": "Number of hours per day where the cell temperature exceeds 45°C."
    }

    return derating_days, derating_hours


import xarray as xr
import numpy as np
