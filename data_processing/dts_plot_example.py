##Imports
from datetime import datetime
from datetime import timedelta
from glob import glob
from time import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as mpimg
import numpy as np
import os

##!>Set working directory to correct folder (BR-DTS-Processing)
working_directory = r'D:\Github\BR-DTS-Processing'
os.chdir(working_directory)

##Custom imports:
#Make sure the working directory is correctly set
from data_processing import dataImports
from data_processing import customFunctions

##DTS import
file_name = r'xml_conversion\output\dts_data.txt'

dts_time, dts_distances, dts_temperatures = dataImports.dts(file_name)


#Cut off distance under 0m
zero_distance_index = customFunctions.index_closest_value(dts_distances,0)

dts_distances    = dts_distances[zero_distance_index:-1]
dts_temperatures = dts_temperatures[:, zero_distance_index:-1]


##turns temperatures and distances into profiles
#Enter distances:
distance_dry_bottom = 99.25
distance_dry_top    = 144.25
distance_wet_bottom = 194.5
distance_wet_top    = 149.5

bottom_cable        = 1
top_cable           = 46

#Get indexes of heights
index_dry_bottom = customFunctions.index_closest_value(dts_distances, distance_dry_bottom)
index_dry_top    = customFunctions.index_closest_value(dts_distances, distance_dry_top)
index_wet_bottom = customFunctions.index_closest_value(dts_distances, distance_wet_bottom)
index_wet_top    = customFunctions.index_closest_value(dts_distances, distance_wet_top)

#Calculate the data ranges, and correct it if one is bigger than the other
index_range_dry = abs(index_dry_bottom - index_dry_top)
index_range_wet = abs(index_wet_bottom - index_wet_top)

index_range = min([index_range_dry,index_range_wet])

#Get temperature profiles
#Get temperature arrays, bottom to top
if index_dry_bottom > index_dry_top and index_wet_top > index_wet_bottom:
    #Cable goes; machine -> wet -> top of tower -> dry
    temperature_dry_bottom_to_top = dts_temperatures[:,index_dry_bottom-index_range:index_dry_bottom][:,::-1]
    temperature_wet_bottom_to_top = dts_temperatures[:,index_wet_bottom:index_wet_bottom+index_range]

if index_dry_bottom < index_dry_top and index_wet_top < index_wet_bottom:
    #Cable goes; machine -> dry -> top of tower -> wet
    temperature_dry_bottom_to_top = dts_temperatures[:,index_dry_bottom:index_dry_bottom+index_range]
    temperature_wet_bottom_to_top = dts_temperatures[:,index_wet_bottom-index_range:index_wet_bottom][:,::-1]

#Create distance reference
distance_array = np.linspace(bottom_cable, top_cable, 
                             num=len(temperature_dry_bottom_to_top[0]))
    
##Plots
#Plot 2d plot
#Note the water baths at the left and right side of figure
fig, ax = plt.subplots()
plot_2d = ax.imshow(dts_temperatures, interpolation='nearest', aspect='auto')
ax.set_xlabel('Distance index')
ax.set_ylabel('Time index')
ax.set_title('DTS cable temperature')
fig.colorbar(plot_2d)

#Plot temperature profile
time_index = 5
fig, (ax1,ax2) = plt.subplots(ncols=2, sharey=True)
ax1.plot(temperature_dry_bottom_to_top[time_index], distance_array, 'r')
ax1.set_xlabel('Dry temperature ($\degree$C)')
ax1.set_ylabel('Height (m)')
ax2.plot(temperature_wet_bottom_to_top[time_index], distance_array, 'b')
ax2.set_xlabel('Wet temperature ($\degree$C)')
