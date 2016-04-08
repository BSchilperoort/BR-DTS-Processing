##Imports
import xml.etree.cElementTree as ET
from glob import glob
from time import time

#############################################################################
#   NOTE: When importing xml files, make sure the distances do not change   #
#   between files in the same folder. This will lead to errors              #
#############################################################################

##Write data to txt file
#Get start time
ta = time()

#Get all xml files from the directory
#leave different channels in different directories!
file_names = sorted(glob(r'xml_conversion\xml_example\*.xml'))
file_amount = len(file_names)

#Initialise variables
timestamp   = [None]
pt100       = [None]
data        = [None]

#Open output file, write header
data_filename = r'xml_conversion\output\dts_data.txt'
data_file = open(data_filename, 'w')
data_file.write('Ultima data_file. Next row; distances (m).')

#Get distances from xml
tree = ET.parse(file_names[0])
root = tree.getroot()
data_line = []
for measurement in root[0][11]:
    data_line.append([x for x in measurement.text.split(',')])
distances = [row[0] for row in data_line]
data_length = len(distances)

#Write distances to file
data_file.write('\n'+';'.join(distances))

#Write Time & temperature header
data_file.write('\nTime\tTemperature')

#Loop over all files and extract the 
for ii in range(0,file_amount):
    tree = ET.parse(file_names[ii])
    root = tree.getroot()
    
    #Copy timestamp from DTS to .txt
    timestamp = root[0][3].text[:-5]
    
    #Can be used to extract Pt100 values:
    # pt100[i] = [float(root[0][5][2].text),float(root[0][5][3].text)] 
    
    #Import all data from the xml
    #Define full list first, then add values (for speed)
    data_line = [None]*data_length
    for ii in range(0,data_length):
        data_line[ii] = root[0][11][ii].text.split(',')
        
    #Extract temperature values from the dataline:
    temperature = [row[3] for row in data_line]
    
    #Append to file
    file_line = '\n'+timestamp+'\t'+';'.join(temperature)
    data_file.write(file_line)

data_file.close()

#Print elapsed time; for code optimization
print('Elapsed time:',time()-ta)