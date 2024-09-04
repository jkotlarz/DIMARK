# DIMARK/climate.py

import numpy as np

def calculate_npp_coefficient(avg_temp, annual_precipitation, CO2_concentration, growing_season_length):
    """
    This function calculates the coefficient modifying the net primary productivity (NPP) of biomass.
    
    Parameters:
    - avg_temp (float): Average annual temperature in degrees Celsius.
    - annual_precipitation (float): Annual precipitation in millimeters.
    - CO2_concentration (float): CO2 concentration in the atmosphere in ppm (parts per million).
    - growing_season_length (int): Length of the growing season in days.
    
    Returns:
    - float: Coefficient modifying net primary productivity (NPP) of biomass.
    """
    
    # Weight coefficients for each parameter (can be adjusted based on empirical data)
    weight_temp = 0.3
    weight_precipitation = 0.25
    weight_CO2 = 0.2
    weight_season = 0.25
    
    # Normalization of input values (approximate, reference values can be adjusted)
    norm_temp = avg_temp / 30.0  # Assuming 30°C is the optimal temperature
    norm_precipitation = annual_precipitation / 1000.0  # Assuming 1000 mm of precipitation is optimal
    norm_CO2 = CO2_concentration / 400.0  # Assuming 400 ppm CO2 is a reference level
    norm_season = growing_season_length / 180.0  # Assuming 180 days is the optimal growing season
    
    # Calculate the NPP coefficient
    npp_coefficient = (
        weight_temp * norm_temp +
        weight_precipitation * norm_precipitation +
        weight_CO2 * norm_CO2 +
        weight_season * norm_season
    )
    
    return npp_coefficient


# 'a' - matrix representing areas covered by species at specific ages
# 'ro' - matrix representing the average density of wood volume per hectare for species at specific ages
# 'h' - matrix representing the shares of areas covered by species at specific ages that are harvested

