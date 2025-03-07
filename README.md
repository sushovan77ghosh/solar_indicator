# solar_indicator
Provides PV industry specific indicators from climate data 
The indicators include:


## 1. PV Potential 

PV potential depends on solar radiation (**rsds**), temperature (**tas**), and wind speed (**sfcWind**).

The equation is:

$$
PV_{pot} = \alpha_1 G + \alpha_2 G^2 + \alpha_3 G T_C + \alpha_4 G V
$$

where:
- \( G \) = Solar radiation (W/m²)
- \( T_C \) = Temperature in Celsius (°C)
- \( V \) = Wind speed (m/s)
- \( \alpha_1 = 0.18 \), \( \alpha_2 = -0.0001 \), \( \alpha_3 = -0.005 \), \( \alpha_4 = -0.002 \)

## 2. Solar Resource Metrics

**2.1.Solar Resource Availability (SRA)**

This metric calculates the percentage of time where solar resource power density (RPD) exceeds 200 W/m².  

**2.2.Bright sunshine Hours (BSH)**

This metric calculates the number of hours where solar resource power density (RPD) exceeds 200 W/m². 

**2.3.Episode length**

This metric calculates the continuous number of hours where solar resource power density (RPD) exceeds 200 W/m². 


## 3. PV Module Temperature & Efficiency Derating Analysis

This module provides functions to compute **PV cell temperature (Tcell)** and its impact on efficiency losses due to high operating temperatures.


**3.1 Hourly PV Cell Temperature**

**3.2 Daily maximum PV Cell Temperature**

**3.2 Number of hours / days where PV Cell Temperature exceedes threshold temperature : Efficiency de-rating hours/days**






 # References

Ghosh, Sushovan, et al. (2024). *Future photovoltaic potential in India: navigating the interplay between air pollution control and climate change mitigation*. Environmental Research Letters, 19(12), 124030.  https://iopscience.iop.org/article/10.1088/1748-9326/ad8c68

