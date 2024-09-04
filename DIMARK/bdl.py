#DIMARK/bdl.py

# The functions in this file require source data obtained from the Forest Data Bank (Bank Danych o Lasach), accessible at www.bdl.lasy.gov.pl. The data can be downloaded through the form available on the website https://www.bdl.lasy.gov.pl/portal/wniosek. For the selected year, data for the chosen set of forest districts should be downloaded and extracted into a single directory, resulting in approximately 400 folders for the entire country, such as ["BDL_01_01_AUGUSTOW_2022", "BDL_01_02_BIALOWIEZA_2022", ...]. It is imperative that the structure of the files within the folders downloaded from the data bank remains unaltered.

import numpy as np
import pandas as pd
import os
from tqdm import tqdm

# Function that returns the area of cultivation of a species within the age range in a given forest district as an array of length 200.
def cultivation_areaf(species, agemin, agemax, folderBDL, folder=""):
    """
    Calculates the cultivation area of a given tree species within a specified age range
    in a given forest district based on data from the BDL folder.

    :param species: Tree species code (str)
    :param agemin: Minimum tree age (int)
    :param agemax: Maximum tree age (int)
    :param folderBDL: Name of the folder with BDL data (str)
    :return: Array of length 200 with the cultivation area within the specified age range (np.ndarray)
    """
    bdl_subarea = pd.read_csv(folder + "/" + folderBDL + "/f_subarea.txt", sep='\t')
    bdl_storey = pd.read_csv(folder + "/" + folderBDL + "/f_storey_species.txt", sep='\t')
    area = bdl_subarea.set_index('arodes_int_num')['sub_area'].to_dict()
    bdl_storey = bdl_storey.fillna(0)
    df = bdl_storey[
        (bdl_storey.storey_cd.str.startswith("DRZEW")) 
        & (bdl_storey.species_cd.str.startswith(species)) 
        & (bdl_storey.volume > 0)]
    df["area_wydz"] = df["arodes_int_num"].map(area)
    df['part_cd_act'] = pd.to_numeric(df['part_cd_act'], errors='coerce')
    df["area"] = df["area_wydz"] * df["part_cd_act"] * 0.1
    areas = np.zeros(200)
    for wiek in range(agemin, agemax):
        dfw = df[df.species_age == wiek] 
        areas[wiek] = dfw.area.sum()
    return areas

# Function that returns the area of cultivation of a species within the age range in a given forest district as an array of length 200.
def cultivation_volumef(species, agemin, agemax, folderBDL, folder=""):
    """
    Calculates the cultivation volume of a given tree species within a specified age range
    in a given forest district based on data from the BDL folder.

    :param species: Tree species code (str)
    :param agemin: Minimum tree age (int)
    :param agemax: Maximum tree age (int)
    :param folderBDL: Name of the folder with BDL data (str)
    :return: Array of length 200 with the cultivation area within the specified age range (np.ndarray)
    """
    bdl_subarea = pd.read_csv(folder + "/" + folderBDL + "/f_subarea.txt", sep='\t')
    bdl_storey = pd.read_csv(folder + "/" + folderBDL + "/f_storey_species.txt", sep='\t')
#    area = bdl_subarea.set_index('arodes_int_num')['sub_area'].to_dict()
    bdl_storey = bdl_storey.fillna(0)
    df = bdl_storey[
        (bdl_storey.storey_cd.str.startswith("DRZEW")) 
        & (bdl_storey.species_cd.str.startswith(species)) 
        & (bdl_storey.volume > 0)]
    df["volume_wydz"] = bdl_storey.volume
#    df['part_cd_act'] = pd.to_numeric(df['part_cd_act'], errors='coerce')
#    df["area"] = df["area_wydz"] * df["part_cd_act"] * 0.1
    volumes = np.zeros(200)
    for wiek in range(agemin, agemax):
        dfw = df[df.species_age == wiek] 
        volumes[wiek] = dfw.volume_wydz.mean()
    return volumes

# Function that returns a list of directories in the given folder f
def list_directories(f):
    """
    Returns a list of directories in the given folder.

    :param f: Path to the directory (str)
    :return: List of directories in the folder (list)
    """
    try:
        # Check if the folder exists
        if not os.path.isdir(f):
            raise ValueError(f"{f} is not a directory or does not exist.")
        
        # List of directories in folder f
        return [d for d in os.listdir(f) if os.path.isdir(os.path.join(f, d))]
    
    except Exception as e:
        print(f'Error: {e}')
        return []

# Function that returns the area of cultivation of a species within the age range in the whole of Poland as an array of length 200.
def cultivation_area(species, agemin, agemax, folder=""):
    """
    Calculates the cultivation area of a given tree species within a specified age range
    for the whole of Poland based on data from multiple BDL folders.

    :param species: Tree species code (str)
    :param agemin: Minimum tree age (int)
    :param agemax: Maximum tree age (int)
    :return: Array of length 200 with the cultivation area within the specified age range (np.ndarray)
    """
    flist = list_directories(folder +"/")
    y = cultivation_areaf(species, agemin, agemax, flist[0], folder)
    for f in tqdm(flist[1:], desc="Progress", unit="dir", ncols=100):
        x = cultivation_areaf(species, agemin, agemax, f, folder)
        for i in range(len(y)):
            y[i] += x[i]
    return y


# Function that returns the area of cultivation of a species within the age range in the whole of Poland as an array of length 200.
def cultivation_volume(species, agemin, agemax, folder=""):
    """
    Calculates the cultivation timber volume of a given tree species within a specified age range
    for the whole of Poland based on data from multiple BDL folders.

    :param species: Tree species code (str)
    :param agemin: Minimum tree age (int)
    :param agemax: Maximum tree age (int)
    :return: Array of length 200 with the cultivation area within the specified age range (np.ndarray)
    """
    flist = list_directories(folder +"/")
    n = len(flist)
    y = cultivation_areaf(species, agemin, agemax, flist[0], folder)
    n0 = np.zeros(200)
    for f in tqdm(flist[1:], desc="Progress", unit="dir", ncols=100):
        x = cultivation_volumef(species, agemin, agemax, f, folder)
        
        for i in range(len(y)):
            if (x[i]> 1.0):    
                y[i] += x[i]
                n0[i] = n0[i]+1
            
    for i in range(len(y)):
        if n0[i] > 0:
            y[i] = y[i]/n0[i]
    return y,n0


# Function that smooths data using moving averages
def smooth_data(data, window_size=10):
    """
    Smooths the input data using moving averages.

    :param data: Array of input data (np.ndarray or list)
    :param window_size: Window size for calculating the average (int)
    :return: Smoothed array (np.ndarray)
    """
    if window_size < 1:
        raise ValueError("Window size must be greater than 0.")
    
    data = np.array(data)
    smoothed_data = np.zeros_like(data, dtype=float)
    cumsum = np.cumsum(data, dtype=float)
    cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
    smoothed_data[window_size - 1:] = cumsum[window_size - 1:] / window_size
    
    for i in range(window_size - 1):
        smoothed_data[i] = np.mean(data[:i + 1])
    
    return smoothed_data

# Function that sums the area in the array area[0-120] from the minimum year to the maximum, optionally shifting the tree age to the year
def areainyear(a, yearmin=90, yearmax=120, year=2022):
    """
    Sums the cultivation area in array a within the given age range, with the option to shift tree age to the specified year.

    :param a: Array of cultivation areas (np.ndarray)
    :param yearmin: Minimum tree age (int)
    :param yearmax: Maximum tree age (int)
    :param year: Year to which the tree age is adjusted (int)
    :return: Sum of cultivation areas within the specified age range (float)
    """
    if year < 2022:
        return 0
    else:
        dy = year - 2022
        return sum(a[yearmin - dy:yearmax - dy])

# Function that returns the distribution of harvesting in array area[0-120] with the option to smooth
def harvest_probability(a, yearmin=90, yearmax=120, av=1, transmission=0.01):
    """
    Calculates the distribution of harvesting probability based on the cultivation area array,
    with the option to smooth the data.

    :param a: Array of cultivation areas (np.ndarray)
    :param yearmin: Minimum tree age for harvesting (int)
    :param yearmax: Maximum tree age for harvesting (int)
    :param av: Window size for smoothing the data (int)
    :param transmission: Transmission factor for adjusting the harvesting probability (float)
    :return: Array with the distribution of harvesting probability (np.ndarray)
    """
    
    h = np.zeros(200)
    for y in range(yearmin, yearmax):
        h[y] = a[y - 1] - a[y]
        h[y] = max(h[y], 0)
    
    suma = sum(h)
    for y in range(yearmin, yearmax):
        h[y] = h[y] / suma
    
    if av > 1:
        h = smooth_data(h, av)
        h_sum = sum(h)
        if h_sum < 0.99:
            for y in range(yearmin, yearmax):
                h[y] = h[y] / h_sum

    h_trans = 1.
    not0 = 0
    s = []
    for y in range(len(a)):
        s.append(1 - h[y])
        if h[y] > 0:
            not0 = not0 + 1
        h_trans = h_trans * (1. - h[y])
    print(transmission, h_trans, not0)
    k = np.power(transmission / h_trans, 1.)    
    for y in range(len(a)):
        s[y] = s[y] * k
    for y in range(len(a)):
        if h[y] > 0 and h[y + 1] == 0:
            h[y] = 1.0 - s[y]
    
    return h

# Function that returns the harvesting area based on area and the harvesting probability distribution
def harvest_area(a, h_prob):
    """
    Calculates the harvesting area based on the cultivation area array
    and the distribution of harvesting probability.

    :param a: Array of cultivation areas (np.ndarray)
    :param h_prob: Array with the distribution of harvesting probability (np.ndarray)
    :return: Harvesting area (float)
    """
    return sum(a * h_prob)

# Function that allows calculating the distribution of cultivation areas at an earlier time based on the distribution of areas by age
def harvest_area_past(area, harvest_age_min, harvest_age_max, timeback_projection, curr_year=2022):
    """
    Calculates the area available for harvesting in the past, taking into account projected historical data
    based on a specified harvesting age range.

    :param area: Array of cultivation areas (np.ndarray)
    :param harvest_age_min: Minimum tree age for harvesting (int)
    :param harvest_age_max: Maximum tree age for harvesting (int)
    :param timeback_projection: Number of years for the backward projection (int)
    :param curr_year: Current year from which the projection starts (int, default is 2022)
    :return: Two lists: list of years and list of corresponding areas available for harvesting in those years (list, list)
    """
    z2 = []
    treshold = area[10:30].mean()  # Set threshold based on the average area in the range 10-30 years
    for i in range(len(area)):
        if (area[i] > treshold) or (i > 20):
            z2.append(area[i])
        else:
            z2.append(treshold)
            area[i] = treshold
    beforeH = area[harvest_age_min - 5:harvest_age_min].mean()
    afterH = area[harvest_age_max:harvest_age_max + 5].mean()
    percent = afterH / beforeH
    print("percent", percent)
    hp = harvest_probability(area, harvest_age_min, harvest_age_max, 5, percent)  # Calculate the distribution of harvesting probability
    retY = []
    retHVA = []
    for dyear in range(0, timeback_projection):
        harvested = z2[0]
        for i in range(len(area) - 1):
            z2[i] = z2[i + 1] + hp[i] * harvested
        
        y = curr_year - dyear
        if y < curr_year:
            retY.append(y)
            retHVA.append(areainyear(z2, harvest_age_min, harvest_age_max))
    
    return retY, retHVA

# Function that allows predicting the distribution of cultivation areas by age in the future based on the current distribution
def age_area_prediction(a, harvest_age_min, harvest_age_max, years=100):
    """
    Allows predicting the distribution of cultivation areas by age in the future based on the current distribution
    and the distribution of harvesting probability.

    :param a: Array of current cultivation areas by tree age (np.ndarray)
    :param harvest_age_min: Minimum tree age for harvesting (int)
    :param harvest_age_max: Maximum tree age for harvesting (int)
    :param years: Number of years for the prediction (int, default is 100)
    :return: List of arrays representing the distribution of cultivation areas for subsequent years (list of np.ndarray)
    """
    beforeH = a[harvest_age_min - 5:harvest_age_min].mean()
    afterH = a[harvest_age_max:harvest_age_max + 5].mean()
    percent = afterH / beforeH
    hp = harvest_probability(a, harvest_age_min, harvest_age_max, 5, percent)  # Calculate the distribution of harvesting probability
    setA = []
    ca = [v for v in a]
    setA.append(ca)
    for y in range(years):
        harvest = sum(hp * ca)
        ca = [v for v in setA[len(setA) - 1]]
        for age in range(len(ca) - 1, 0, -1):
            ca[age] = ca[age - 1] * max(0., 1. - hp[age])
        setA.append(ca)
        setA[len(setA) - 1][0] = harvest
    return setA

# Function that allows predicting the harvesting area based on the age distribution of cultivation areas
def harvest_area_prediction(area, harvest_age_min, harvest_age_max, time_projection, curr_year=2022):
    """
    Allows predicting the harvesting area based on the age distribution of cultivation areas.

    :param area: Array of cultivation areas (np.ndarray)
    :param harvest_age_min: Minimum tree age for harvesting (int)
    :param harvest_age_max: Maximum tree age for harvesting (int)
    :param time_projection: Number of years for the prediction (int)
    :param curr_year: Current year from which the prediction starts (int, default is 2022)
    :return: Two lists: list of years and list of corresponding harvesting areas in those years (list, list)
    """
    age_area = age_area_prediction(area, harvest_age_min, harvest_age_max, time_projection)
    retY = []
    retHVA = []
    for y in range(time_projection):
        retY.append(y + curr_year)
        retHVA.append(sum(age_area[y][harvest_age_min: harvest_age_max]))
    return retY, retHVA
