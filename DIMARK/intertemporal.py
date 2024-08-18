# DIMARK/intertemporal.py

from . import bdl as bdl
import matplotlib.pyplot as plt

# 'a' - matrix representing areas covered by species at specific ages
# 'ro' - matrix representing the average density of wood volume per hectare for species at specific ages
# 'h' - matrix representing the shares of areas covered by species at specific ages that are harvested

def Mmultiple(a, b):
    """Element-wise multiplication of two matrices."""
    return [[a[x][y] * b[x][y] for y in range(len(a[0]))] for x in range(len(a))]

def wood_volume(a, ro):
    """Calculates the wood volume by multiplying the area matrix with the density matrix."""
    return Mmultiple(a, ro)

def harvest_volume(a, h, ro):
    """Calculates the harvest volume by first calculating the harvested area and then multiplying it with the density matrix."""
    ah = Mmultiple(a, h)
    return Mmultiple(ah, ro)

# The following function assumes that the matrices 'ro' (due to changes in climate generating new wood growth models) 
# and 'h' (as forestry policies may change the harvesting model) can be manipulated. 
# We assume that a series of matrices 'ro' and 'h', along with an initial area matrix 'a', are given. 
# The function will calculate the harvested wood volumes for each species over the years.

def area_prediction(area_t0, harvest, time=100):
    """Predicts the area and harvested wood volumes over a specified time period.
    
    Parameters:
    area_t0 (list of lists): Initial area matrix for species at specific ages.
    harvest (list of lists): A sequence of harvest matrices over time.
    time (int): Number of years to simulate. Defaults to 100.
    
    Returns:
    tuple: A tuple containing the predicted area matrices and harvested volumes over time.
    """
    a = []
    a.append(area_t0)
    harvested = []
        
    for t in range(time):
        curr_a = [row[:] for row in a[t]]  # Deep copying of 2D area matrix
        curr_h = [row[:] for row in harvest[t]]  # Deep copying of 2D harvest matrix
        harv_area = Mmultiple(curr_a, curr_h)  # Calculate harvested area
        #print("ha", harv_area)
        ages = len(curr_a[0])
        #print("ages", ages)
        ch = []
        for species in range(len(curr_a)):
            for age in range(ages):
                curr_a[species][age] -= harv_area[species][age]  # Subtract harvested area
            curr_a[species][ages-2] += curr_a[species][ages-1]  # Transfer remaining area from the oldest age
            curr_a[species].pop()  # Remove the oldest age class
            curr_a[species].insert(0, sum(harv_area[species]))  # Insert the new area harvested at the youngest age
            ch.append(sum(harv_area[species]))
        new_a = [row[:] for row in curr_a]  # Deep copy the updated area matrix
        new_ch = [row for row in ch]  # Copy the harvested volumes
        
        a.append(new_a)
        harvested.append(new_ch)
    return a, harvested  # Return the updated area matrices and harvested volumes over time
