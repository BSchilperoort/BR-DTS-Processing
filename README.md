# BR-DTS-Processing
Python scripts to process the raw DTS data and calculate the bowen ratio or fluxes

###Raw ultima data
The Ultima xml files can be converted to an ascii file containing all the temperature data using the 'xml_to_txt.py' file. The folder xml_conversion contains example data.

###Temperature processing and plotting
Functions for importing the processed data can be found in the data_processing folder (dataImports). It also contains some custom functions which are used (customFunctions).

An example of how to read out, process and plot the Ultima data is located under data_processing/dts_plot_example.py
