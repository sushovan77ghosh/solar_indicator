import xarray as xr
import numpy as np

def compute_sol_res_avail(rsds_file, rpd_threshold=200):
    """Compute solar resource availability percentage."""
    ds = xr.open_dataset(rsds_file)
    rsds = ds["rsds"]
    
    sol_res_avail = ((rsds > rpd_threshold).sum(dim="time") / rsds.time.size) * 100
    
    sol_res_avail.name = "resource_availability"
    sol_res_avail.attrs = {
        "shortname": "resource_availability",
        "longname": "Solar Resource Availability",
        "units": "%",
        "description": "Percentage of hours where RPD exceeds the threshold of 200 W/m²."
    }
    
    return sol_res_avail

def compute_bright_sunshine_hours(rsds_file, rpd_threshold=200):
    """Compute Bright Sunshine Hours (BSH) for each day where RPD exceeds the threshold."""
    ds = xr.open_dataset(rsds_file)
    rsds = ds["rsds"]

    bright_sunshine_hours = rsds.where(rsds > rpd_threshold).resample(time="1D").count()
    
    bright_sunshine_hours.name = "bright_sunshine_hours"
    bright_sunshine_hours.attrs = {
        "shortname": "bright_sunshine_hours",
        "longname": "Daily Bright Sunshine Hours",
        "units": "hours",
        "description": "Total duration per day where RPD exceeds the threshold of 200 W/m²."
    }

    return bright_sunshine_hours

def compute_episode_length(rsds_file, rpd_threshold=200):
    """Compute total episode length (in hours) where RPD is above threshold, for each day."""
    ds = xr.open_dataset(rsds_file)
    rsds = ds["rsds"]

    def compute_daily_episode_length(day_data):
        above_threshold = day_data > rpd_threshold
        episode_length = above_threshold.astype(int).sum(dim="time")
        return episode_length.where(episode_length > 0)

    episode_length = rsds.groupby("time.day").map(compute_daily_episode_length)
    episode_length.name = "resource_continuity"
    episode_length.attrs = {
        "shortname": "resource_continuity",
        "longname": "Daily Solar Resource Continuity",
        "units": "hours",
        "description": "Total duration per day where RPD exceeds the threshold of 200 W/m²."
    }

    return episode_length

def compute_percentage_continuity(rsds_file, rpd_threshold=200):
    """Compute the percentage of time each day that RPD is continuously above the threshold."""
    episode_length = compute_episode_length(rsds_file, rpd_threshold)
    total_daily_hours = 24
    percentage_continuity = (episode_length / total_daily_hours) * 100

    percentage_continuity.name = "percentage_resource_continuity"
    percentage_continuity.attrs = {
        "shortname": "percentage_resource_continuity",
        "longname": "Daily Percentage Solar Resource Continuity",
        "units": "%",
        "description": "Percentage of each day where RPD exceeds the threshold of 200 W/m²."
    }

    return percentage_continuity

