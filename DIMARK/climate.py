# DIMARK/climate.py

import numpy as np
import pandas as pd 

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
    norm_temp = avg_temp / 7.0  # Assuming 7°C is the optimal temperature
    norm_precipitation = annual_precipitation / 800.0  # Assuming 800 mm of precipitation is optimal
    norm_CO2 = CO2_concentration / 400.0  # Assuming 400 ppm CO2 is a reference level
    norm_season = growing_season_length / 250.0  # Assuming 150 days is the optimal growing season
    
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

def NPP_climate(file_path, c_NPP):
    """
    Reads the CSV file from the given path, multiplies values in columns ending with 'dv' by c_NPP,
    and returns these columns as a DataFrame.
    
    Parameters:
    - file_path: The path to the NPP CSV file
    - c_NPP: The multiplier value to apply to columns ending with 'dv'
    
    Returns:
    - A DataFrame containing the processed columns
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Identify columns ending with 'dv'
    dv_columns = [col for col in df.columns if col.endswith('dv')]
    
    # Multiply the values in these columns by c_NPP
    for col in dv_columns:
        df[col] = df[col] * c_NPP
    
    # Return the filtered columns as a new DataFrame
    return df[dv_columns]