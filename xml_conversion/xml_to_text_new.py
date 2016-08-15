##Imports
import xml.etree.cElementTree as ET
from glob import glob
from time import time
import os

#############################################################################
#   NOTE: When importing xml files, make sure the distances do not change   #
#   between files in the same folder. This will lead to errors              #
#############################################################################

##!>Set working directory to correct folder (BR-DTS-Processing)
#working_directory = r'D:\Github\BR-DTS-Processing'
working_directory = r'C:\Users\Bart\Downloads\BR-DTS-Processing-master'
os.chdir(working_directory)

##Write data to txt file
#Get start time
ta = time()

#Get all xml files from the directory
#leave different channels in different directories!
file_names = sorted(glob(r'xml_conversion\\xml_example_2016\*.xml'))
file_amount = len(file_names)

#Initialise variables
timestamp   = [None]
pt100       = [None]
data        = [None]

#Open output file, write header
data_filename = r'xml_conversion\output\dts_data_V2.txt'
data_file = open(data_filename, 'w')
data_file.write('Ultima data_file. Next row; distances (m).')

#Get distances from xml
tree = ET.ElementTree(file=file_names[0])
root = tree.getroot()

start_index = float(root[0][4].text)
end_index   = float(root[0][5].text)
increment   = float(root[0][6].text)

start_time  = root[0][7].text
end_time    = root[0][8].text

logdata = [x.text for x in root[0][15]]
data_strings = logdata[2:]

data_length    = len(data_strings)
temp           = [None]*data_length

for ii in range(0, data_length):
    temp[ii] = float(data_strings[ii].split(',')[3])

diff = (end_index - start_index)/(data_length - 1)
distances = [str(diff * x + start_index)[0:9]  for x in range(data_length)]

#Write distances to file
data_file.write('\n'+';'.join(distances))

#Write Time & temperature header
data_file.write('\nTime\tTemperature')

#Loop over all files and extract the 
for ii in range(0,file_amount):
    tree = ET.parse(file_names[ii])
    root = tree.getroot()
    
    #test if start or end indexes have changed (untested function):
    if not (float(root[0][4].text) == start_index and float(root[0][5].text) == end_index):
        raise Exception('Distance of file '+file_names[0]+' does not match starting indexes! \n'
                        'Check if settings were changed in between files')
                        
    #Copy timestamp from DTS to .txt
    timestamp = root[0][8].text[:-5]
    
    #Get the data values
    logdata      = [x.text for x in root[0][15]]
    data_strings = logdata[2:]

    #get the temperature from the xml
    #Define full list first, then add values (for speed)
    temperature = [None]*data_length
    for ii in range(0, data_length):
        temperature[ii] = data_strings[ii].split(',')[3][:-1]

    #Append to file
    file_line = '\n'+timestamp+'\t'+';'.join(temperature)
    data_file.write(file_line)

data_file.close()

#Print elapsed time; for code optimization
print('Elapsed time:',time()-ta)
