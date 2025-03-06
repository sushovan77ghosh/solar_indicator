"""
# Solar Indicators - Utility Functions
# Author: Sushovan Ghosh
"""

import xarray as xr

def check_dimensions(var, expected_dims=("time", "lat", "lon")):
    """Checks if a given xarray DataArray has expected dimensions."""
    assert all(dim in var.dims for dim in expected_dims), f"Expected dimensions {expected_dims}, but got {var.dims}."

def load_dataset(file_path, variable_name):
    """Load a NetCDF file and extract a specified variable as an xarray DataArray."""
    ds = xr.open_dataset(file_path)
    return ds[variable_name].load()

