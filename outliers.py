import pandas as pd 
import numpy as np
import math 
from statistics import mean

# A function to determine whether a number is an integer 
def is_integer(x):
    return abs(x - math.floor(x)) < 0.001

# Function to get quartiles 
def quartiles(lt, type = "first"):
    lst = lt.sort_values()
    n = len(lst) 

    if type == 'first':
        L = n / 4 
    elif type == 'third':
        L = 0.75 * n
    else:
        raise ValueError("Argument 'type' must be either 'first' (for first quartile) or 'third' (for third quartile)")

    if is_integer(L):
        # Since lists are 0-indexed, Lth value is at index L-1
        L = int(L) 
        return mean([lst.iloc[L-1], lst.iloc[L]]) 
    else:
        # Round L up 
        L = math.ceil(L) 
        return lst.iloc[L]

# Given a pandas series, return the lower and upper boundaries for outliers 
def outlier_boundaries(ser):
    q1 = quartiles(ser)
    q3 = quartiles(ser, type = "third")

    iqr = q3 - q1 
    lower_bdy = q1 - 1.5 * iqr
    upper_bdy = q3 + 1.5 * iqr
    return [lower_bdy, upper_bdy]

# Now we will read the data for 10 years
stocks = pd.read_csv("spx_ten_years.csv").reset_index(names = "Day") 
open = stocks["Open"] 
high = stocks["High"] 
low = stocks["Low"]
close = stocks["Close"]

# Boundaries
open_lower_bdy, open_upper_bdy = outlier_boundaries(open) 
high_lower_bdy, high_upper_bdy = outlier_boundaries(high) 
low_lower_bdy, low_upper_bdy = outlier_boundaries(low) 
close_lower_bdy, close_upper_bdy = outlier_boundaries(close)

# Boolean selectors
ix_open = (stocks["Open"] > open_upper_bdy) | (stocks["Open"] < open_lower_bdy) 
ix_high = (stocks["High"] > high_upper_bdy) | (stocks["High"] < high_lower_bdy)
ix_low = (stocks["Low"] > low_upper_bdy) | (stocks["Low"] < low_lower_bdy) 
ix_close = (stocks["Close"] > close_upper_bdy) | (stocks["Close"] < close_lower_bdy) 

# Get outliers 
outliers = stocks[(ix_open) | (ix_high) | (ix_low) | (ix_close)]
num_outliers = len(outliers.index)

outliers.to_csv("outliers.csv", header = True, index = False) 
print(f"Finished writing file outliers.csv: wrote {num_outliers} rows")
